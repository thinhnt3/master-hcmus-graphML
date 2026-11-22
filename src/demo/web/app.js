"use strict";
const $ = (id) => document.getElementById(id);
let current = null,
  selectedExample = null,
  method = "graph";
function element(tag, text, className) {
  const e = document.createElement(tag);
  if (text !== undefined) e.textContent = text;
  if (className) e.className = className;
  return e;
}
function svgElement(tag, attrs, text) {
  const e = document.createElementNS("http://www.w3.org/2000/svg", tag);
  for (const [k, v] of Object.entries(attrs)) e.setAttribute(k, v);
  if (text !== undefined) e.textContent = text;
  return e;
}
function relationGraph(relations) {
  const box = element("details", undefined, "graph-details");
  box.append(element("summary", "Xem đồ thị con giải thích"));
  const svg = svgElement("svg", {
    viewBox: `0 0 320 ${relations.length * 64}`,
    role: "img",
    "aria-label": "Đồ thị con gồm các relation đang giải thích",
  });
  relations.forEach((r, i) => {
    const y = i * 64 + 28;
    svg.append(
      svgElement("rect", {
        x: 2,
        y: y - 14,
        width: 100,
        height: 28,
        rx: 5,
        fill: "#e4eee7",
        stroke: "#b5ccbf",
      }),
    );
    svg.append(
      svgElement("rect", {
        x: 218,
        y: y - 14,
        width: 100,
        height: 28,
        rx: 5,
        fill: "#e4eee7",
        stroke: "#b5ccbf",
      }),
    );
    svg.append(
      svgElement("line", {
        x1: 104,
        y1: y,
        x2: 215,
        y2: y,
        stroke: "#567d68",
        "stroke-width": 1.5,
      }),
    );
    svg.append(
      svgElement("path", {
        d: `M209 ${y - 4} L215 ${y} L209 ${y + 4}`,
        fill: "none",
        stroke: "#567d68",
      }),
    );
    const shorten = (s) => (s.length > 16 ? s.slice(0, 15) + "…" : s);
    svg.append(
      svgElement(
        "text",
        { x: 52, y: y + 4, "text-anchor": "middle", class: "graph-label" },
        shorten(r.subject),
      ),
    );
    svg.append(
      svgElement(
        "text",
        { x: 268, y: y + 4, "text-anchor": "middle", class: "graph-label" },
        shorten(r.object),
      ),
    );
    svg.append(
      svgElement(
        "text",
        { x: 160, y: y - 8, "text-anchor": "middle", class: "predicate" },
        r.predicate,
      ),
    );
  });
  box.append(svg);
  return box;
}
function picture(row) {
  const box = element("div", undefined, "photo"),
    img = element("img");
  img.src = row.image_url;
  img.alt = `Ảnh Visual Genome ${row.image_id}`;
  img.loading = "lazy";
  img.onerror = () => {
    img.hidden = true;
    box.append(element("span", "Không tải được ảnh."));
  };
  box.append(img, element("span", `#${row.rank}`, "rank"));
  return box;
}
function render() {
  if (!current) return;
  const graph = method === "graph",
    rows = graph ? current.results : current.clip_results;
  $("graph-tab").setAttribute("aria-selected", String(graph));
  $("clip-tab").setAttribute("aria-selected", String(!graph));
  $("graph-tab").tabIndex = graph ? 0 : -1;
  $("clip-tab").tabIndex = graph ? -1 : 0;
  $("result-list").setAttribute(
    "aria-labelledby",
    graph ? "graph-tab" : "clip-tab",
  );
  $("method-note").textContent = graph
    ? "Các ảnh sau khi kết hợp điểm. Quan hệ bên dưới được kiểm bằng cách bỏ riêng rồi chấm lại."
    : "Xếp hạng bằng CLIP trên cùng gallery, trước khi kết hợp graph.";
  $("result-list").replaceChildren();
  for (const row of rows) {
    const card = element("article", undefined, "result-card");
    card.append(picture(row));
    const content = element("div", undefined, "card-body"),
      title = element("div", undefined, "card-title");
    title.append(element("h3", `VG ${row.image_id}`));
    if (graph) {
      title.append(
        element("span", `CLIP #${row.clip_rank} → #${row.rank}`, "move"),
      );
      content.append(title);
      const scores = element("div", undefined, "scores");
      for (const [label, key] of [
        ["CLIP", "clip_score"],
        ["Graph", "graph_score"],
        ["Điểm cuối", "final_score"],
      ]) {
        const cell = element("div");
        cell.append(element("small", label), element("b", row[key].toFixed(4)));
        scores.append(cell);
      }
      content.append(scores);
      const relations = element("div", undefined, "relations");
      relations.append(element("h4", "Quan hệ có tác động cao nhất"));
      if (!row.relations.length)
        relations.append(element("p", "Không có relation để giải thích."));
      for (const r of row.relations) {
        const item = element("div", undefined, "relation");
        item.append(
          element("strong", `${r.subject} → ${r.predicate} → ${r.object}`),
        );
        const drop = (r.score_drop >= 0 ? "+" : "") + r.score_drop.toFixed(5);
        item.append(
          element(
            "div",
            `Bỏ riêng: giảm điểm graph ${drop}`,
            `delta${r.score_drop < 0 ? " negative" : ""}`,
          ),
        );
        relations.append(item);
      }
      if (row.relations.length) relations.append(relationGraph(row.relations));
      if (!row.rerank_candidate)
        relations.append(
          element(
            "p",
            "Ngoài top-k ứng viên CLIP: graph không được dùng cho điểm cuối của ảnh này.",
          ),
        );
      content.append(relations);
    } else {
      content.append(title);
    }
    card.append(content);
    $("result-list").append(card);
  }
}
async function search(event) {
  event.preventDefault();
  const text = $("query").value.trim();
  if (!text) return;
  $("search-button").disabled = true;
  $("status").classList.remove("error");
  $("status").textContent = "Đang tìm ảnh và kiểm tra các relation…";
  $("search-output").hidden = true;
  try {
    const body = { query: text, results: Number($("results").value) };
    if (selectedExample && selectedExample.text === text)
      body.query_id = selectedExample.query_id;
    const response = await fetch("/api/search", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      }),
      data = await response.json();
    if (!response.ok) throw Error(data.error || "Không xử lý được truy vấn.");
    current = data;
    method = "graph";
    $("status").textContent =
      `Đã tìm trong ${data.protocol.gallery_images.toLocaleString("vi-VN")} ảnh · ${data.elapsed_seconds.toFixed(2)} giây.`;
    $("query-summary").textContent = `“${data.query}”`;
    $("truth").replaceChildren();
    $("truth").hidden = !data.ground_truth;
    if (data.ground_truth) {
      const t = data.ground_truth,
        img = element("img");
      img.src = t.image_url;
      img.alt = `Ảnh đáp án VG ${t.image_id}`;
      const label = element("div");
      label.append(
        element("strong", `Đáp án của ví dụ: VG ${t.image_id}`),
        element(
          "p",
          `Hạng ảnh đúng: CLIP ${t.clip_rank} → sau rerank ${t.reranked_rank}.`,
        ),
      );
      $("truth").append(img, label);
    } else {
      $("status").textContent += " Câu mới chưa có nhãn đáp án.";
    }
    $("search-output").hidden = false;
    render();
  } catch (error) {
    $("status").classList.add("error");
    $("status").textContent = error.message;
  } finally {
    $("search-button").disabled = false;
  }
}
$("search-form").addEventListener("submit", search);
$("query").addEventListener("input", () => {
  selectedExample = null;
});
$("graph-tab").onclick = () => {
  method = "graph";
  render();
};
$("clip-tab").onclick = () => {
  method = "clip";
  render();
};
$("download").onclick = () => {
  if (!current) return;
  const url = URL.createObjectURL(
    new Blob([JSON.stringify(current, null, 2)], { type: "application/json" }),
  );
  const a = element("a");
  a.href = url;
  a.download = "retrieval-result.json";
  a.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
};
(async () => {
  try {
    const response = await fetch("/api/status"),
      data = await response.json();
    if (!response.ok) throw Error(data.error);
    const p = data.protocol;
    $("status").textContent =
      `Sẵn sàng · ${p.gallery_images.toLocaleString("vi-VN")} ảnh ${p.dataset}.`;
    $("protocol").textContent =
      `Gallery ${p.gallery_split}, seed ${p.seed}; α=${p.alpha}, k=${p.candidate_k}, lấy từ validation. Không chọn lại tham số trong demo.`;
    data.examples.forEach((example, i) => {
      const b = element("button", `Ví dụ ${i + 1}: ${example.text}`);
      b.type = "button";
      b.onclick = () => {
        $("query").value = example.text;
        selectedExample = example;
        $("query").focus();
      };
      $("examples").append(b);
    });
    $("search-button").disabled = false;
  } catch (error) {
    $("status").classList.add("error");
    $("status").textContent = "Không kết nối được demo: " + error.message;
  }
})();

for (const id of ["graph-tab", "clip-tab"])
  $(id).addEventListener("keydown", (event) => {
    if (["ArrowLeft", "ArrowRight", "Home", "End"].includes(event.key)) {
      event.preventDefault();
      const target =
        event.key === "Home" || event.key === "ArrowLeft"
          ? "graph-tab"
          : "clip-tab";
      $(target).click();
      $(target).focus();
    }
  });
