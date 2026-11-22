# Checklist nghiệm thu bài nộp

Cập nhật 22/11/2026 theo bản tích hợp từ remote và phần demo/notebook mới.
Phân công: [task.md](../task.md). `[x]` có artifact/bằng chứng; `[~]` còn giới hạn;
`[ ]` chưa có. Có code hoặc có bảng không đồng nghĩa toàn bộ bài đã sẵn sàng nộp.

## 1. Mã nguồn, môi trường và chạy lại

- [x] CLIP frozen, GraphSAGE, AdaMF-MAT adaptation, benchmark và explanation đã có code/config/test.
- [x] Đã tích hợp hướng dẫn của Phú, năm config ablation MKG-W caption subset và panel W&B dataset 2.
- [x] Có `scripts/build_vg_coco.py`: sources → join → normalize → split → export → images → graph; có checksum raw và chặn ghi đè metadata khác nếu thiếu `--overwrite`.
- [x] `scripts/review_vg_coco.py` audit metadata thật: 7.000/1.500/1.500 ảnh và 35.000/7.500/7.500 query; không trùng split, query đúng caption/ảnh/split, graph đúng ID/vocabulary.
- [x] Có kiểm thử tích hợp từ raw giả lập tới graph và kiểm chặn query/split/graph sai. Bản tích hợp qua 514 test; Ruff sạch; mypy sạch trên 128 file nguồn (Python 3.12, môi trường constraints demo).
- [~] Chưa chạy lại toàn bộ download/build từ raw công khai bằng CLI mới trong một môi trường sạch. Script dùng lại các module dữ liệu có sẵn; không tuyên bố đã tái tạo byte-for-byte bộ lịch sử.
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
- [~] Audit metadata không thay thế kiểm ảnh trùng nội dung, nhãn ngữ nghĩa hay leakage audit độc lập.

Nguồn: `src/data/`, `src/models/run_validation.py`, `src/evaluation/`, `data/splits/`, data card VN Heritage.

## 3. Báo cáo 12–18 trang, slide và đóng góp

- [x] Có README, tài liệu năm chương + phụ lục của Phú, bảng Markdown/LaTeX trong `table.md`, report XAI và data card MMKG.
- [x] Có bảng phân công đúng bốn người, bốn việc riêng và ba việc chung từng cặp trong `task.md`; tài khoản Git đã xác nhận được ghi riêng.
- [~] Prism: đợt 1 đã sửa phương pháp/công thức/citation; bản PDF đã kiểm ở đợt đó là 10 trang. Còn abstract/tác giả, XAI/MMKG, nguồn bảng và bản cuối 12–18 trang.
- [ ] Slide thuyết trình.
- [~] Đã ghi rõ hỗ trợ AI ở phần tích hợp; báo cáo cuối còn cần khai báo nguồn mở/AI và đóng góp thực tế của thành viên.

Không lấy lượt GraphSAGE 17/11, 18/11 và 21/11 ghép thành một bảng ba seed.

## 4. Notebook/giao diện truy vấn và giải thích

- [x] UI local nhập text mới, top-3/5/10, ảnh thật, điểm CLIP/graph/fused, so baseline, subgraph và signed deletion score.
- [x] Notebook dùng chung service, có công thức, shape và ảnh; đã chạy 8/8 cell code với CLIP/checkpoint thật.
- [x] Demo kiểm provenance, chỉ dùng known-query ground truth khi ID và text khớp; query tự nhập không có nhãn đúng giả định.
- [x] Tải lại ảnh gallery bằng metadata; không chỉnh α/k hoặc train lại trong demo.
- [~] Demo hiện cho VG–COCO/GraphSAGE. Cần gói model/cache và chạy thử trên máy trình bày; không nhận đã demo MMKG/AdaMF-MAT qua UI.

Nguồn: `src/demo/`, `scripts/run_demo.py`, `notebooks/retrieval_demo.ipynb`, `configs/demo/vg_coco.yaml`.

## 5. Phân tích 5 thành công và 5 thất bại

