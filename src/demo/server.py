"""A loopback-only HTTP presentation of RetrievalDemo, without a web-framework dependency."""

from __future__ import annotations

import io
import json
import logging
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

from PIL import Image

from src.core.exceptions import AppError
from src.demo.service import RetrievalDemo

log = logging.getLogger(__name__)
WEB_ROOT = Path(__file__).with_name("web")
_MAX_BODY_BYTES = 16384
_ASSETS = {
    "/": ("index.html", "text/html"),
    "/app.js": ("app.js", "text/javascript"),
    "/style.css": ("style.css", "text/css"),
}


def make_server(demo: RetrievalDemo, *, port: int = 7860) -> ThreadingHTTPServer:
    """Create a local server; port=0 is useful for HTTP integration tests."""

    class Handler(BaseHTTPRequestHandler):
        def _send(self, data: bytes, kind: str, status: HTTPStatus = HTTPStatus.OK) -> None:
            self.send_response(status)
            self.send_header("Content-Type", kind + ("; charset=utf-8" if kind != "image/jpeg" else ""))
            self.send_header("Content-Length", str(len(data)))
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Cache-Control", "no-store" if kind == "application/json" else "private, max-age=3600")
            self.end_headers()
            self.wfile.write(data)

        def _json(self, data: dict[str, Any], status: HTTPStatus = HTTPStatus.OK) -> None:
            self._send(json.dumps(data, ensure_ascii=False, allow_nan=False).encode(), "application/json", status)

        def _local_request(self) -> bool:
            port = server.server_port
            hosts = {f"127.0.0.1:{port}", f"localhost:{port}"}
            origin = self.headers.get("Origin")
            return self.headers.get("Host") in hosts and (origin is None or origin in {f"http://{h}" for h in hosts})

        def do_GET(self) -> None:
            if not self._local_request():
                self._json({"error": "Chỉ dùng demo trên localhost."}, HTTPStatus.FORBIDDEN)
                return
            path = urlsplit(self.path).path
            if path in _ASSETS:
                name, kind = _ASSETS[path]
                self._send((WEB_ROOT / name).read_bytes(), kind)
            elif path == "/api/status":
                self._json({"protocol": demo.protocol, "examples": demo.examples()})
            elif path.startswith("/api/image/"):
                try:
                    image_id = int(path.removeprefix("/api/image/"))
                    with Image.open(demo.image_file(image_id)) as source:
                        image = source.convert("RGB")
                        image.thumbnail((960, 720))
                        output = io.BytesIO()
                        image.save(output, format="JPEG", quality=85)
                    self._send(output.getvalue(), "image/jpeg")
                except (AppError, ValueError, OSError):
                    self._json({"error": "Không có ảnh này trong gallery."}, HTTPStatus.NOT_FOUND)
            else:
                self._json({"error": "Không tìm thấy địa chỉ."}, HTTPStatus.NOT_FOUND)

        def do_POST(self) -> None:
            if not self._local_request():
                self._json({"error": "Chỉ dùng demo trên localhost."}, HTTPStatus.FORBIDDEN)
                return
            if urlsplit(self.path).path != "/api/search":
                self._json({"error": "Không tìm thấy địa chỉ."}, HTTPStatus.NOT_FOUND)
                return
            try:
                length = int(self.headers.get("Content-Length", "0"))
                if not 0 < length <= _MAX_BODY_BYTES:
                    raise ValueError("Dữ liệu truy vấn rỗng hoặc quá dài.")
                body = json.loads(self.rfile.read(length))
                if not isinstance(body, dict):
                    raise ValueError("Truy vấn phải là một object JSON.")
                query = body.get("query")
                if not isinstance(query, str):
                    raise ValueError("Truy vấn phải là một câu văn bản.")
                result = demo.search(
                    query,
                    results=body.get("results"),
                    relations=body.get("relations"),
                    query_id=body.get("query_id"),
                )
                self._json(result)
            except (AppError, ValueError, TypeError, UnicodeError) as exc:
                self._json({"error": str(exc)}, HTTPStatus.BAD_REQUEST)
            except Exception:
                log.exception("query failed")
                self._json(
                    {"error": "Không xử lý được truy vấn. Xem log của demo để kiểm tra model/cache."},
                    HTTPStatus.INTERNAL_SERVER_ERROR,
                )

        def log_message(self, format: str, *args: Any) -> None:
            log.info("%s", format % args)

    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    server.daemon_threads = True
    return server
