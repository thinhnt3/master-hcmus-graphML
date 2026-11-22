"""Offline notebook rendering of the shared demo result; no HTTP server needed."""

from __future__ import annotations

import base64
import html
import io
from typing import Any

from PIL import Image

from src.demo.service import RetrievalDemo


def result_html(demo: RetrievalDemo, result: dict[str, Any]) -> str:
    """Render actual result images and relation deltas as a portable, escaped HTML fragment."""
    cards = []
    for row in result["results"]:
        with Image.open(demo.image_file(row["image_id"])) as source:
            image = source.convert("RGB")
            image.thumbnail((480, 360))
            output = io.BytesIO()
            image.save(output, format="JPEG", quality=80)
        encoded = base64.b64encode(output.getvalue()).decode()
        relations = "".join(
            f"<li>{html.escape(r['subject'])} → {html.escape(r['predicate'])} → {html.escape(r['object'])}"
            f"<br><small>Giảm điểm graph khi bỏ riêng: {r['score_drop']:+.5f}; "
            f"giảm điểm cuối: {r['final_score_drop']:+.5f}</small></li>"
            for r in row["relations"]
        )
        cards.append(
            f'<article style="border:1px solid #d4d4d8;border-radius:10px;padding:12px;min-width:0">'
            f'<img alt="Ảnh VG {row["image_id"]}" src="data:image/jpeg;base64,{encoded}" '
            'style="width:100%;height:180px;object-fit:contain;background:#f4f4f5">'
            f"<h4>#{row['rank']} · VG {row['image_id']} · CLIP hạng {row['clip_rank']}</h4>"
            f"<p>CLIP {row['clip_score']:.4f} · graph {row['graph_score']:.4f} · cuối {row['final_score']:.4f}</p>"
            f'<ul style="padding-left:18px">{relations}</ul></article>'
        )
    truth = result["ground_truth"]
    note = (
        f"Ví dụ có đáp án: VG {truth['image_id']}, hạng CLIP {truth['clip_rank']} → "
        f"hạng sau rerank {truth['reranked_rank']}."
        if truth is not None
        else "Câu mới chưa có nhãn đáp án; demo không tự kết luận ảnh đúng hay sai."
    )
    return (
        f"<div><h3>{html.escape(result['query'])}</h3><p>{note}</p>"
        "<p>Điểm cosine là mức phù hợp, không phải xác suất. Quan hệ được xếp theo tác động khi bỏ riêng.</p>"
        '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:12px">'
        + "".join(cards)
        + "</div></div>"
    )
