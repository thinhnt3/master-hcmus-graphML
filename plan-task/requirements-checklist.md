# Checklist nghiệm thu bài nộp

Cập nhật 22/11/2026 theo báo cáo kỹ thuật và hồ sơ nộp hiện tại.
Phân công: [task.md](../task.md). `[x]` có artifact/bằng chứng; `[~]` còn giới hạn;
`[ ]` chưa có. Có code hoặc có bảng không đồng nghĩa toàn bộ bài đã sẵn sàng nộp.

## 1. Mã nguồn, môi trường và chạy lại

- [x] CLIP frozen, GraphSAGE, AdaMF-MAT adaptation, benchmark và explanation đã có code/config/test.
- [x] Đã tích hợp hướng dẫn của Phú, năm config ablation MKG-W caption subset và panel W&B dataset 2.
- [x] Có `scripts/build_vg_coco.py`: sources → join → normalize → split → export → images → graph; có checksum raw và chặn ghi đè metadata khác nếu thiếu `--overwrite`.
- [x] `scripts/review_vg_coco.py` audit metadata thật: 7.000/1.500/1.500 ảnh và 35.000/7.500/7.500 query; không trùng split, query đúng caption/ảnh/split, graph đúng ID/vocabulary.
- [x] Có kiểm thử tích hợp từ raw giả lập tới graph và kiểm chặn query/split/graph sai. Bản tích hợp qua 514 test; Ruff sạch; mypy sạch trên 128 file nguồn (Python 3.12, môi trường constraints demo).
- [x] Đã dựng lại metadata VG–COCO và đối chiếu ID split, caption và nội dung graph. Định dạng của một số tệp xuất khác bản lưu dùng cho checkpoint.
- [x] Có requirements nền, dependency notebook riêng và constraints các phiên bản đã chạy demo.
- [~] Constraints demo không phải lock toàn bộ dependency/OS/CUDA. Ảnh, embedding và checkpoint lớn cần gói bàn giao hoặc dựng lại; không có trong Git.

Nguồn: `README.md`, `requirements*.txt`, `scripts/{build_vg_coco,review_vg_coco,run_demo}.py`, `tests/data/test_vg_coco_commands.py`.

## 2. Split và chống rò rỉ

- [x] VG–COCO: 10.000 ảnh, 50.000 caption; test chỉ từ Karpathy test; vocab graph từ train.
- [x] MKG-W caption subset: 2.055/440/441 mục và 2 caption/mục; split versioned.
- [x] α/k, checkpoint và query-adaptive alpha chọn/fit trên validation; không chọn lại từ test.
- [x] Các baseline/ablation dùng cùng split/gallery; full và bốn biến thể chạy ba seed 13/37/97.
- [x] Cache/run lưu hash đầu vào; consumer kiểm hash và settings, resume từ chối artifact sai/thiếu.
- [x] MMKG remote có split claim theo cặp đỉnh; fact val/test không ở train graph; code masking cạnh truy vấn train.
- [~] Audit phát hiện bảng điền synset của bản lưu được tạo trước split. Từ vựng graph dùng train. Chưa huấn luyện lại với bảng synset chỉ từ train.

Nguồn: `src/data/`, `src/models/run_validation.py`, `src/evaluation/`, `data/splits/`, data card VN Heritage.

## 3. Báo cáo 12–18 trang, slide và đóng góp

- [x] Có README, tài liệu năm chương + phụ lục của Phú, bảng Markdown/LaTeX trong `table.md`, report XAI và data card MMKG.
- [x] `task.md` có bốn người phụ trách các phần riêng, ba cặp và việc chung cả nhóm. Script xuất bảng của Quốc Thịnh là đầu ra cần bổ sung.
- [x] Báo cáo 12 trang đính kèm Prism và bản [PDF trên GitHub](../report.pdf).
- [x] Slide 12 trang có trong hồ sơ nộp của nhóm, kịch bản 18 phút 30 giây gồm demo.
- [x] Báo cáo ghi phân công, thư viện, nguồn mở và phần dùng AI hỗ trợ.

Bảng kết quả, phân tích ca và demo VG–COCO trong báo cáo dùng checkpoint GraphSAGE của cùng bộ thực nghiệm.

## 4. Notebook/giao diện truy vấn và giải thích

- [x] UI local nhập text mới, top-3/5/10, ảnh thật, điểm CLIP/graph/fused, so baseline, subgraph và signed deletion score.
- [x] Notebook dùng chung service, có công thức, shape và ảnh; đã chạy 8/8 cell code với CLIP/checkpoint thật.
- [x] Demo kiểm provenance, chỉ dùng known-query ground truth khi ID và text khớp; query tự nhập không có nhãn đúng giả định.
- [x] Tải lại ảnh gallery bằng metadata; không chỉnh α/k hoặc train lại trong demo.
- [~] Đã chạy UI và CLI GraphSAGE trên VG–COCO, cả truy vấn có mã và câu mới. Cả nhóm cần thử trên máy vấn đáp.

