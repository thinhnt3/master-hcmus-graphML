# Phân công đồ án

Bảng ghi người phụ trách và đầu ra của từng phần. [Checklist theo yêu cầu của đề](plan-task/requirements-checklist.md)

## Việc riêng

| Người phụ trách | Phần việc | Sản phẩm và trạng thái |
| --- | --- | --- |
| Nguyễn Trường Thịnh | Dựng và huấn luyện CLIP–GraphSAGE trên VG–COCO. | Mã trong `src/models/`, benchmark và gói demo. |
| Đỗ Thanh Nghị | Đánh giá ablation trên hai tập. Giữ cố định split và cache khi so sánh các biến thể. | `configs/retrieval/ablations/` và bảng ablation trong báo cáo. |
| Phan Lê Đắc Phú | Đánh giá giải thích bằng fidelity, sparsity và validity. Phân tích 5 ca tăng hạng và 5 ca giảm hạng. | `reports/explanation-quality/`, báo cáo và phụ lục. Validity hiện có nhãn thí điểm của AI. |
| Trần Quốc Thịnh | Tổng hợp báo cáo, phụ trách slide và viết script xuất bảng so sánh CLIP với CLIP + GraphSAGE từ JSON benchmark VG–COCO. | Có báo cáo và slide. Đầu ra cần bổ sung là script và bảng Markdown sinh từ số liệu gốc. |

Script của Quốc Thịnh đọc `clip.test` và `reranked.test` trong `runs/benchmark/graphsage-directed-learned-l3-h512.json`, đổi đơn vị sang phần trăm và xuất R@1, R@5, R@10, MRR. Dòng GraphSAGE giữ trung bình và độ lệch chuẩn qua ba seed.

## Việc theo cặp

| Thành viên | Phần việc | Đầu ra |
| --- | --- | --- |
| Trường Thịnh và Phú | Trường Thịnh phụ trách thích nghi AdaMF–MAT và huấn luyện. Phú phụ trách split, truy vấn trực tiếp/gián tiếp và kiểm thông tin được cấp sẵn cho MKG-W. | Hai quy trình đánh giá trong `docs/mkg-w-results.md` và `docs/mkg-w-captions-results.md`. |
| Nghị và Phú | Nghị phụ trách nguồn, giấy phép, liên kết thực thể và dựng triple VN Heritage. Phú phụ trách đánh giá chuyển giao và so sánh gallery theo ảnh với theo địa điểm. | `docs/vn-heritage-data-card.md`, `data/processed/vn_heritage_core/` và `docs/vn-heritage-results.md`. |
| Trường Thịnh và Quốc Thịnh | Trường Thịnh phụ trách giao diện, notebook và hiển thị quan hệ. Quốc Thịnh phụ trách kịch bản trình bày và chuẩn bị video dự phòng. | `scripts/run_demo.py`, `notebooks/retrieval_demo.ipynb` và `reports/demo/retrieval-demo.mp4`. |

## Việc cả nhóm

Cả nhóm chạy thử từ thư mục mới giải nén và kiểm tra lại demo trên máy sẽ dùng khi vấn đáp. Với gói dữ liệu của nhóm, lệnh kiểm nhận đủ 1.500 ảnh và truy vấn `coco-224024` đưa ảnh VG 2355841 từ hạng 26 lên hạng 1.

## Tài khoản Git

Nguyễn Trường Thịnh dùng `thinhnt`, Đỗ Thanh Nghị dùng `nghidt`, Phan Lê Đắc Phú dùng `dacphu` và Trần Quốc Thịnh dùng `thinhnt3`. Giữ tác giả gốc của các commit đã chia sẻ. Ghi đồng tác giả cho thay đổi thực sự làm chung, sau khi xác nhận với người đó.

Nhóm khai báo hỗ trợ AI trong báo cáo kỹ thuật, gồm phần biên tập, kiểm thử demo/CLI và lượt chấm thí điểm validity.
