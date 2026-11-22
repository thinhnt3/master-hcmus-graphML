#!/usr/bin/env python3
"""One entry point for checking assets, restoring images, querying, serving and running the notebook."""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
from pathlib import Path
from typing import Any

from src.core.exceptions import AppError, DataError
from src.data.config import DataConfig
from src.data.download import ImageJob, download_images
from src.data.json_io import read_json, write_json
from src.demo.service import CODE_ROOT, DEFAULT_CONFIG, DemoConfig, RetrievalDemo, check_artifacts
from src.embeddings.clip_encoder import ClipEncoder

log = logging.getLogger("run_demo")


def _options(args: argparse.Namespace) -> DemoConfig:
    return DemoConfig.from_yaml(args.config, asset_root=Path(args.asset_root) if args.asset_root else None)


def _images(options: DemoConfig, *, all_images: bool) -> dict[str, Any]:
    """Restore images from the committed metadata without changing split/graph/cache files."""
    data = DataConfig.from_yaml(options.retrieval().data_config)
    processed = data.paths.processed_dir
    if not processed.is_absolute():
        processed = options.asset_root / processed
    rows = read_json(processed / "images.json")
    jobs = [
        ImageJob(int(row["vg_image_id"]), row["url"])
        for row in rows
        if all_images or row["split"] == options.split.value
    ]
    report = download_images(
        jobs,
        processed / "images",
        workers=data.download.workers,
        retries=data.download.retries,
        timeout_s=data.download.timeout_s,
    ).to_dict()
    write_json(options.asset_root / "runs/demo/image-download.json", report)
    if report["failed_count"]:
        raise DataError(f"{report['failed_count']} ảnh tải lỗi; xem runs/demo/image-download.json rồi chạy lại")
    return report


def _notebook(options: DemoConfig, output: Path, config_file: Path) -> dict[str, str]:
    """Execute the delivered notebook with the same asset root as the browser/CLI demo."""
    try:
        import nbformat
        from jupyter_client import KernelManager
        from nbclient import NotebookClient
    except ImportError as exc:
        raise DataError("Cài notebook trước: python -m pip install -r requirements-notebook.txt") from exc
    source = CODE_ROOT / "notebooks/retrieval_demo.ipynb"
    if source.resolve() == output.resolve():
        raise DataError("Chọn output khác notebook nguồn để giữ bản hướng dẫn sạch.")
    notebook = nbformat.read(source, as_version=4)
    manager = KernelManager(kernel_name="python3")
    kernel_spec = manager.kernel_spec
    if kernel_spec is None:
        raise DataError("Không tìm thấy kernel Python. Cài requirements-notebook.txt rồi chạy lại.")
    kernel_spec.argv = [sys.executable, "-m", "ipykernel_launcher", "-f", "{connection_file}"]
    client = NotebookClient(
        notebook,
        km=manager,
        timeout=600,
        kernel_name="python3",
        resources={"metadata": {"path": str(CODE_ROOT)}},
    )
    try:
        client.execute(
            env={
                **os.environ,
                "GRAPH_DEMO_ASSET_ROOT": str(options.asset_root),
                "GRAPH_DEMO_CONFIG": str(config_file.resolve()),
            }
        )
    finally:
        if client.kc is not None:
            client.kc.stop_channels()
        if manager.has_kernel:
            manager.shutdown_kernel(now=True)
    output.parent.mkdir(parents=True, exist_ok=True)
    nbformat.write(notebook, output)
    return {"source": str(source), "executed_notebook": str(output)}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("check", "images", "prepare-model", "query", "serve", "notebook"):
        command = sub.add_parser(name)
        command.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
        command.add_argument(
            "--asset-root", help="repo containing the frozen data/cache/runs; defaults to this checkout"
        )
        if name == "images":
            command.add_argument(
                "--all", action="store_true", help="restore all split images instead of the demo gallery"
            )
        elif name == "query":
            group = command.add_mutually_exclusive_group(required=True)
            group.add_argument("--text", help="a new English sentence")
            group.add_argument("--query-id", help="an existing query, with its known answer")
            command.add_argument("--results", type=int, default=None)
            command.add_argument("--relations", type=int, default=None)
            command.add_argument(
                "--output", type=Path, help="optional result JSON; no file is changed without this option"
            )
        elif name == "serve":
            command.add_argument("--port", type=int, default=7860)
        elif name == "notebook":
            command.add_argument("--output", type=Path, default=CODE_ROOT / "runs/demo/retrieval_demo.executed.ipynb")
    args = parser.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    try:
        options = _options(args)
        if args.command == "images":
            result: dict[str, Any] = _images(options, all_images=args.all)
        elif args.command == "prepare-model":
            config = options.retrieval()
            ClipEncoder(config.clip.model_name, config.clip.device)
            result = {"model": config.clip.model_name, "status": "cached for offline demo"}
        elif args.command == "notebook":
            result = _notebook(options, args.output, args.config)
        elif args.command == "check":
            result = check_artifacts(options)
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 0 if result["available_images"] == result["gallery_images"] and result["clip_cached"] else 1
        else:
            demo = RetrievalDemo.load(options)
            if args.command == "serve":
                from src.demo.server import make_server

                with make_server(demo, port=args.port) as server:
                    log.info("Mở demo: http://127.0.0.1:%s", server.server_port)
                    log.info(
                        "Gallery %s ảnh; α=%s và k=%s lấy từ validation.",
                        len(demo.images),
                        demo.protocol["alpha"],
                        demo.protocol["candidate_k"],
                    )
                    server.serve_forever()
                return 0
            query = demo.queries.get(args.query_id) if args.query_id is not None else None
            if args.query_id is not None and query is None:
                raise DataError("Không có query ID này trong split demo.")
            result = demo.search(
                query["text"] if query else args.text,
                query_id=args.query_id,
                results=args.results,
                relations=args.relations,
            )
            if args.output:
                write_json(args.output, result)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (AppError, OSError, ValueError) as exc:
        log.error("%s", exc)
        if args.command in {"serve", "query"}:
            log.error(
                "Kiểm tra dữ liệu: python -m scripts.run_demo check; "
                "cache CLIP: python -m scripts.run_demo prepare-model"
            )
        return 1
    except KeyboardInterrupt:
        log.info("Đã dừng demo.")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