Nguồn: `src/demo/`, `scripts/run_demo.py`, `notebooks/retrieval_demo.ipynb`, `configs/demo/vg_coco.yaml`.

## 5. Phân tích 5 thành công và 5 thất bại

- [x] Bảng XV trong báo cáo có 5 ca ảnh đích lên hạng nhất và 5 ca mất hạng nhất, gồm mã truy vấn, ID ảnh, hạng và giải thích.
- [x] Mười ca dùng mô hình GraphSAGE seed 13, giống demo.
- [x] Phụ lục của hồ sơ nộp có ảnh, điểm, hạng, quan hệ và hạng sau khi xóa quan hệ.
- [~] Nhận xét về thiếu/nhiễu scene graph chỉ là giả thuyết từ các ca minh hoạ, chưa là kết luận nhân quả toàn tập.

Nguồn: [báo cáo kỹ thuật](../report.pdf) và `scripts/explain_retrieval.py`.

## 6. Cấp độ 2: hai tập công khai và ≥20 query

- [x] VG–COCO và MKG-W đã có pipeline/kết quả; ablation dataset 2 có đủ năm YAML.
- [x] AdaMF-MAT (2024) có adaptation và kết quả; tách bản retrieval với bản KG/reproduction.
- [x] Có bộ 30 câu viết tay và bộ KG trực tiếp/gián tiếp; định nghĩa và cách dựng trong `docs/mkg-w-results.md`.
- [x] Ghi giới hạn oracle anchor/relation của nhánh KG; không so ngang với text-only như cùng đầu vào.
- [x] Phụ lục ghi bộ 5.154 truy vấn test MKG-W và kết quả đối chiếu 24 truy vấn mẫu theo định nghĩa trực tiếp/gián tiếp.

## 7. Cấp độ 3: MMKG tự xây và XAI

- [x] MMKG chuẩn là VN Heritage trên remote: 160 địa điểm, 772 ảnh, 849 thực thể, 981 claim/18 quan hệ và 902 cạnh bài viết.
- [x] Có card, metadata nguồn/ảnh, linking, split và hướng dẫn xây; không thay bằng MMKG local cũ.
- [x] Có transfer GraphSAGE và ablation; tách gallery 772 ảnh với gallery 160 địa điểm, đúng cách gộp split/seed.
- [x] Fidelity, sparsity/keep-only trên VG–COCO có random control, budget thực tế và ca skip.
- [~] Validity dùng nhãn thí điểm của AI trên 20 truy vấn và 42 quan hệ. Có 17 quan hệ đúng ảnh và liên quan tới truy vấn, 2 quan hệ chưa rõ. Chưa có nhãn người độc lập.
- [ ] Người kiểm tay validity, mẫu ảnh đúng địa điểm và mẫu cạnh rút từ bài theo rubric đã chốt.
- [x] Gói VN Heritage của nhóm có 772 ảnh và bảng ghi công theo ảnh. Điều kiện sử dụng nằm trong [data card](../docs/vn-heritage-data-card.md).

Nguồn: `docs/vn-heritage-results.md`, `data/processed/vn_heritage_core/`, `docs/wandb-report/70*`–`73*`.

## 8. Demo trực tiếp và video dự phòng

- [x] Có code UI/notebook và kịch bản demo dưới 5 phút trong README.
- [x] Có `reports/demo/retrieval-demo.mp4`: khoảng 1:30 (<5 phút), H.264, phụ đề tiếng Việt, không lời đọc; ghi thao tác thật và đã kiểm frame/thời lượng.
- [x] Video dự phòng đã có phụ đề, thuận tiện mở khi máy demo gặp sự cố.
- [x] Gói demo có 1.500 ảnh, cache và checkpoint seed 13. Lần chạy đầu tải CLIP bằng `prepare-model`.
- [ ] Thử mở lại bằng môi trường/gói artifact trên máy vấn đáp.

## Phần mở rộng tùy chọn

- [x] Query-adaptive alpha của Phú có code/config và 27 kiểm thử, đã tích hợp.
- [ ] Chạy và báo kết quả trên cả hai tập công khai, gồm random control; chưa nhận hoàn thành cấp độ 4 hoặc có cải thiện.
- [ ] Backbone thứ hai, hub ablation và matched-parameter direction ablation: chưa có; không phải các mục đã nghiệm thu.

## Kết luận nghiệm thu

Hồ sơ có mã nguồn, split, báo cáo, slide, demo, notebook, video dự phòng, phụ lục truy vấn và dữ liệu VN Heritage. Việc còn lại trước buổi chấm là thử demo trên máy dùng để trình bày. Validity trong báo cáo là kết quả thí điểm dùng nhãn AI.
