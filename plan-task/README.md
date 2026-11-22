# Plan task - Text-to-image with graph reranking

> **Ghi chú 18/11/2026:** bảng trạng thái P0–P5 trong file này viết cho bản thử 40 ảnh (10/11/2026) và không còn đúng. Tiến độ nghiệm thu hiện hành nằm ở [requirements-checklist.md](requirements-checklist.md); kế hoạch ở `plans/261117-0037-multimodal-graph-retrieval-roadmap/`; phân công ở `task.md`; giải thích dự án ở `docs/README.md`. Các quy tắc chống rò rỉ dữ liệu, dùng chung split và tập ứng viên, và chạy ít nhất 3 seed vẫn áp dụng.

## Phạm vi đề xuất

Mục tiêu an toàn để đạt Cấp độ 1 và tạo đường nâng lên Cấp độ 3:

- Nhánh: text-to-image.
- Dataset công khai ban đầu: Visual Genome vì có ảnh, caption/region và scene graph sẵn.
- Baseline: CLIP frozen + FAISS.
- Graph model: chọn **một** trong GCN/GAT/GraphSAGE sau benchmark smoke test; mặc định GraphSAGE vì dễ mở rộng và ít phụ thuộc hơn.
- Score: `final = alpha * clip_cosine + (1-alpha) * graph_score`; alpha chỉ chọn trên validation.
- Evaluation: Recall@1/5/10, MRR; tối thiểu 10 query cho Cấp độ 1, tối thiểu 20 query và direct/indirect split cho Cấp độ 2.
- Đích mở rộng: Cấp độ 3 với MMKG tiếng Việt nhỏ và fidelity/validity/sparsity trên tối thiểu 10 query.

Nếu muốn Cấp độ 2, thêm dataset thứ hai sau khi pipeline Visual Genome ổn định. Nếu muốn Cấp độ 4, chỉ chọn sau khi Cấp độ 3 có kết quả reproducible.

## Dependency graph

```text
P0 scope/data decision
        |
P1 contracts + split + leakage policy
   _____|____________________
  /      |        |          \
P2-data P2-clip P2-graph   P2-query
  \______|________|__________/
         P3 integration + smoke test
                    |
       P4 experiments (3 seeds)
          ____|___________
         /      |         \
   P4-ablation P4-xai  P4-custom-mmkg
         \______|________/
             P5 report/demo
```

## Có thể chạy song song

Sau P1: download/inspect dữ liệu, CLIP+FAISS baseline, graph schema, query-set design và environment lock có thể chạy song song nếu cùng tuân thủ contract.

Sau P3: metric implementation, ablation harness, explanation extraction và custom-MMKG collection có thể chạy song song; các nhánh chỉ dùng artifact versioned từ P3.

## Phải chạy đồng bộ

- P0 phải chốt dataset/model trước P2.
- P1 phải chốt split, ID mapping, graph schema trước mọi preprocessing/model.
- P3 phải tích hợp trên cùng candidate pool trước khi so sánh CLIP với graph.
- P4 experiment phải chạy sau smoke test và freeze config.
- P5 chỉ bắt đầu khi đủ logs 3 seed, ablation và query-level examples.

## Definition of done tổng

Có thể chạy lại từ một command/config; có split cố định; không leakage; có CLIP-only và CLIP+Graph; có ablation; có mean/std từ 3 seed; có bảng metric và 5 query thành công + 5 query thất bại; nếu nhận Cấp độ 3 thì có MMKG tiếng Việt, data card và fidelity/validity/sparsity.

## Trạng thái hiện hành

Bảng tiến độ pilot 40 ảnh đã được thay bằng checklist nghiệm thu ngày 22/11/2026.
Xem [requirements-checklist.md](requirements-checklist.md) và [phân công](../task.md).
Code hiện dùng GraphSAGE đã huấn luyện, hai tập công khai và MMKG VN Heritage;
không dùng các mốc 28/10/10 hoặc scorer từ khóa của pilot để mô tả bản cuối.

UI/notebook và CLI dựng/audit VG–COCO đã có. Báo cáo cuối, slide, video và gói
artifact vẫn cần bàn giao theo checklist. Dependency graph phía trên là kế hoạch
triển khai gốc, không phải bằng chứng rằng mọi bước P5 đã hoàn tất.
