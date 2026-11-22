# Phân công và bàn giao bài nộp

Cập nhật: 22/11/2026. Bảng này là trách nhiệm hoàn thiện đã chốt của nhóm,
không dùng để suy ngược tác giả lịch sử từ số commit. Task chung có đúng hai người;
các task riêng do một người chịu trách nhiệm nghiệm thu.

## Việc riêng

| ID | Người phụ trách | Đầu vào | Đầu ra / bằng chứng hiện có | Nghiệm thu và phần còn lại |
|---|---|---|---|---|
| R1 | Nghị | Split/cache cố định; full và bốn biến thể | `src/models/ablations.py`, `configs/retrieval/ablations/`, bảng hai dataset trong README | Đã có code, cấu hình và summary ba seed cho VG–COCO và MKG-W caption subset. Kiểm tra nguồn của từng bảng khi đưa vào bản PDF cuối; không đổi tham số theo test. |
| R2 | Trường Thịnh | VG–COCO, CLIP frozen, GraphSAGE | `src/models/`, `runs/benchmark/`, script dựng và audit VG–COCO | Pipeline có kiểm thử và audit metadata. Bàn giao thêm ảnh/cache/checkpoint ngoài Git; tách lượt 18/11 với 21/11 và biến thể CLIP-image. |
| R3 | Phú | Checkpoint cố định, fidelity/random control và các ca đã phân tích | `src/evaluation/`, `reports/explanation-quality/`, 5 ca thành công + 5 ca thất bại trong README | Có fidelity/sparsity, có 10 ca; validity hiện là pilot AI 20 query/42 relation. Còn người chấm theo rubric cố định và gói trace/ảnh cho các ca của lượt 21/11. |
| R4 | Quốc Thịnh | Các gói R1–R3, C1–C2; nguồn bảng và hình | Báo cáo Prism, tài liệu hướng dẫn `docs/`, bảng kết quả `table.md` | Prism đã sửa phương pháp đợt 1; còn abstract/tác giả, XAI/MMKG, thống nhất nguồn bảng và đủ 12–18 trang. Slide chưa có. |

## Việc chung

| ID | Đúng hai người | Phần của từng người | Bằng chứng hiện có | Điều kiện bàn giao |
|---|---|---|---|---|
| C1 | Trường Thịnh + Phú | Trường Thịnh: AdaMF-MAT/adaptation, loss, checkpoint, bảng mô hình. Phú: MKG-W, query trực tiếp/gián tiếp, split và kiểm oracle input. | `docs/mkg-w-results.md`, `docs/mkg-w-captions-results.md`, bộ query và code trong repo | Đã có code và kết quả. Khi viết báo cáo phải tách caption text-only với KG được cho anchor/relation; không trình bày như so sánh cùng input. |
| C2 | Nghị + Phú | Nghị: nguồn/license, linking, triple, data card và split. Phú: transfer, gallery ảnh/địa điểm, ablation và phân tích lỗi. | `data/processed/vn_heritage_core/`, `docs/vn-heritage-results.md` | Chỉ dùng MMKG trên remote: 160 địa điểm, 772 ảnh, 849 thực thể, 981 claim + 902 cạnh bài viết. Còn kiểm tay mẫu và đóng gói ảnh/license; không lấy bộ MMKG local cũ thay vào. |
| C3 | Trường Thịnh + Quốc Thịnh | Trường Thịnh: code/runtime, model/cache, top-k và relation. Quốc Thịnh: kịch bản, quay/biên tập video, đối chiếu slide. | `scripts/run_demo.py`, `src/demo/`, `notebooks/retrieval_demo.ipynb`, hướng dẫn README | UI/notebook đã chạy trên model thật; có video dự phòng ~1:30 có phụ đề, không lời đọc (`reports/demo/retrieval-demo.mp4`). Còn nhóm duyệt video và nghiệm thu ở máy trình bày. |

## Tài khoản Git và cách ghi đóng góp

- Nghị: `nghidt`, email commit đã cấu hình `nhokcrboy@gmail.com`.
- Phú: `dacphu`, email lấy từ commit remote `pldppldp123@gmail.com`.
- Trường Thịnh: `thinhnt3`, theo xác nhận mới nhất của nhóm; email commit remote `thinhnt3@vng.com.vn`.
- Quốc Thịnh: phụ trách R4 và cùng làm C3; chưa có tài khoản/email Git được xác nhận.

Giữ author gốc của commit đã chia sẻ. Tên người bấm merge chỉ nói ai tích hợp,
không nói người đó làm hết nội dung. Khi hai người thực sự cùng tạo một thay đổi,
commit có thể có một author và `Co-authored-by` sau khi xác nhận danh tính người còn lại.
Không đổi author của code cũ chỉ để chia đều số commit theo bảng phân công.

Phần demo/notebook, bổ sung CLI dựng/audit và biên tập tích hợp ngày 22/11 được
chuẩn bị với trợ lý AI trong phiên làm việc của Nghị. Người phụ trách trong bảng
chịu trách nhiệm đọc, chạy lại, hiểu và nghiệm thu trước khi nộp; bảng không khẳng
định họ đã tự viết toàn bộ phần được giao. Không dùng số commit làm tỷ lệ đóng góp.

## Thứ tự hoàn tất

1. Tích hợp tài liệu Phú → query-adaptive alpha tùy chọn → cấu hình ablation dataset 2 → demo/notebook → panel W&B dataset 2.
2. Chạy test/lint/type, audit metadata và chạy demo/notebook trên bản tích hợp. Query-adaptive alpha chưa có số liệu, chưa nhận hoàn thành cấp độ 4.
3. Chốt gói artifact ngoài Git, kiểm validity, hoàn thiện Prism và slide theo gói kỹ thuật đã bàn giao.
4. Duyệt video dự phòng đã chuẩn bị (có thể bổ sung lời đọc), chạy thử trên máy vấn đáp. Không đánh dấu cả bài hoàn thành trước khi đủ các sản phẩm này.

Trạng thái theo sản phẩm: [requirements-checklist.md](plan-task/requirements-checklist.md).