- [x] README có 5 ca ảnh đúng lên hạng 1 và 5 ca rơi khỏi hạng 1, hạng CLIP → fused, điểm graph, relation và quy tắc chọn.
- [x] Đã ghi ba caption thành công cùng thuộc một ảnh và các ca thuộc lượt 21/11, khác checkpoint bảng chính 18/11.
- [~] Report HTML XAI có ảnh/graph; cần bàn giao ground-truth image, prediction, query ID và trace khớp lượt 21/11. Giảm score sau xoá relation không phải hạng của ảnh ground truth.
- [~] Nhận xét về thiếu/nhiễu scene graph chỉ là giả thuyết từ các ca minh hoạ, chưa là kết luận nhân quả toàn tập.

Nguồn: `README.md`, `reports/explanation-quality/index.html`, `scripts/explain_retrieval.py`.

## 6. Cấp độ 2: hai tập công khai và ≥20 query

- [x] VG–COCO và MKG-W đã có pipeline/kết quả; ablation dataset 2 có đủ năm YAML.
- [x] AdaMF-MAT (2024) có adaptation và kết quả; tách bản retrieval với bản KG/reproduction.
- [x] Có bộ 30 câu viết tay và bộ KG trực tiếp/gián tiếp; định nghĩa và cách dựng trong `docs/mkg-w-results.md`.
- [x] Ghi giới hạn oracle anchor/relation của nhánh KG; không so ngang với text-only như cùng đầu vào.
- [~] Cần chọn bộ query cuối đưa phụ lục và kiểm tra thủ công theo định nghĩa đã công bố.

## 7. Cấp độ 3: MMKG tự xây và XAI

- [x] MMKG chuẩn là VN Heritage trên remote: 160 địa điểm, 772 ảnh, 849 thực thể, 981 claim/18 quan hệ và 902 cạnh bài viết.
- [x] Có card, metadata nguồn/ảnh, linking, split và hướng dẫn xây; không thay bằng MMKG local cũ.
- [x] Có transfer GraphSAGE và ablation; tách gallery 772 ảnh với gallery 160 địa điểm, đúng cách gộp split/seed.
- [x] Fidelity, sparsity/keep-only trên VG–COCO có random control, budget thực tế và ca skip.
- [~] Validity là một lượt AI: 20 query/42 relation, 83,3% theo rubric rộng và 33,3% theo rubric chặt. Chưa có nhãn người độc lập.
- [ ] Người kiểm tay validity, mẫu ảnh đúng địa điểm và mẫu cạnh rút từ bài theo rubric đã chốt.
- [~] Có nguồn/license trong metadata và báo cáo dữ liệu; còn đóng gói ảnh kèm attribution/điều kiện sử dụng cụ thể cho bản nộp.

Nguồn: `docs/vn-heritage-results.md`, `data/processed/vn_heritage_core/`, `docs/wandb-report/70*`–`73*`.

## 8. Demo trực tiếp và video dự phòng

- [x] Có code UI/notebook và kịch bản demo dưới 5 phút trong README.
- [ ] Video dự phòng ≤5 phút được nhóm kiểm và bàn giao.
- [ ] Thử mở lại bằng môi trường/gói artifact trên máy vấn đáp.

## Phần mở rộng tùy chọn

- [x] Query-adaptive alpha của Phú có code/config và 27 kiểm thử, đã tích hợp.
- [ ] Chạy và báo kết quả trên cả hai tập công khai, gồm random control; chưa nhận hoàn thành cấp độ 4 hoặc có cải thiện.
- [ ] Backbone thứ hai, hub ablation và matched-parameter direction ablation: chưa có; không phải các mục đã nghiệm thu.

## Kết luận nghiệm thu

Code cốt lõi, MMKG remote, dữ liệu/split, cấu hình ablation, UI và notebook đã có.
Các sản phẩm còn chặn bộ nộp hoàn chỉnh: báo cáo cuối + slide, video, gói artifact
và kiểm tay theo rubric. Không cần chốt lại số liệu bằng cách train/tune theo test;
cần gắn mỗi bảng/case với đúng nguồn chạy đã có.
