# Học máy với dữ liệu đồ thị - HP3-K35

## Giới thiệu

**Project 3: Multimodal XAI** — truy vấn đa phương thức có giải thích bằng đồ thị. Nhóm làm bài toán text-to-image: cho một câu mô tả, hệ thống tìm ảnh khớp nhất và chỉ ra các quan hệ trong đồ thị đã góp vào kết quả.

Quy trình tổng thể: truy vấn → mã hóa bằng CLIP → chọn top-k ứng viên theo cosine → tính điểm đồ thị cho từng ứng viên (nhúng GNN hoặc đường đi nối truy vấn với ứng viên) → xếp hạng lại → kết quả + quan hệ/đường đi đã dùng làm giải thích → đánh giá fidelity.

## Thành viên

| Tên | MSSV |
|---|---|
| Trần Quốc Thịnh | 25C11065 |
| Đỗ Thanh Nghị | 25C11051 |
| Phan Lê Đắc Phú | 25C11059 |
| Nguyễn Trường Thịnh | 25C11066 |

## Báo cáo

- Bài báo cáo: [report.pdf](report.pdf).
- Báo cáo W&B: [link](https://forge.coreweave.com/wandb/thinhnt3-vnggames/vg-coco-graph-retrieval/reports/x--VmlldzoxODM0MjcyMA); danh sách link và mục lục ở [wandb-reports.md](wandb-reports.md).
- Tài liệu giải thích đầy đủ, có hình minh hoạ: [docs/README.md](docs/README.md).
- Kết quả chi tiết: [VG ∩ COCO](docs/04-ket-qua.md), [MKG-W](docs/mkg-w-results.md), [VN Heritage](docs/vn-heritage-results.md).

## Task

Phân công và tình trạng bàn giao: [task.md](task.md). Bảng số liệu cho báo cáo, kèm mã LaTeX: [table.md](table.md).

| Cấp độ | Yêu cầu của đề | Tình trạng | Chi tiết |
|---|---|---|---|
| 1 | CLIP đóng băng, một GNN, xếp hạng lại, so CLIP với CLIP + đồ thị | Có | [Kết quả](docs/04-ket-qua.md) |
| 1 | Ablation bỏ cạnh hoặc cạnh ngẫu nhiên | Có, trên cả ba dataset | [Kết quả](docs/04-ket-qua.md) |
| 1 | Hiển thị quan hệ đã dùng; 5 truy vấn thành công và 5 thất bại | Có | [Kết quả](docs/04-ket-qua.md) |
| 2 | Ít nhất 2 tập công khai | Có: VG ∩ COCO và MKG-W | [Dữ liệu](docs/02-du-lieu.md) |
| 2 | Một phương pháp từ 2024 trên cùng pipeline | Có: AdaMF-MAT | [MKG-W](docs/mkg-w-results.md) |
| 2 | Bộ ≥ 20 truy vấn, tách trực tiếp và gián tiếp | Có | [MKG-W](docs/mkg-w-results.md) |
| 3 | Fidelity, sparsity trên ≥ 10 truy vấn | Có | [Kết quả](docs/04-ket-qua.md) |
| 3 | Validity | Một phần: nhãn do AI chấm, chưa có người chấm | [Kết quả](docs/04-ket-qua.md) |
| 3 | MMKG tự xây, chạy phương pháp của cấp độ 1/2 trên đó | Có: VN Heritage | [VN Heritage](docs/vn-heritage-results.md) |
| 4 | Cải tiến riêng: α theo truy vấn | Một phần: code và test xong, chưa có số liệu | [query-alpha](docs/query-alpha.md) |

## Cấu trúc repo

```
configs/            tham số dữ liệu và thí nghiệm (YAML)
src/data/           xây dữ liệu: VG ∩ COCO, MKG-W, VN Heritage
src/embeddings/     CLIP đóng băng và kho lưu vector
src/models/         đồ thị con, GraphSAGE, AdaMF-MAT, huấn luyện, giải thích
src/retrieval/      xếp hạng lại, so khớp từ, đọc config
src/evaluation/     Recall@K, MRR, benchmark, ablation, fidelity, sparsity, validity
src/demo/           engine và giao diện web của demo
scripts/            các lệnh chạy (dựng dữ liệu, embedding, train, benchmark, demo)
notebooks/          notebook demo
runs/               kết quả benchmark và lượt huấn luyện
reports/            báo cáo có hình: duyệt dữ liệu, ablation, đánh giá giải thích
docs/               tài liệu giải thích, kết quả từng dataset, phần chữ của report W&B
tools/              form chấm validity
plans/, plan-task/  kế hoạch, nhật ký và checklist yêu cầu
tests/              test tự động
task.md             phân công
table.md            bảng cho báo cáo
wandb-reports.md    link report W&B
```

## Cách chạy

Cần Python 3.12. Chạy mọi lệnh từ thư mục gốc của repo.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Cấp độ 1 trên VG ∩ COCO:

```bash
python -m scripts.build_vg_coco --stage images           # khôi phục 10.000 ảnh theo metadata đã chốt (1,4 GB, không nằm trong Git)
python -m scripts.embed_vg_coco                          # vector CLIP của ảnh, caption, chữ trên đồ thị
python -m scripts.run_benchmark --method clip            # baseline CLIP
python -m scripts.train_graphsage                        # huấn luyện 3 seed, khoảng 2 phút mỗi seed trên CPU
python -m scripts.run_benchmark --method graphsage       # CLIP + GraphSAGE
python -m scripts.explain_retrieval --sample 5           # kết quả kèm relation giải thích
```

Cấp độ 2 (AdaMF-MAT), ablation và đánh giá giải thích:

```bash
python -m scripts.train_graphsage --model adamf_mat
python -m scripts.run_benchmark --method adamf_mat --run adamf-mat-d256-mu1

python -m scripts.train_graphsage --config configs/retrieval/ablations/objects_only.yaml --resume
python -m scripts.run_benchmark --method graphsage --config configs/retrieval/ablations/objects_only.yaml
python -m scripts.analyze_ablation

python -m scripts.evaluate_fidelity --config configs/evaluation/fidelity.yaml
python -m scripts.evaluate_explanation_quality
```

Kiểm thử:

```bash
pytest                                                   # chạy offline, không cần mạng
```

Lưu ý:

- `train_graphsage` báo cáo lên Weights & Biases. Đổi `wandb.mode` trong `configs/retrieval/vg_coco.yaml` thành `offline` hoặc `disabled` nếu không dùng.
- Lệnh cho MKG-W: [docs/mkg-w-results.md](docs/mkg-w-results.md#chạy-lại). Lệnh cho VN Heritage: [docs/vn-heritage-results.md](docs/vn-heritage-results.md#chạy-lại).
- Toàn bộ lệnh, tuỳ chọn và bản đồ code: [docs/05-chay-lai-va-ban-do-code.md](docs/05-chay-lai-va-ban-do-code.md).

## Demo

Video: [reports/demo/retrieval-demo.mp4](reports/demo/retrieval-demo.mp4) — khoảng 1 phút 30 giây, ghi từ thao tác thật, có phụ đề tiếng Việt, không có lời đọc.

Demo chạy tại máy trên VG ∩ COCO với CLIP ViT-B/32 và checkpoint GraphSAGE đã huấn luyện: nhập một câu mô tả tiếng Anh, xem top-k ảnh, so hai bảng xếp hạng CLIP và CLIP + GraphSAGE, và mở đồ thị con của các quan hệ giải thích.

```bash
pip install -r requirements-notebook.txt
python -m scripts.run_demo prepare-model                 # cache CLIP một lần (cần mạng), sau đó chạy offline
python -m scripts.run_demo images                        # khôi phục 1.500 ảnh gallery của tập test
python -m scripts.run_demo check                         # kiểm dữ liệu, checkpoint, cache CLIP, ảnh gallery
python -m scripts.run_demo serve                         # mở http://127.0.0.1:7860
```

Chạy từ terminal hoặc notebook thay cho giao diện web:

```bash
python -m scripts.run_demo query --text "A man riding a horse on a grassy field."
python -m scripts.run_demo notebook                      # chạy notebooks/retrieval_demo.ipynb, lưu bản có output
```

Nếu `check` báo thiếu vector hoặc checkpoint, chạy các lệnh embedding và train ở mục [Cách chạy](#cách-chạy) trước.
