# Bảng cho báo cáo

Tập bảng đề xuất cho báo cáo, xếp theo thứ tự trình bày. Mỗi bảng có bản Markdown để đọc nhanh, caption, một câu kết luận, và mã LaTeX theo đúng kiểu bảng đang dùng trong `main.tex` (IEEEtran, caption đặt trên bảng, kẻ `\hline` từng dòng). Số liệu lấy từ các file kết quả và tài liệu trong repo; nguồn ghi dưới mỗi bảng.

## Đối chiếu với báo cáo hiện tại

Báo cáo hiện có 11 bảng (I đến XI), đủ cho nhiệm vụ 2 nhưng thiếu ablation của nhiệm vụ 1 và toàn bộ nhiệm vụ 3.

| Bảng hiện tại | Nội dung | Xử lý | Bảng tương ứng ở đây |
|---|---|---|---|
| I | Số ảnh và truy vấn của VG ∩ COCO | Sửa: mở rộng thành bảng ba bộ dữ liệu | [Bảng 1](#bảng-1-thống-kê-ba-bộ-dữ-liệu) |
| II | Kết quả mức 1 | Sửa: số 48,20 lệch với 48,12 ở Bảng III; thiếu độ lệch chuẩn; in đậm 48,20 trong khi dòng dưới 49,43 cao hơn | [Bảng 3](#bảng-3-kết-quả-chính-mức-1) |
| III | Kết quả chính mức 2 trên hai tập | Giữ | [Bảng 8](#bảng-8-kết-quả-chính-mức-2-trên-hai-tập) |
| IV | Trực tiếp và gián tiếp trên MKG-W, 3 phương pháp | Gộp với Bảng X | [Bảng 9](#bảng-9-truy-vấn-trực-tiếp-và-gián-tiếp-trên-mkg-w) |
| V | Biến thể ngoài ba mô hình chính | Giữ | [Bảng 11](#bảng-11-các-biến-thể-ngoài-ba-mô-hình-chính) |
| VI | Thành phần của AdaMF-MAT | Giữ | [Bảng 12](#bảng-12-thành-phần-của-adamf-mat) |
| VII | Ablation modality trên MKG-W caption subset | Giữ | [Bảng 13](#bảng-13-ablation-modality-trên-mkg-w-caption-subset) |
| VIII | Relation queries và che cạnh | Giữ | [Bảng 14](#bảng-14-mô-hình-có-đọc-cạnh-không-che-cạnh-được-hỏi) |
| IX | Truy vấn gián tiếp qua IsA | Chuyển xuống phụ lục: kết quả âm, không trả lời yêu cầu nào trực tiếp | [Bảng 24](#bảng-24-truy-vấn-gián-tiếp-qua-khái-niệm-cha-isa) |
| X | Các phương pháp khác trên MKG-W | Gộp vào bảng trực tiếp và gián tiếp; hai dòng xáo cạnh sang bảng ablation cạnh | [Bảng 9](#bảng-9-truy-vấn-trực-tiếp-và-gián-tiếp-trên-mkg-w) |
| XI | Hai bộ kiểm tra thêm | Sửa: thêm số câu | [Bảng 16](#bảng-16-hai-bộ-truy-vấn-chỉ-dùng-để-đánh-giá) |

## Danh sách bảng theo yêu cầu của đề

Mỗi bảng gắn với một yêu cầu của đề; bảng nào không trả lời yêu cầu nào thì không đưa vào.

| Bảng | Phần | Yêu cầu của đề | So với báo cáo hiện tại |
|---|---|---|---|
| [Bảng 1](#bảng-1-thống-kê-ba-bộ-dữ-liệu): Thống kê ba bộ dữ liệu | Dữ liệu và thiết lập | Mức 2: ít nhất 2 tập công khai. Mức 3: MMKG tự xây. Chung: nộp cách chia | Sửa Bảng I (hiện chỉ có VG ∩ COCO) |
| [Bảng 2](#bảng-2-thiết-lập-thực-nghiệm): Thiết lập thực nghiệm | Dữ liệu và thiết lập | Chung: α và siêu tham số chọn trên validation, tối thiểu 3 seed | Thêm mới |
| [Bảng 3](#bảng-3-kết-quả-chính-mức-1): Kết quả chính mức 1 | Nhiệm vụ 1 | Mức 1: so sánh CLIP với CLIP + đồ thị trên cùng cách chia | Sửa Bảng II: dùng lượt 48,12 ± 0,23 cho khớp Bảng III, thêm độ lệch chuẩn và cột điểm đồ thị, sửa chỗ in đậm |
| [Bảng 4](#bảng-4-ablation-cấu-trúc-đồ-thị-huấn-luyện-lại): Ablation cấu trúc đồ thị (huấn luyện lại) | Nhiệm vụ 1 | Mức 1: bỏ cạnh hoặc thay bằng cạnh ngẫu nhiên | Thêm mới |
| [Bảng 5](#bảng-5-chênh-lệch-ghép-cặp-của-ablation): Chênh lệch ghép cặp của ablation | Nhiệm vụ 1 | Mức 1: chứng minh cải thiện đến từ cấu trúc quan hệ | Thêm mới |
| [Bảng 6](#bảng-6-xoá-cạnh-xoá-đỉnh-đổi-nhãn-lúc-test): Xoá cạnh, xoá đỉnh, đổi nhãn lúc test | Nhiệm vụ 1 | Mức 1 và 2: ablation xoá cạnh, xoá đỉnh | Thêm mới |
| [Bảng 7](#bảng-7-5-truy-vấn-thành-công-5-thất-bại): 5 truy vấn thành công, 5 thất bại | Nhiệm vụ 1 | Mức 1: hiển thị quan hệ đã dùng; phân tích 5 thành công và 5 thất bại | Thêm mới |
| [Bảng 8](#bảng-8-kết-quả-chính-mức-2-trên-hai-tập): Kết quả chính mức 2 trên hai tập | Nhiệm vụ 2 | Mức 2: phương pháp từ 2024 trên cùng pipeline, ít nhất 2 tập công khai | Giữ Bảng III |
| [Bảng 9](#bảng-9-truy-vấn-trực-tiếp-và-gián-tiếp-trên-mkg-w): Truy vấn trực tiếp và gián tiếp trên MKG-W | Nhiệm vụ 2 | Mức 2: bộ truy vấn có nhóm gián tiếp cần khai thác quan hệ, báo cáo tách hai nhóm | Gộp Bảng IV và Bảng X (bỏ hai dòng xáo cạnh, chuyển sang bảng ablation cạnh) |
| [Bảng 10](#bảng-10-tái-lập-adamf-mat-trên-bài-toán-gốc): Tái lập AdaMF-MAT trên bài toán gốc | Nhiệm vụ 2 | Mức 2: triển khai hoặc tái lập một phương pháp từ 2024 | Thêm mới |
| [Bảng 11](#bảng-11-các-biến-thể-ngoài-ba-mô-hình-chính): Các biến thể ngoài ba mô hình chính | Nhiệm vụ 2 | Mức 2: tách đóng góp của đồ thị khỏi nhánh ảnh | Giữ Bảng V |
| [Bảng 12](#bảng-12-thành-phần-của-adamf-mat): Thành phần của AdaMF-MAT | Nhiệm vụ 2 | Mức 2: ablation của phương pháp | Giữ Bảng VI |
| [Bảng 13](#bảng-13-ablation-modality-trên-mkg-w-caption-subset): Ablation modality trên MKG-W caption subset | Nhiệm vụ 2 | Mức 2: ablation của phương pháp trên tập thứ hai | Giữ Bảng VII |
| [Bảng 14](#bảng-14-mô-hình-có-đọc-cạnh-không-che-cạnh-được-hỏi): Mô hình có đọc cạnh không: che cạnh được hỏi | Nhiệm vụ 2 | Mức 2: xoá cạnh; truy vấn cần khai thác quan hệ | Giữ Bảng VIII |
| [Bảng 15](#bảng-15-ablation-cạnh-trên-mkg-w): Ablation cạnh trên MKG-W | Nhiệm vụ 2 | Mức 1 và 2: bỏ cạnh hoặc cạnh ngẫu nhiên, trên tập thứ hai | Thêm mới (thay hai dòng “xáo cạnh” của Bảng X) |
| [Bảng 16](#bảng-16-hai-bộ-truy-vấn-chỉ-dùng-để-đánh-giá): Hai bộ truy vấn chỉ dùng để đánh giá | Nhiệm vụ 2 | Mức 2: bộ tối thiểu 20 truy vấn chỉ để đánh giá | Sửa Bảng XI: thêm số câu |
| [Bảng 17](#bảng-17-fidelity-và-sparsity): Fidelity và sparsity | Nhiệm vụ 3 | Mức 3: fidelity và sparsity định lượng | Thêm mới |
| [Bảng 18](#bảng-18-validity): Validity | Nhiệm vụ 3 | Mức 3: validity định lượng | Thêm mới |
| [Bảng 19](#bảng-19-bằng-chứng-trên-10-truy-vấn): Bằng chứng trên 10 truy vấn | Nhiệm vụ 3 | Mức 3: bằng chứng cụ thể cho tối thiểu 10 truy vấn | Thêm mới |
| [Bảng 20](#bảng-20-vn-heritage-thẻ-dữ-liệu): VN Heritage: thẻ dữ liệu | Nhiệm vụ 3 | Mức 3: MMKG tự xây, mô tả nguồn và cách liên kết ảnh với thực thể | Thêm mới |
| [Bảng 21](#bảng-21-vn-heritage-kết-quả): VN Heritage: kết quả | Nhiệm vụ 3 | Mức 3: chạy phương pháp của mức 1/2 trên MMKG tự xây; tách trực tiếp và gián tiếp | Thêm mới |
| [Bảng 22](#bảng-22-vn-heritage-ablation-cạnh): VN Heritage: ablation cạnh | Nhiệm vụ 3 | Mức 1 trên MMKG tự xây: bỏ cạnh hoặc cạnh ngẫu nhiên | Thêm mới |
| [Bảng 23](#bảng-23-vn-heritage-adamf-mat): VN Heritage: AdaMF-MAT | Nhiệm vụ 3 | Mức 3: chạy phương pháp tốt nhất của mức 2 trên MMKG tự xây | Thêm mới |
| [Bảng 24](#bảng-24-truy-vấn-gián-tiếp-qua-khái-niệm-cha-isa): Truy vấn gián tiếp qua khái niệm cha (IsA) | Phụ lục | Mức 2: nhóm truy vấn gián tiếp trên VG ∩ COCO | Bảng IX: chuyển xuống phụ lục |

Gói LaTeX cần có: `tabularx`, `multirow` (đã có trong `main.tex`). Bảng rộng dùng `table*`.

## Dữ liệu và thiết lập

### Bảng 1: Thống kê ba bộ dữ liệu

**Caption.** Thống kê các bộ dữ liệu. Ba số trong một ô là train / validation / test.

| Bộ dữ liệu | Gallery | Truy vấn | Đồ thị |
|---|---|---|---|
| VG ∩ COCO (công khai) | 7.000 / 1.500 / 1.500 ảnh | 35.000 / 7.500 / 7.500 caption | đồ thị cảnh riêng từng ảnh; 1.778 khái niệm, 493 vị từ |
| MKG-W caption subset (công khai) | 2.055 / 440 / 441 mục | 4.110 / 880 / 882 caption | triple Wikidata quanh từng mục; 11.153 khái niệm, 144 vị từ |
| MKG-W, bài toán đồ thị tri thức (công khai) | 9.301 thực thể có ảnh | trực tiếp 12.672 / 2.711 / 2.710; gián tiếp 14.441 / 2.462 / 2.444 | 15.000 thực thể, 169 quan hệ; 34.196 / 4.276 / 4.274 triple |
| VN Heritage (tự xây) | 160 địa điểm (97 / 22 / 41), 772 ảnh | trực tiếp: tên địa điểm; gián tiếp: khoảng 145 câu test mỗi cách chia | 849 thực thể, 981 claim Wikidata (18 quan hệ) |

MKG-W được dùng dưới hai dạng: tập con dựng theo khuôn VG ∩ COCO để chạy lại nguyên pipeline, và bài toán đồ thị tri thức có truy vấn gián tiếp.

Nguồn: `data/splits/*.yaml`, `docs/mkg-w-results.md`, `docs/vn-heritage-results.md`.

```latex
\begin{table*}[t]
  \centering
  \caption{Thống kê các bộ dữ liệu. Ba số trong một ô là train / validation / test}
  \label{tab:data}
  \footnotesize
  \setlength{\tabcolsep}{3pt}
  \begin{tabularx}{\textwidth}{|l|X|X|X|}
    \hline
    Bộ dữ liệu & Gallery & Truy vấn & Đồ thị \\
    \hline
    VG $\cap$ COCO (công khai) & 7.000 / 1.500 / 1.500 ảnh & 35.000 / 7.500 / 7.500 caption & đồ thị cảnh riêng từng ảnh; 1.778 khái niệm, 493 vị từ \\
    \hline
    MKG-W caption subset (công khai) & 2.055 / 440 / 441 mục & 4.110 / 880 / 882 caption & triple Wikidata quanh từng mục; 11.153 khái niệm, 144 vị từ \\
    \hline
    MKG-W, bài toán đồ thị tri thức (công khai) & 9.301 thực thể có ảnh & trực tiếp 12.672 / 2.711 / 2.710; gián tiếp 14.441 / 2.462 / 2.444 & 15.000 thực thể, 169 quan hệ; 34.196 / 4.276 / 4.274 triple \\
    \hline
    VN Heritage (tự xây) & 160 địa điểm (97 / 22 / 41), 772 ảnh & trực tiếp: tên địa điểm; gián tiếp: khoảng 145 câu test mỗi cách chia & 849 thực thể, 981 claim Wikidata (18 quan hệ) \\
    \hline
  \end{tabularx}
\end{table*}
```

### Bảng 2: Thiết lập thực nghiệm

**Caption.** Thiết lập dùng chung cho mọi thí nghiệm, trừ khi bảng ghi khác.

| Thành phần | Giá trị |
|---|---|
| CLIP | ViT-B/32, đóng băng |
| GraphSAGE | 3 tầng, 512 chiều ẩn, có hướng |
| AdaMF-MAT | 256 chiều, μ = 1, nhiễu 64 chiều |
| Huấn luyện | InfoNCE, τ = 0,07; batch 256; lr 0,001; weight decay 0,0001 |
| Dừng sớm | tối đa 50 epoch, patience 5, chọn epoch theo R@1 validation |
| Seed | 13, 37, 97; bảng ghi 5 seed thêm 211, 307 |
| α | lưới bước 0,01, chọn trên validation |
| k | chọn trên validation, một trong 10, 20, 50, 100, 200, 500, 1.500 |

Tập test chỉ được chấm sau khi α và k đã chốt trên validation.

Nguồn: `configs/retrieval/vg_coco.yaml`.

```latex
\begin{table}[t]
  \centering
  \caption{Thiết lập dùng chung cho mọi thí nghiệm, trừ khi bảng ghi khác}
  \label{tab:setup}
  \footnotesize
  \setlength{\tabcolsep}{3pt}
  \begin{tabularx}{\columnwidth}{|l|X|}
    \hline
    Thành phần & Giá trị \\
    \hline
    CLIP & ViT-B/32, đóng băng \\
    \hline
    GraphSAGE & 3 tầng, 512 chiều ẩn, có hướng \\
    \hline
    AdaMF-MAT & 256 chiều, $\mu$ = 1, nhiễu 64 chiều \\
    \hline
    Huấn luyện & InfoNCE, $\tau$ = 0,07; batch 256; lr 0,001; weight decay 0,0001 \\
    \hline
    Dừng sớm & tối đa 50 epoch, patience 5, chọn epoch theo R@1 validation \\
    \hline
    Seed & 13, 37, 97; bảng ghi 5 seed thêm 211, 307 \\
    \hline
    $\alpha$ & lưới bước 0,01, chọn trên validation \\
    \hline
    k & chọn trên validation, một trong 10, 20, 50, 100, 200, 500, 1.500 \\
    \hline
  \end{tabularx}
\end{table}
```

## Nhiệm vụ 1

### Bảng 3: Kết quả chính mức 1

**Caption.** Truy hồi ảnh theo caption trên tập test của VG ∩ COCO (%). Trung bình ± độ lệch chuẩn qua 3 seed. Cột cuối là R@1 khi chỉ dùng điểm đồ thị, không cộng CLIP.

| Phương pháp | R@1 | R@5 | R@10 | MRR | Chỉ đồ thị, R@1 |
|---|---|---|---|---|---|
| CLIP ViT-B/32 | 43,89 | 72,19 | 82,64 | 56,76 | – |
| CLIP + so khớp từ với đồ thị | 46,41 | 74,80 | 85,41 | 59,29 | 12,63 |
| CLIP + GraphSAGE (đỉnh ảnh học được) | 48,12 ± 0,23 | 75,33 ± 0,65 | 83,87 ± 2,12 | 60,42 ± 0,44 | 27,54 ± 0,50 |
| CLIP + GraphSAGE (đỉnh ảnh mang CLIP) | **49,43 ± 0,46** | **77,90 ± 0,47** | **87,52 ± 0,69** | **62,22 ± 0,37** | 42,25 ± 0,48 |

GraphSAGE nâng R@1 của CLIP thêm 4,2 điểm. Bản đỉnh ảnh học được là mô hình chính vì điểm đồ thị của nó không lẫn thông tin CLIP của ảnh.

Nguồn: `runs/benchmark/*.json` (lượt 18/11).

```latex
\begin{table*}[t]
  \centering
  \caption{Truy hồi ảnh theo caption trên tập test của VG $\cap$ COCO (\%). Trung bình $\pm$ độ lệch chuẩn qua 3 seed. Cột cuối là R@1 khi chỉ dùng điểm đồ thị, không cộng CLIP}
  \label{tab:t1-results}
  \footnotesize
  \setlength{\tabcolsep}{3pt}
  \begin{tabular}{|l|c|c|c|c|c|}
    \hline
    Phương pháp & R@1 & R@5 & R@10 & MRR & Chỉ đồ thị, R@1 \\
    \hline
    CLIP ViT-B/32 & 43,89 & 72,19 & 82,64 & 56,76 & -- \\
    \hline
    CLIP + so khớp từ với đồ thị & 46,41 & 74,80 & 85,41 & 59,29 & 12,63 \\
    \hline
    CLIP + GraphSAGE (đỉnh ảnh học được) & 48,12 $\pm$ 0,23 & 75,33 $\pm$ 0,65 & 83,87 $\pm$ 2,12 & 60,42 $\pm$ 0,44 & 27,54 $\pm$ 0,50 \\
    \hline
    CLIP + GraphSAGE (đỉnh ảnh mang CLIP) & \textbf{49,43 $\pm$ 0,46} & \textbf{77,90 $\pm$ 0,47} & \textbf{87,52 $\pm$ 0,69} & \textbf{62,22 $\pm$ 0,37} & 42,25 $\pm$ 0,48 \\
    \hline
  \end{tabular}
\end{table*}
```

### Bảng 4: Ablation cấu trúc đồ thị (huấn luyện lại)

**Caption.** Ablation cấu trúc đồ thị của GraphSAGE trên hai tập công khai: R@1 trên test (%), 3 seed. Mỗi biến thể được huấn luyện lại, α và k chọn riêng trên validation.

| Biến thể | Sau xếp hạng lại | Chỉ đồ thị | Sau xếp hạng lại | Chỉ đồ thị |
|---|---|---|---|---|
| CLIP (không đồ thị) | 43,89 | – | 35,60 | – |
| Đầy đủ | **48,12 ± 0,23** | 27,54 ± 0,50 | **43,35 ± 0,54** | **28,19 ± 1,08** |
| Bỏ cạnh, chỉ giữ vật thể | 47,56 ± 0,16 | 26,16 ± 0,45 | 40,67 ± 1,25 | 21,01 ± 0,58 |
| Cạnh ngẫu nhiên | 47,79 ± 0,18 | 27,38 ± 0,26 | 42,67 ± 0,47 | 26,95 ± 0,91 |
| Bỏ nhãn vị từ | 48,06 ± 0,28 | 27,35 ± 0,49 | 41,42 ± 0,66 | 22,52 ± 1,18 |
| Không hướng | 47,84 ± 0,15 | **28,16 ± 0,58** | 42,25 ± 0,56 | 27,10 ± 1,93 |

Trên VG ∩ COCO, bỏ hết cạnh chỉ mất 0,56 điểm trong 4,2 điểm tăng: phần lớn đến từ danh sách vật thể. Trên MKG-W caption subset, cạnh và nhãn vị từ đóng góp rõ hơn (mất 2,68 và 1,93 điểm).

Nhóm cột trong bản LaTeX: VG ∩ COCO (2 cột); MKG-W caption subset (2 cột).

Nguồn: `runs/benchmark/*.json`; dataset 2 chạy ngày 21/11.

```latex
\begin{table*}[t]
  \centering
  \caption{Ablation cấu trúc đồ thị của GraphSAGE trên hai tập công khai: R@1 trên test (\%), 3 seed. Mỗi biến thể được huấn luyện lại, $\alpha$ và k chọn riêng trên validation}
  \label{tab:t1-ablation}
  \footnotesize
  \setlength{\tabcolsep}{3pt}
  \begin{tabular}{|l|c|c|c|c|}
    \hline
    \multirow{2}{*}{Biến thể} & \multicolumn{2}{c|}{VG $\cap$ COCO} & \multicolumn{2}{c|}{MKG-W caption subset} \\
    \cline{2-3} \cline{4-5}
     & Sau xếp hạng lại & Chỉ đồ thị & Sau xếp hạng lại & Chỉ đồ thị \\
    \hline
    CLIP (không đồ thị) & 43,89 & -- & 35,60 & -- \\
    \hline
    Đầy đủ & \textbf{48,12 $\pm$ 0,23} & 27,54 $\pm$ 0,50 & \textbf{43,35 $\pm$ 0,54} & \textbf{28,19 $\pm$ 1,08} \\
    \hline
    Bỏ cạnh, chỉ giữ vật thể & 47,56 $\pm$ 0,16 & 26,16 $\pm$ 0,45 & 40,67 $\pm$ 1,25 & 21,01 $\pm$ 0,58 \\
    \hline
    Cạnh ngẫu nhiên & 47,79 $\pm$ 0,18 & 27,38 $\pm$ 0,26 & 42,67 $\pm$ 0,47 & 26,95 $\pm$ 0,91 \\
    \hline
    Bỏ nhãn vị từ & 48,06 $\pm$ 0,28 & 27,35 $\pm$ 0,49 & 41,42 $\pm$ 0,66 & 22,52 $\pm$ 1,18 \\
    \hline
    Không hướng & 47,84 $\pm$ 0,15 & \textbf{28,16 $\pm$ 0,58} & 42,25 $\pm$ 0,56 & 27,10 $\pm$ 1,93 \\
    \hline
  \end{tabular}
\end{table*}
```

### Bảng 5: Chênh lệch ghép cặp của ablation

**Caption.** Bản đầy đủ trừ biến thể, điểm % R@1 sau xếp hạng lại, kèm khoảng tin cậy 95% (bootstrap ghép cặp, gom caption theo ảnh đúng). Khoảng không chứa 0 được in đậm.

| Biến thể | VG ∩ COCO | MKG-W caption subset |
|---|---|---|
| Bỏ cạnh | **0,56 [0,05; 1,06]** | **2,68 [1,06; 4,35]** |
| Cạnh ngẫu nhiên | 0,33 [−0,09; 0,74] | 0,68 [−0,45; 1,81] |
| Bỏ nhãn vị từ | 0,05 [−0,35; 0,45] | **1,93 [0,38; 3,36]** |
| Không hướng | – | 1,10 [−0,11; 2,34] |

Chỉ phép bỏ cạnh tách được khỏi bản đầy đủ trên cả hai tập. Cạnh ngẫu nhiên giữ nguyên vật thể, số cạnh và nhãn vị từ, nên chưa tách được.

Nguồn: `docs/graphsage-design-decisions.md`; `runs/mkg_w_captions/analysis/ablation.json`.

```latex
\begin{table}[t]
  \centering
  \caption{Bản đầy đủ trừ biến thể, điểm \% R@1 sau xếp hạng lại, kèm khoảng tin cậy 95\% (bootstrap ghép cặp, gom caption theo ảnh đúng). Khoảng không chứa 0 được in đậm}
  \label{tab:t1-ablation-ci}
  \footnotesize
  \setlength{\tabcolsep}{3pt}
  \begin{tabular}{|l|c|c|}
    \hline
    Biến thể & VG $\cap$ COCO & MKG-W caption subset \\
    \hline
    Bỏ cạnh & \textbf{0,56 [0,05; 1,06]} & \textbf{2,68 [1,06; 4,35]} \\
    \hline
    Cạnh ngẫu nhiên & 0,33 [$-$0,09; 0,74] & 0,68 [$-$0,45; 1,81] \\
    \hline
    Bỏ nhãn vị từ & 0,05 [$-$0,35; 0,45] & \textbf{1,93 [0,38; 3,36]} \\
    \hline
    Không hướng & -- & 1,10 [$-$0,11; 2,34] \\
    \hline
  \end{tabular}
\end{table}
```

### Bảng 6: Xoá cạnh, xoá đỉnh, đổi nhãn lúc test

**Caption.** Làm hỏng đồ thị của ảnh test rồi chấm lại, không huấn luyện lại: R@1 trên VG ∩ COCO (%), 3 seed. Mỗi phép làm hỏng áp dụng với xác suất ghi trong ngoặc; α và k giữ từ validation sạch.

| Đồ thị test | Sau xếp hạng lại | Chỉ đồ thị | Sau xếp hạng lại | Chỉ đồ thị | Sau xếp hạng lại | Chỉ mô hình |
|---|---|---|---|---|---|---|
| Nguyên vẹn | 48,20 ± 0,05 | 27,78 ± 0,63 | 49,43 ± 0,46 | 42,25 ± 0,48 | 51,42 ± 0,32 | 48,48 ± 0,36 |
| Xoá cạnh (30%) | 47,65 ± 0,04 | 26,46 ± 0,21 | 49,36 ± 0,41 | 42,26 ± 0,31 | 51,43 ± 0,31 | 48,51 ± 0,38 |
| Xoá cạnh (50%) | 47,31 ± 0,26 | 25,86 ± 0,07 | 49,29 ± 0,35 | 42,36 ± 0,34 | 51,43 ± 0,32 | 48,52 ± 0,40 |
| Xoá đỉnh vật thể (30%) | 43,77 ± 0,23 | 20,13 ± 0,53 | 49,21 ± 0,37 | 41,95 ± 0,28 | 50,97 ± 0,22 | 46,92 ± 0,38 |
| Đổi nhãn vật thể (20%) | 43,43 ± 0,39 | 20,08 ± 0,35 | 49,03 ± 0,45 | 41,60 ± 0,42 | 50,82 ± 0,27 | 47,24 ± 0,43 |

Xoá đỉnh làm GraphSAGE mức 1 mất 4,4 điểm, xoá một nửa số cạnh chỉ mất 0,9 điểm: mô hình dựa vào vật thể nhiều hơn quan hệ. AdaMF-MAT và bản đỉnh ảnh mang CLIP gần như không đổi khi xoá cạnh, vì nhánh ảnh đã đủ.

Nhóm cột trong bản LaTeX: GraphSAGE (đỉnh ảnh học được) (2 cột); GraphSAGE (đỉnh ảnh mang CLIP) (2 cột); AdaMF-MAT (2 cột).

Nguồn: `scripts/eval_graph_noise.py`; cột đầu chạy ngày 21/11 trên mô hình huấn luyện lại (trùng lượt 17/11: 48,20 ± 0,05).

```latex
\begin{table*}[t]
  \centering
  \caption{Làm hỏng đồ thị của ảnh test rồi chấm lại, không huấn luyện lại: R@1 trên VG $\cap$ COCO (\%), 3 seed. Mỗi phép làm hỏng áp dụng với xác suất ghi trong ngoặc; $\alpha$ và k giữ từ validation sạch}
  \label{tab:noise}
  \scriptsize
  \setlength{\tabcolsep}{3pt}
  \begin{tabular}{|l|c|c|c|c|c|c|}
    \hline
    \multirow{2}{*}{Đồ thị test} & \multicolumn{2}{c|}{GraphSAGE (đỉnh ảnh học được)} & \multicolumn{2}{c|}{GraphSAGE (đỉnh ảnh mang CLIP)} & \multicolumn{2}{c|}{AdaMF-MAT} \\
    \cline{2-3} \cline{4-5} \cline{6-7}
     & Sau xếp hạng lại & Chỉ đồ thị & Sau xếp hạng lại & Chỉ đồ thị & Sau xếp hạng lại & Chỉ mô hình \\
    \hline
    Nguyên vẹn & 48,20 $\pm$ 0,05 & 27,78 $\pm$ 0,63 & 49,43 $\pm$ 0,46 & 42,25 $\pm$ 0,48 & 51,42 $\pm$ 0,32 & 48,48 $\pm$ 0,36 \\
    \hline
    Xoá cạnh (30\%) & 47,65 $\pm$ 0,04 & 26,46 $\pm$ 0,21 & 49,36 $\pm$ 0,41 & 42,26 $\pm$ 0,31 & 51,43 $\pm$ 0,31 & 48,51 $\pm$ 0,38 \\
    \hline
    Xoá cạnh (50\%) & 47,31 $\pm$ 0,26 & 25,86 $\pm$ 0,07 & 49,29 $\pm$ 0,35 & 42,36 $\pm$ 0,34 & 51,43 $\pm$ 0,32 & 48,52 $\pm$ 0,40 \\
    \hline
    Xoá đỉnh vật thể (30\%) & 43,77 $\pm$ 0,23 & 20,13 $\pm$ 0,53 & 49,21 $\pm$ 0,37 & 41,95 $\pm$ 0,28 & 50,97 $\pm$ 0,22 & 46,92 $\pm$ 0,38 \\
    \hline
    Đổi nhãn vật thể (20\%) & 43,43 $\pm$ 0,39 & 20,08 $\pm$ 0,35 & 49,03 $\pm$ 0,45 & 41,60 $\pm$ 0,42 & 50,82 $\pm$ 0,27 & 47,24 $\pm$ 0,43 \\
    \hline
  \end{tabular}
\end{table*}
```

### Bảng 7: 5 truy vấn thành công, 5 thất bại

**Caption.** Năm truy vấn mà xếp hạng lại đưa ảnh đúng lên hạng 1 từ hạng CLIP thấp nhất, và năm truy vấn mà ảnh đúng rơi khỏi hạng 1 xa nhất (seed 13, test). Điểm đồ thị là của ảnh đúng, trong ngoặc là hạng của nó trong 1.500 ảnh.

| Truy vấn | Hạng: CLIP → sau | Điểm đồ thị | Relation đóng góp nhiều nhất / đồ thị của ảnh đúng |
|---|---|---|---|
| *Thành công* |  |  |  |
| A bicycle with an umbrella, basket and cloths with pens. | 26 → 1 | 0,537 (1) | handle on umbrella; flowers on umbrella; clip in basket |
| A bicycle with a blue umbrella and baskets attached to carry things. | 23 → 1 | 0,520 (1) | handle on umbrella; bell on bike; clip in basket |
| a bicycle with a basket and a blue and pink umbrella | 21 → 1 | 0,532 (1) | handle on umbrella; bell on bike; flowers on umbrella |
| A large red truck parks in front of a building. | 14 → 1 | 0,406 (3) | window on truck; light on truck; building next to fire truck |
| The man is holding a large bird outside. | 14 → 1 | 0,321 (1) | man petting bird; shirt worn by man; man has man |
| *Thất bại* |  |  |  |
| A man teaches a boy how to ski | 1 → 37 | −0,010 (1.266) | 4 vật thể (sky, people, clouds, outdoors), 7 relation về mây và trời |
| A rode that has car and bicycle lane that cars are driving on the left side of the road | 1 → 32 | 0,008 (813) | 3 vật thể (sign, glass, ramp), không có relation |
| A man seated next to bags, suit cases and back packs | 1 → 25 | −0,081 (1.291) | 1 vật thể (sky), không có relation |
| the birds are flying next to the boat | 1 → 25 | 0,033 (913) | 4 vật thể (man, floor, steps, deck), 2 relation |
| Female tennis player in full run on a blue court to complete a backhand return. | 1 → 21 | 0,103 (213) | 2 vật thể (sign, letters), 1 relation |

Thành công khi đồ thị của ảnh đúng chứa các vật thể câu nêu. Thất bại khi chú giải đồ thị của ảnh đúng gần như rỗng hoặc không nhắc vật thể trong câu, nên điểm đồ thị gần 0. Trên cả 7.500 truy vấn: 607 ảnh đúng lên hạng 1, 281 ảnh đúng mất hạng 1.

Nguồn: `scripts/explain_retrieval.py`, mô hình huấn luyện lại ngày 21/11.

```latex
\begin{table*}[t]
  \centering
  \caption{Năm truy vấn mà xếp hạng lại đưa ảnh đúng lên hạng 1 từ hạng CLIP thấp nhất, và năm truy vấn mà ảnh đúng rơi khỏi hạng 1 xa nhất (seed 13, test). Điểm đồ thị là của ảnh đúng, trong ngoặc là hạng của nó trong 1.500 ảnh}
  \label{tab:t1-cases}
  \footnotesize
  \setlength{\tabcolsep}{3pt}
  \begin{tabularx}{\textwidth}{|X|c|c|X|}
    \hline
    Truy vấn & Hạng: CLIP $\rightarrow$ sau & Điểm đồ thị & Relation đóng góp nhiều nhất / đồ thị của ảnh đúng \\
    \hline
    \multicolumn{4}{|l|}{\textit{Thành công}} \\
    \hline
    A bicycle with an umbrella, basket and cloths with pens. & 26 $\rightarrow$ 1 & 0,537 (1) & handle on umbrella; flowers on umbrella; clip in basket \\
    \hline
    A bicycle with a blue umbrella and baskets attached to carry things. & 23 $\rightarrow$ 1 & 0,520 (1) & handle on umbrella; bell on bike; clip in basket \\
    \hline
    a bicycle with a basket and a blue and pink umbrella & 21 $\rightarrow$ 1 & 0,532 (1) & handle on umbrella; bell on bike; flowers on umbrella \\
    \hline
    A large red truck parks in front of a building. & 14 $\rightarrow$ 1 & 0,406 (3) & window on truck; light on truck; building next to fire truck \\
    \hline
    The man is holding a large bird outside. & 14 $\rightarrow$ 1 & 0,321 (1) & man petting bird; shirt worn by man; man has man \\
    \hline
    \multicolumn{4}{|l|}{\textit{Thất bại}} \\
    \hline
    A man teaches a boy how to ski & 1 $\rightarrow$ 37 & $-$0,010 (1.266) & 4 vật thể (sky, people, clouds, outdoors), 7 relation về mây và trời \\
    \hline
    A rode that has car and bicycle lane that cars are driving on the left side of the road & 1 $\rightarrow$ 32 & 0,008 (813) & 3 vật thể (sign, glass, ramp), không có relation \\
    \hline
    A man seated next to bags, suit cases and back packs & 1 $\rightarrow$ 25 & $-$0,081 (1.291) & 1 vật thể (sky), không có relation \\
    \hline
    the birds are flying next to the boat & 1 $\rightarrow$ 25 & 0,033 (913) & 4 vật thể (man, floor, steps, deck), 2 relation \\
    \hline
    Female tennis player in full run on a blue court to complete a backhand return. & 1 $\rightarrow$ 21 & 0,103 (213) & 2 vật thể (sign, letters), 1 relation \\
    \hline
  \end{tabularx}
\end{table*}
```

## Nhiệm vụ 2

### Bảng 8: Kết quả chính mức 2 trên hai tập

**Caption.** Truy hồi ảnh theo caption (%). Trên VG ∩ COCO báo cáo R@1, R@5, R@10 và MRR; trên MKG-W caption subset báo cáo R@1. Trung bình ± độ lệch chuẩn qua 3 seed.

| Phương pháp | R@1 | R@5 | R@10 | MRR | R@1 |
|---|---|---|---|---|---|
| CLIP ViT-B/32 | 43,89 | 72,19 | 82,64 | 56,76 | 35,60 |
| CLIP + GraphSAGE (đỉnh ảnh học được) | 48,12 ± 0,23 | 75,33 ± 0,65 | 83,87 ± 2,12 | 60,42 ± 0,44 | **43,35 ± 0,54** |
| CLIP + AdaMF-MAT | **51,42 ± 0,32** | **79,36 ± 0,37** | **88,91 ± 0,19** | **63,98 ± 0,31** | 41,16 ± 0,59 |

AdaMF-MAT hơn GraphSAGE 3,3 điểm R@1 trên VG ∩ COCO nhưng thua 2,2 điểm trên MKG-W caption subset.

Nhóm cột trong bản LaTeX: VG ∩ COCO (4 cột); MKG-W caption subset (1 cột).

Nguồn: README, mục Cấp độ 2.

```latex
\begin{table*}[t]
  \centering
  \caption{Truy hồi ảnh theo caption (\%). Trên VG $\cap$ COCO báo cáo R@1, R@5, R@10 và MRR; trên MKG-W caption subset báo cáo R@1. Trung bình $\pm$ độ lệch chuẩn qua 3 seed}
  \label{tab:t2-main-caption}
  \small
  \setlength{\tabcolsep}{3pt}
  \begin{tabular}{|l|c|c|c|c|c|}
    \hline
    \multirow{2}{*}{Phương pháp} & \multicolumn{4}{c|}{VG $\cap$ COCO} & MKG-W caption subset \\
    \cline{2-5} \cline{6-6}
     & R@1 & R@5 & R@10 & MRR & R@1 \\
    \hline
    CLIP ViT-B/32 & 43,89 & 72,19 & 82,64 & 56,76 & 35,60 \\
    \hline
    CLIP + GraphSAGE (đỉnh ảnh học được) & 48,12 $\pm$ 0,23 & 75,33 $\pm$ 0,65 & 83,87 $\pm$ 2,12 & 60,42 $\pm$ 0,44 & \textbf{43,35 $\pm$ 0,54} \\
    \hline
    CLIP + AdaMF-MAT & \textbf{51,42 $\pm$ 0,32} & \textbf{79,36 $\pm$ 0,37} & \textbf{88,91 $\pm$ 0,19} & \textbf{63,98 $\pm$ 0,31} & 41,16 $\pm$ 0,59 \\
    \hline
  \end{tabular}
\end{table*}
```

### Bảng 9: Truy vấn trực tiếp và gián tiếp trên MKG-W

**Caption.** R@1 (%) trên MKG-W sau xếp hạng lại cùng CLIP, tách theo nhóm truy vấn: 2.626 cặp gián tiếp, 2.710 cặp trực tiếp. 3 seed. Cột thứ hai cho biết mô hình nhận gì từ câu hỏi.

| Phương pháp | Đọc từ câu hỏi | Gián tiếp | Trực tiếp | Toàn bộ |
|---|---|---|---|---|
| CLIP ViT-B/32 | câu chữ | 2,70 | 52,51 | 28,00 |
| CLIP + GraphSAGE | câu chữ | 5,81 ± 0,16 | 60,96 ± 0,23 | 33,82 ± 0,17 |
| CLIP + GraphSAGE, không cạnh | câu chữ | 4,70 ± 0,21 | **87,27 ± 0,30** | **46,63 ± 0,18** |
| CLIP + path score (không huấn luyện) | anchor | 15,61 | 52,51 | 34,35 |
| CLIP + RotatE (chỉ cấu trúc) | anchor + quan hệ | 26,18 ± 0,48 | 52,51 | 39,56 ± 0,24 |
| CLIP + AdaMF-MAT | anchor + quan hệ | 24,77 ± 0,42 | 52,51 | 38,86 ± 0,20 |
| CLIP + relation path scorer | câu chữ + anchor | **27,44 ± 0,12** | 52,51 | 40,17 ± 0,06 |

CLIP gần như không trả lời được câu gián tiếp (2,70). Các mô hình xuất phát từ anchor hơn hẳn; chúng không so ngang được với GraphSAGE vì được cho thêm anchor. Nhóm trực tiếp của chúng bằng CLIP vì chỉ xếp hạng lại nhóm gián tiếp.

Nguồn: `docs/mkg-w-results.md`.

```latex
\begin{table*}[t]
  \centering
  \caption{R@1 (\%) trên MKG-W sau xếp hạng lại cùng CLIP, tách theo nhóm truy vấn: 2.626 cặp gián tiếp, 2.710 cặp trực tiếp. 3 seed. Cột thứ hai cho biết mô hình nhận gì từ câu hỏi}
  \label{tab:t2-direct-indirect}
  \small
  \setlength{\tabcolsep}{3pt}
  \begin{tabular}{|l|l|c|c|c|}
    \hline
    Phương pháp & Đọc từ câu hỏi & Gián tiếp & Trực tiếp & Toàn bộ \\
    \hline
    CLIP ViT-B/32 & câu chữ & 2,70 & 52,51 & 28,00 \\
    \hline
    CLIP + GraphSAGE & câu chữ & 5,81 $\pm$ 0,16 & 60,96 $\pm$ 0,23 & 33,82 $\pm$ 0,17 \\
    \hline
    CLIP + GraphSAGE, không cạnh & câu chữ & 4,70 $\pm$ 0,21 & \textbf{87,27 $\pm$ 0,30} & \textbf{46,63 $\pm$ 0,18} \\
    \hline
    CLIP + path score (không huấn luyện) & anchor & 15,61 & 52,51 & 34,35 \\
    \hline
    CLIP + RotatE (chỉ cấu trúc) & anchor + quan hệ & 26,18 $\pm$ 0,48 & 52,51 & 39,56 $\pm$ 0,24 \\
    \hline
    CLIP + AdaMF-MAT & anchor + quan hệ & 24,77 $\pm$ 0,42 & 52,51 & 38,86 $\pm$ 0,20 \\
    \hline
    CLIP + relation path scorer & câu chữ + anchor & \textbf{27,44 $\pm$ 0,12} & 52,51 & 40,17 $\pm$ 0,06 \\
    \hline
  \end{tabular}
\end{table*}
```

### Bảng 10: Tái lập AdaMF-MAT trên bài toán gốc

**Caption.** Dự đoán liên kết trên tập test của MKG-W (%): bản cài đặt trong nghiên cứu này so với số của bài báo gốc. 3 seed.

| Mô hình | MRR | Hits@1 | Hits@3 | Hits@10 |
|---|---|---|---|---|
| AdaMF-MAT (bài báo) | **35,85** | **29,04** | 39,01 | 48,42 |
| AdaMF-MAT (cài đặt này) | 34,58 ± 0,07 | 25,78 ± 0,07 | **39,47 ± 0,26** | **49,18 ± 0,29** |
| RotatE (chỉ cấu trúc) | 29,96 ± 0,14 | 24,54 ± 0,12 | 32,17 ± 0,26 | 40,35 ± 0,21 |

Bản cài đặt đạt MRR thấp hơn bài báo 1,3 điểm và hơn RotatE chỉ cấu trúc 4,6 điểm, nên ảnh và văn bản có giúp dự đoán liên kết.

Nguồn: `docs/mkg-w-results.md`.

```latex
\begin{table}[t]
  \centering
  \caption{Dự đoán liên kết trên tập test của MKG-W (\%): bản cài đặt trong nghiên cứu này so với số của bài báo gốc. 3 seed}
  \label{tab:t2-reproduce}
  \scriptsize
  \setlength{\tabcolsep}{3pt}
  \begin{tabular}{|l|c|c|c|c|}
    \hline
    Mô hình & MRR & Hits@1 & Hits@3 & Hits@10 \\
    \hline
    AdaMF-MAT (bài báo) & \textbf{35,85} & \textbf{29,04} & 39,01 & 48,42 \\
    \hline
    AdaMF-MAT (cài đặt này) & 34,58 $\pm$ 0,07 & 25,78 $\pm$ 0,07 & \textbf{39,47 $\pm$ 0,26} & \textbf{49,18 $\pm$ 0,29} \\
    \hline
    RotatE (chỉ cấu trúc) & 29,96 $\pm$ 0,14 & 24,54 $\pm$ 0,12 & 32,17 $\pm$ 0,26 & 40,35 $\pm$ 0,21 \\
    \hline
  \end{tabular}
\end{table}
```

### Bảng 11: Các biến thể ngoài ba mô hình chính

**Caption.** Các biến thể ngoài ba mô hình ở bảng kết quả chính, trên cùng hai tập và cùng quy trình xếp hạng lại (%). 3 seed; dòng ghi 5 seed thêm seed 211 và 307.

| Phương pháp | R@1 | R@5 | R@10 | MRR | R@1 |
|---|---|---|---|---|---|
| CLIP + GraphSAGE (đỉnh ảnh mang CLIP) | 49,43 ± 0,46 | 77,90 ± 0,47 | 87,52 ± 0,69 | 62,22 ± 0,37 | 39,98 ± 0,40 |
| CLIP + linear adapter (chỉ modality image) | 49,76 ± 0,08 | 77,86 ± 0,06 | 87,33 ± 0,42 | 62,44 ± 0,13 | 35,75 ± 0,43 |
| CLIP + AdaMF, không MAT, chuẩn hoá L2 (5 seed) | **51,93 ± 0,32** | **79,81 ± 0,17** | **89,23 ± 0,27** | **64,47 ± 0,24** | **41,70 ± 0,92** |

Linear adapter không dùng đồ thị đã ngang GraphSAGE đỉnh ảnh mang CLIP trên VG ∩ COCO, nhưng chỉ ngang CLIP trên MKG-W caption subset.

Nhóm cột trong bản LaTeX: VG ∩ COCO (4 cột); MKG-W caption subset (1 cột).

Nguồn: README, mục Cấp độ 2.

```latex
\begin{table*}[t]
  \centering
  \caption{Các biến thể ngoài ba mô hình ở bảng kết quả chính, trên cùng hai tập và cùng quy trình xếp hạng lại (\%). 3 seed; dòng ghi 5 seed thêm seed 211 và 307}
  \label{tab:t2-abl-variants}
  \small
  \setlength{\tabcolsep}{3pt}
  \begin{tabular}{|l|c|c|c|c|c|}
    \hline
    \multirow{2}{*}{Phương pháp} & \multicolumn{4}{c|}{VG $\cap$ COCO} & MKG-W caption subset \\
    \cline{2-5} \cline{6-6}
     & R@1 & R@5 & R@10 & MRR & R@1 \\
    \hline
    CLIP + GraphSAGE (đỉnh ảnh mang CLIP) & 49,43 $\pm$ 0,46 & 77,90 $\pm$ 0,47 & 87,52 $\pm$ 0,69 & 62,22 $\pm$ 0,37 & 39,98 $\pm$ 0,40 \\
    \hline
    CLIP + linear adapter (chỉ modality image) & 49,76 $\pm$ 0,08 & 77,86 $\pm$ 0,06 & 87,33 $\pm$ 0,42 & 62,44 $\pm$ 0,13 & 35,75 $\pm$ 0,43 \\
    \hline
    CLIP + AdaMF, không MAT, chuẩn hoá L2 (5 seed) & \textbf{51,93 $\pm$ 0,32} & \textbf{79,81 $\pm$ 0,17} & \textbf{89,23 $\pm$ 0,27} & \textbf{64,47 $\pm$ 0,24} & \textbf{41,70 $\pm$ 0,92} \\
    \hline
  \end{tabular}
\end{table*}
```

### Bảng 12: Thành phần của AdaMF-MAT

**Caption.** Ablation các thành phần của AdaMF-MAT trên VG ∩ COCO: R@1 sau xếp hạng lại (%), 3 seed.

| Cấu hình | R@1 |
|---|---|
| AdaMF-MAT đầy đủ | 51,42 |
| AdaMF, không MAT | 51,63 |
| Mean pooling, có MAT | **52,16** |
| Mean pooling, không MAT | 51,69 |
| Bỏ structure | 51,92 |
| Bỏ text | 50,54 |
| Bỏ image | 47,75 |

Adaptive fusion và MAT không giúp. Bỏ image mất 3,9 điểm, bỏ structure không đổi: mô hình dựa vào nhánh ảnh.

Nguồn: README, mục Ablation của AdaMF-MAT.

```latex
\begin{table}[t]
  \centering
  \caption{Ablation các thành phần của AdaMF-MAT trên VG $\cap$ COCO: R@1 sau xếp hạng lại (\%), 3 seed}
  \label{tab:t2-abl-components}
  \footnotesize
  \setlength{\tabcolsep}{3pt}
  \begin{tabular}{|l|c|}
    \hline
    Cấu hình & R@1 \\
    \hline
    AdaMF-MAT đầy đủ & 51,42 \\
    \hline
    AdaMF, không MAT & 51,63 \\
    \hline
    Mean pooling, có MAT & \textbf{52,16} \\
    \hline
    Mean pooling, không MAT & 51,69 \\
    \hline
    Bỏ structure & 51,92 \\
    \hline
    Bỏ text & 50,54 \\
    \hline
    Bỏ image & 47,75 \\
    \hline
  \end{tabular}
\end{table}
```

### Bảng 13: Ablation modality trên MKG-W caption subset

**Caption.** Ablation modality trên MKG-W caption subset (%). 3 seed, dòng đầu 5 seed. Cột 2 là R@1 sau xếp hạng lại với CLIP, cột 3 là R@1 chỉ dùng điểm mô hình.

| Cấu hình | Sau xếp hạng lại | Chỉ điểm mô hình |
|---|---|---|
| AdaMF, không MAT, L2 | 41,70 ± 0,92 | **34,29 ± 1,34** |
| Bỏ image | **44,37 ± 0,68** | 31,25 ± 0,26 |
| Bỏ structure | 41,12 ± 0,80 | 32,62 ± 2,11 |
| Bỏ text | 40,44 ± 1,62 | 31,97 ± 1,71 |
| GraphSAGE (đỉnh ảnh học được) | 43,35 ± 0,54 | 28,19 ± 1,08 |

Trên tập này bỏ image lại tăng 2,7 điểm: nhánh ảnh lặp lại thông tin CLIP đã có trong điểm cuối.

Nguồn: `docs/mkg-w-captions-results.md`.

```latex
\begin{table}[t]
  \centering
  \caption{Ablation modality trên MKG-W caption subset (\%). 3 seed, dòng đầu 5 seed. Cột 2 là R@1 sau xếp hạng lại với CLIP, cột 3 là R@1 chỉ dùng điểm mô hình}
  \label{tab:t2-abl-mkgw-modality}
  \footnotesize
  \setlength{\tabcolsep}{3pt}
  \begin{tabular}{|l|c|c|}
    \hline
    Cấu hình & Sau xếp hạng lại & Chỉ điểm mô hình \\
    \hline
    AdaMF, không MAT, L2 & 41,70 $\pm$ 0,92 & \textbf{34,29 $\pm$ 1,34} \\
    \hline
    Bỏ image & \textbf{44,37 $\pm$ 0,68} & 31,25 $\pm$ 0,26 \\
    \hline
    Bỏ structure & 41,12 $\pm$ 0,80 & 32,62 $\pm$ 2,11 \\
    \hline
    Bỏ text & 40,44 $\pm$ 1,62 & 31,97 $\pm$ 1,71 \\
    \hline
    GraphSAGE (đỉnh ảnh học được) & 43,35 $\pm$ 0,54 & 28,19 $\pm$ 1,08 \\
    \hline
  \end{tabular}
\end{table}
```

### Bảng 14: Mô hình có đọc cạnh không: che cạnh được hỏi

**Caption.** Confuser acc@1 (%) của điểm mô hình (không cộng CLIP) trên bộ relation queries của VG ∩ COCO, 5 seed. Cột “Che cạnh” là kết quả sau khi xoá cạnh được hỏi khỏi đồ thị của ảnh đúng. `so0.3`: structure-only dropout 30%; `sl0.1`: structure-only loss với trọng số 0,1.

| Cấu hình | acc@1 | Che cạnh | acc@1 | Che cạnh |
|---|---|---|---|---|
| CLIP (tham chiếu) | 28,8 | – | 32,6 | – |
| AdaMF không MAT, L2 (mốc) | 27,7 | 27,7 | 33,6 | 33,7 |
| + `so0.3` | **30,0** | 28,5 | **35,0** | 33,2 |
| + `sl0.1` | **30,0** | 28,5 | 34,9 | 33,1 |
| + `so0.3` + `sl0.1` | **30,0** | 28,4 | 34,9 | 33,0 |

Mô hình mốc không đổi khi che cạnh, tức không đọc cạnh. Ép nhánh structure tự khớp caption làm kết quả tụt 1,5 điểm khi che cạnh: mô hình bắt đầu dùng cạnh.

Nhóm cột trong bản LaTeX: all (1.408 câu) (2 cột); contrast (734 câu) (2 cột).

Nguồn: README, mục Mô hình có đọc cạnh không.

```latex
\begin{table}[t]
  \centering
  \caption{Confuser acc@1 (\%) của điểm mô hình (không cộng CLIP) trên bộ relation queries của VG $\cap$ COCO, 5 seed. Cột ``Che cạnh'' là kết quả sau khi xoá cạnh được hỏi khỏi đồ thị của ảnh đúng. \texttt{so0.3}: structure-only dropout 30\%; \texttt{sl0.1}: structure-only loss với trọng số 0,1}
  \label{tab:t2-abl-relation}
  \footnotesize
  \setlength{\tabcolsep}{3pt}
  \begin{tabular}{|l|c|c|c|c|}
    \hline
    \multirow{2}{*}{Cấu hình} & \multicolumn{2}{c|}{all (1.408 câu)} & \multicolumn{2}{c|}{contrast (734 câu)} \\
    \cline{2-3} \cline{4-5}
     & acc@1 & Che cạnh & acc@1 & Che cạnh \\
    \hline
    CLIP (tham chiếu) & 28,8 & -- & 32,6 & -- \\
    \hline
    AdaMF không MAT, L2 (mốc) & 27,7 & 27,7 & 33,6 & 33,7 \\
    \hline
    + \texttt{so0.3} & \textbf{30,0} & 28,5 & \textbf{35,0} & 33,2 \\
    \hline
    + \texttt{sl0.1} & \textbf{30,0} & 28,5 & 34,9 & 33,1 \\
    \hline
    + \texttt{so0.3} + \texttt{sl0.1} & \textbf{30,0} & 28,4 & 34,9 & 33,0 \\
    \hline
  \end{tabular}
\end{table}
```

### Bảng 15: Ablation cạnh trên MKG-W

**Caption.** R@1 gián tiếp (%) trên MKG-W sau xếp hạng lại cùng CLIP khi thay đồ thị. Xáo cạnh giữ nguyên đầu và đuôi của các triple nhưng ghép lại ngẫu nhiên. CLIP đạt 2,70.

| Phương pháp | Đồ thị thật | Xáo cạnh | Không cạnh |
|---|---|---|---|
| GraphSAGE | 5,81 ± 0,16 | 5,03 ± 0,39 | 4,70 ± 0,21 |
| Path score (không huấn luyện) | 15,61 | 2,44 | – |
| Relation path scorer | **27,44 ± 0,12** | 2,75 ± 0,05 | – |

Hai mô hình đi theo đường từ anchor rơi về mức CLIP khi xáo cạnh, nên phần tăng của chúng đến từ cạnh thật. GraphSAGE gần như không đổi.

Nguồn: `docs/mkg-w-results.md`.

```latex
\begin{table}[t]
  \centering
  \caption{R@1 gián tiếp (\%) trên MKG-W sau xếp hạng lại cùng CLIP khi thay đồ thị. Xáo cạnh giữ nguyên đầu và đuôi của các triple nhưng ghép lại ngẫu nhiên. CLIP đạt 2,70}
  \label{tab:t2-kg-edges}
  \footnotesize
  \setlength{\tabcolsep}{3pt}
  \begin{tabular}{|l|c|c|c|}
    \hline
    Phương pháp & Đồ thị thật & Xáo cạnh & Không cạnh \\
    \hline
    GraphSAGE & 5,81 $\pm$ 0,16 & 5,03 $\pm$ 0,39 & 4,70 $\pm$ 0,21 \\
    \hline
    Path score (không huấn luyện) & 15,61 & 2,44 & -- \\
    \hline
    Relation path scorer & \textbf{27,44 $\pm$ 0,12} & 2,75 $\pm$ 0,05 & -- \\
    \hline
  \end{tabular}
\end{table}
```

### Bảng 16: Hai bộ truy vấn chỉ dùng để đánh giá

**Caption.** R@1 (%) trên hai bộ truy vấn gián tiếp chỉ dùng để đánh giá của MKG-W.

| Bộ truy vấn | Số câu | CLIP | Relation path scorer |
|---|---|---|---|
| Câu cần hai triple nối nhau | 3.943 | 0,96 | **3,9** |
| Câu viết tay | 30 | 0,00 | **20,0** |

Bộ viết tay nhỏ, mỗi câu đổi 3,3 điểm. Anchor được đọc từ nhãn của câu hỏi; tự tìm anchor trong câu chữ thì bộ viết tay còn 6,7.

Nguồn: `docs/mkg-w-results.md`.

```latex
\begin{table}[t]
  \centering
  \caption{R@1 (\%) trên hai bộ truy vấn gián tiếp chỉ dùng để đánh giá của MKG-W}
  \label{tab:t2-extra-queries}
  \footnotesize
  \setlength{\tabcolsep}{3pt}
  \begin{tabular}{|l|c|c|c|}
    \hline
    Bộ truy vấn & Số câu & CLIP & Relation path scorer \\
    \hline
    Câu cần hai triple nối nhau & 3.943 & 0,96 & \textbf{3,9} \\
    \hline
    Câu viết tay & 30 & 0,00 & \textbf{20,0} \\
    \hline
  \end{tabular}
\end{table}
```

## Nhiệm vụ 3

### Bảng 17: Fidelity và sparsity

**Caption.** Fidelity và sparsity của giải thích trên VG ∩ COCO: 200 truy vấn test, 3 seed. Xoá đồng thời nhóm relation được chọn khỏi đồ thị của ảnh đứng đầu, hoặc chỉ giữ nhóm đó; “ngẫu nhiên” là trung bình 20 nhóm cùng số relation. Sparsity là 1 trừ tỷ lệ relation nằm trong giải thích.

| Mức xoá | Cách chọn relation | Mất vị trí đầu khi xoá | Điểm đồ thị giảm | Giữ vị trí đầu khi chỉ giữ nhóm | Sparsity |
|---|---|---|---|---|---|
| 10% | Bỏ từng relation (giải thích chính) | **18,23%** | **0,0236** | **91,83%** | 79,58% |
| 10% | GNNExplainer (đối chứng) | 8,52% | 0,0090 | 87,91% | 79,58% |
| 10% | Ngẫu nhiên | 4,66% | 0,0022 | 81,06% | 79,58% |
| 25% | Bỏ từng relation (giải thích chính) | **25,05%** | **0,0327** | **96,59%** | 69,57% |
| 25% | GNNExplainer (đối chứng) | 12,78% | 0,0153 | 92,33% | 69,57% |
| 25% | Ngẫu nhiên | 6,64% | 0,0034 | 85,52% | 69,57% |

Xoá nhóm giải thích làm ảnh mất vị trí đầu nhiều gấp khoảng 4 lần xoá ngẫu nhiên. GNNExplainer chọn relation không qua phép xoá mà vẫn vượt ngẫu nhiên, nên tín hiệu không chỉ do cách chọn tự chấm chính nó.

Nguồn: `reports/explanation-quality/index.html`, lượt 21/11.

```latex
\begin{table*}[t]
  \centering
  \caption{Fidelity và sparsity của giải thích trên VG $\cap$ COCO: 200 truy vấn test, 3 seed. Xoá đồng thời nhóm relation được chọn khỏi đồ thị của ảnh đứng đầu, hoặc chỉ giữ nhóm đó; ``ngẫu nhiên'' là trung bình 20 nhóm cùng số relation. Sparsity là 1 trừ tỷ lệ relation nằm trong giải thích}
  \label{tab:t3-fidelity}
  \footnotesize
  \setlength{\tabcolsep}{3pt}
  \begin{tabular}{|c|l|c|c|c|c|}
    \hline
    Mức xoá & Cách chọn relation & Mất vị trí đầu khi xoá & Điểm đồ thị giảm & Giữ vị trí đầu khi chỉ giữ nhóm & Sparsity \\
    \hline
    10\% & Bỏ từng relation (giải thích chính) & \textbf{18,23\%} & \textbf{0,0236} & \textbf{91,83\%} & 79,58\% \\
    \hline
    10\% & GNNExplainer (đối chứng) & 8,52\% & 0,0090 & 87,91\% & 79,58\% \\
    \hline
    10\% & Ngẫu nhiên & 4,66\% & 0,0022 & 81,06\% & 79,58\% \\
    \hline
    25\% & Bỏ từng relation (giải thích chính) & \textbf{25,05\%} & \textbf{0,0327} & \textbf{96,59\%} & 69,57\% \\
    \hline
    25\% & GNNExplainer (đối chứng) & 12,78\% & 0,0153 & 92,33\% & 69,57\% \\
    \hline
    25\% & Ngẫu nhiên & 6,64\% & 0,0034 & 85,52\% & 69,57\% \\
    \hline
  \end{tabular}
\end{table*}
```

### Bảng 18: Validity

**Caption.** Validity của giải thích: 42 relation của 20 truy vấn (10 ảnh trả về đúng, 10 sai), do một trợ lý AI xem ảnh và chấm một lượt; chưa có người chấm.

| Tiêu chí | Có | Chưa rõ | Không | Tỷ lệ có |
|---|---|---|---|---|
| Relation đúng với ảnh | 38 | 4 | 0 | 90,5% |
| Liên quan truy vấn: chạm tới vật thể, hành động hoặc ràng buộc được hỏi | 39 | 1 | 2 | 92,9% |
| Đạt cả hai | 35 | 5 | 2 | 83,3% |
| Liên quan truy vấn, đọc chặt: nói đúng quan hệ hoặc hành động được hỏi | 15 | 0 | 27 | 35,7% |
| Đạt cả hai, đọc chặt | 14 | 0 | 28 | 33,3% |

Relation gần như luôn đúng với ảnh. Tỷ lệ liên quan truy vấn phụ thuộc cách đọc tiêu chí: 83,3% nếu chỉ cần chạm tới vật thể được hỏi, 33,3% nếu phải nói đúng quan hệ được hỏi.

Nguồn: `reports/explanation-quality/index.html`, lượt 21/11.

```latex
\begin{table}[t]
  \centering
  \caption{Validity của giải thích: 42 relation của 20 truy vấn (10 ảnh trả về đúng, 10 sai), do một trợ lý AI xem ảnh và chấm một lượt; chưa có người chấm}
  \label{tab:t3-validity}
  \footnotesize
  \setlength{\tabcolsep}{3pt}
  \begin{tabularx}{\columnwidth}{|X|c|c|c|c|}
    \hline
    Tiêu chí & Có & Chưa rõ & Không & Tỷ lệ có \\
    \hline
    Relation đúng với ảnh & 38 & 4 & 0 & 90,5\% \\
    \hline
    Liên quan truy vấn: chạm tới vật thể, hành động hoặc ràng buộc được hỏi & 39 & 1 & 2 & 92,9\% \\
    \hline
    Đạt cả hai & 35 & 5 & 2 & 83,3\% \\
    \hline
    Liên quan truy vấn, đọc chặt: nói đúng quan hệ hoặc hành động được hỏi & 15 & 0 & 27 & 35,7\% \\
    \hline
    Đạt cả hai, đọc chặt & 14 & 0 & 28 & 33,3\% \\
    \hline
  \end{tabularx}
\end{table}
```

### Bảng 19: Bằng chứng trên 10 truy vấn

**Caption.** Mười truy vấn test (seed 13, mức xoá 25%): năm truy vấn đầu tiên trong mẫu có ảnh trả về đúng và năm truy vấn đầu tiên có ảnh trả về sai, với ảnh có 6–11 relation. Điểm đồ thị giảm khi xoá nhóm giải thích so với trung bình 20 nhóm ngẫu nhiên.

| Truy vấn | Ảnh trả về | Relation trong giải thích (bị xoá) | Điểm giảm | Ngẫu nhiên | Hạng |
|---|---|---|---|---|---|
| A zebra stands next to a tree on gravel. | đúng | door behind zebra; shadow from tree; branch in tree | 0,0335 | 0,0110 | 1 → 1 |
| Workers busy making donuts in a commercial bakery | đúng | doughnut on top of tray; lights on top of ceiling | 0,0403 | 0,0034 | 1 → 1 |
| A small child stands in a shopping cart with an umbrella. | đúng | child holding umbrella; pants on child; person wearing skirt | 0,1175 | 0,0158 | 1 → 1 |
| Teddy bears with a guitar are in the dark. | đúng | person behind bear; bear holds guitar; bear holding guitar | 0,0109 | −0,0089 | 1 → 1 |
| The boats are sailing out on the water. | đúng | wake behind boat; land in water; object in sky | 0,0105 | −0,0003 | 1 → 2 |
| A close up of flowers in a vase. | sai | flowers in vase; vase has flowers; vase holds flowers | 0,0186 | 0,0004 | 1 → 1 |
| A display of donuts six for five dollars | sai | donut in bag; sign for donut; tray of donut | 0,0142 | −0,0052 | 1 → 1 |
| People walking through a covered pedestrian walk-way that has a large clock | sai | hair on woman; man wearing hat | 0,0327 | 0,0098 | 1 → 1 |
| Three zebra in the middle of a field with a body of water in the distance. | sai | tail of zebra; stripe on zebra | 0,0177 | −0,0055 | 1 → 1 |
| A green light in a palm tree lined street. | sai | traffic light above street; pole holds traffic light | 0,0276 | 0,0031 | 1 → 1 |

Điểm đồ thị giảm nhiều hơn ngẫu nhiên ở cả 10 truy vấn, nhưng hạng chỉ đổi ở 1 truy vấn: CLIP được giữ nguyên và điểm đồ thị chỉ đổi cỡ 0,01–0,1.

Nguồn: `runs/fidelity/full-joint-test.json` của lượt 21/11 (file local).

```latex
\begin{table*}[t]
  \centering
  \caption{Mười truy vấn test (seed 13, mức xoá 25\%): năm truy vấn đầu tiên trong mẫu có ảnh trả về đúng và năm truy vấn đầu tiên có ảnh trả về sai, với ảnh có 6--11 relation. Điểm đồ thị giảm khi xoá nhóm giải thích so với trung bình 20 nhóm ngẫu nhiên}
  \label{tab:t3-evidence}
  \footnotesize
  \setlength{\tabcolsep}{3pt}
  \begin{tabularx}{\textwidth}{|X|c|X|c|c|c|}
    \hline
    Truy vấn & Ảnh trả về & Relation trong giải thích (bị xoá) & Điểm giảm & Ngẫu nhiên & Hạng \\
    \hline
    A zebra stands next to a tree on gravel. & đúng & door behind zebra; shadow from tree; branch in tree & 0,0335 & 0,0110 & 1 $\rightarrow$ 1 \\
    \hline
    Workers busy making donuts in a commercial bakery & đúng & doughnut on top of tray; lights on top of ceiling & 0,0403 & 0,0034 & 1 $\rightarrow$ 1 \\
    \hline
    A small child stands in a shopping cart with an umbrella. & đúng & child holding umbrella; pants on child; person wearing skirt & 0,1175 & 0,0158 & 1 $\rightarrow$ 1 \\
    \hline
    Teddy bears with a guitar are in the dark. & đúng & person behind bear; bear holds guitar; bear holding guitar & 0,0109 & $-$0,0089 & 1 $\rightarrow$ 1 \\
    \hline
    The boats are sailing out on the water. & đúng & wake behind boat; land in water; object in sky & 0,0105 & $-$0,0003 & 1 $\rightarrow$ 2 \\
    \hline
    A close up of flowers in a vase. & sai & flowers in vase; vase has flowers; vase holds flowers & 0,0186 & 0,0004 & 1 $\rightarrow$ 1 \\
    \hline
    A display of donuts six for five dollars & sai & donut in bag; sign for donut; tray of donut & 0,0142 & $-$0,0052 & 1 $\rightarrow$ 1 \\
    \hline
    People walking through a covered pedestrian walk-way that has a large clock & sai & hair on woman; man wearing hat & 0,0327 & 0,0098 & 1 $\rightarrow$ 1 \\
    \hline
    Three zebra in the middle of a field with a body of water in the distance. & sai & tail of zebra; stripe on zebra & 0,0177 & $-$0,0055 & 1 $\rightarrow$ 1 \\
    \hline
    A green light in a palm tree lined street. & sai & traffic light above street; pole holds traffic light & 0,0276 & 0,0031 & 1 $\rightarrow$ 1 \\
    \hline
  \end{tabularx}
\end{table*}
```

### Bảng 20: VN Heritage: thẻ dữ liệu

**Caption.** VN Heritage, MMKG tự xây về địa điểm và di tích Việt Nam (bản lõi).

| Thành phần | Số lượng | Nguồn |
|---|---|---|
| Địa điểm có ảnh | 160 (train 97, validation 22, test 41) | Wikidata |
| Ảnh | 772, mỗi địa điểm 3–5 ảnh | Wikimedia Commons |
| Thực thể trong đồ thị | 849 (160 địa điểm + 689 đỉnh tri thức) | Wikidata |
| Claim | 981, 18 quan hệ | Wikidata |
| Cạnh rút từ bài viết | 902 | Wikipedia tiếng Việt |
| Truy vấn gián tiếp | khoảng 145 câu test mỗi cách chia, sinh từ 25% claim bị giấu | claim Wikidata |

Ảnh nối vào đồ thị qua địa điểm mà nó chụp. Số claim (981) nằm trong khoảng gợi ý của đề (300–1.000 triple); số thực thể (849) và số ảnh (772) vượt khoảng gợi ý (50–150 và 200–500). Truy vấn viết bằng tiếng Anh vì CLIP dùng chung chỉ học tiếng Anh; tên riêng giữ tiếng Việt.

Nguồn: `docs/vn-heritage-results.md`, `data/processed/vn_heritage_core/stats.json`.

```latex
\begin{table}[t]
  \centering
  \caption{VN Heritage, MMKG tự xây về địa điểm và di tích Việt Nam (bản lõi)}
  \label{tab:t3-vn-data}
  \footnotesize
  \setlength{\tabcolsep}{3pt}
  \begin{tabularx}{\columnwidth}{|l|X|l|}
    \hline
    Thành phần & Số lượng & Nguồn \\
    \hline
    Địa điểm có ảnh & 160 (train 97, validation 22, test 41) & Wikidata \\
    \hline
    Ảnh & 772, mỗi địa điểm 3--5 ảnh & Wikimedia Commons \\
    \hline
    Thực thể trong đồ thị & 849 (160 địa điểm + 689 đỉnh tri thức) & Wikidata \\
    \hline
    Claim & 981, 18 quan hệ & Wikidata \\
    \hline
    Cạnh rút từ bài viết & 902 & Wikipedia tiếng Việt \\
    \hline
    Truy vấn gián tiếp & khoảng 145 câu test mỗi cách chia, sinh từ 25\% claim bị giấu & claim Wikidata \\
    \hline
  \end{tabularx}
\end{table}
```

### Bảng 21: VN Heritage: kết quả

**Caption.** Truy hồi trên VN Heritage, tập test (%). Bốn cột đầu chấm trên gallery 772 ảnh, cột cuối chấm trên gallery 160 địa điểm. Trung bình ± độ lệch chuẩn qua 10 cách chia claim, mỗi cách chia 5 seed.

| Phương pháp | Nhóm truy vấn | R@1 | R@5 | R@10 | MRR | R@10 theo địa điểm |
|---|---|---|---|---|---|---|
| CLIP ViT-B/32 | trực tiếp | 4,9 | **24,4** | **31,7** | **14,2** | 34,2 |
| CLIP + GraphSAGE | trực tiếp | **5,9 ± 1,8** | 16,4 ± 6,7 | 24,3 ± 8,7 | 12,6 ± 3,1 | **41,1 ± 3,7** |
| CLIP ViT-B/32 | gián tiếp | 6,7 ± 1,7 | **17,8 ± 2,7** | **25,1 ± 3,2** | 13,3 ± 1,8 | 30,5 ± 3,8 |
| CLIP + GraphSAGE | gián tiếp | **8,6 ± 1,0** | 17,3 ± 2,8 | 24,4 ± 3,9 | **14,1 ± 1,5** | **35,8 ± 2,8** |

Chấm theo ảnh, đồ thị không vượt CLIP ở R@10; chấm theo địa điểm thì hơn 5,3 điểm ở nhóm gián tiếp. Lý do: mọi ảnh của một địa điểm nhận cùng điểm đồ thị, nên một địa điểm sai được đẩy lên kéo theo tất cả ảnh của nó.

Nguồn: `docs/vn-heritage-results.md`.

```latex
\begin{table*}[t]
  \centering
  \caption{Truy hồi trên VN Heritage, tập test (\%). Bốn cột đầu chấm trên gallery 772 ảnh, cột cuối chấm trên gallery 160 địa điểm. Trung bình $\pm$ độ lệch chuẩn qua 10 cách chia claim, mỗi cách chia 5 seed}
  \label{tab:t3-vn-results}
  \footnotesize
  \setlength{\tabcolsep}{3pt}
  \begin{tabular}{|l|l|c|c|c|c|c|}
    \hline
    Phương pháp & Nhóm truy vấn & R@1 & R@5 & R@10 & MRR & R@10 theo địa điểm \\
    \hline
    CLIP ViT-B/32 & trực tiếp & 4,9 & \textbf{24,4} & \textbf{31,7} & \textbf{14,2} & 34,2 \\
    \hline
    CLIP + GraphSAGE & trực tiếp & \textbf{5,9 $\pm$ 1,8} & 16,4 $\pm$ 6,7 & 24,3 $\pm$ 8,7 & 12,6 $\pm$ 3,1 & \textbf{41,1 $\pm$ 3,7} \\
    \hline
    CLIP ViT-B/32 & gián tiếp & 6,7 $\pm$ 1,7 & \textbf{17,8 $\pm$ 2,7} & \textbf{25,1 $\pm$ 3,2} & 13,3 $\pm$ 1,8 & 30,5 $\pm$ 3,8 \\
    \hline
    CLIP + GraphSAGE & gián tiếp & \textbf{8,6 $\pm$ 1,0} & 17,3 $\pm$ 2,8 & 24,4 $\pm$ 3,9 & \textbf{14,1 $\pm$ 1,5} & \textbf{35,8 $\pm$ 2,8} \\
    \hline
  \end{tabular}
\end{table*}
```

### Bảng 22: VN Heritage: ablation cạnh

**Caption.** Ablation đồ thị trên VN Heritage, truy vấn gián tiếp, tập test (%). Mỗi biến thể huấn luyện lại trên 10 cách chia × 5 seed. Cột chênh lệch là bản đầy đủ trừ biến thể, ghép cặp theo cách chia, ± sai số chuẩn; trong ngoặc là số cách chia thắng/thua.

| Biến thể | R@1 | R@10 | Đầy đủ − biến thể | R@10 | Đầy đủ − biến thể |
|---|---|---|---|---|---|
| Đầy đủ (đồ thị Wikidata) | 8,6 ± 1,0 | 24,4 ± 3,9 |  | 35,8 ± 2,8 |  |
| Bỏ hết cạnh | 8,8 ± 0,8 | 23,3 ± 5,1 | +1,2 ± 1,8 (6/4) | 34,7 ± 2,4 | +1,1 ± 1,1 (7/3) |
| Cạnh ngẫu nhiên | **9,0 ± 1,0** | 21,7 ± 4,3 | **+2,8 ± 1,5 (8/2)** | 31,4 ± 2,5 | **+4,4 ± 1,0 (9/1)** |
| Bỏ nhãn quan hệ | 8,4 ± 1,5 | 24,6 ± 3,1 | −0,2 ± 1,0 (5/4) | 34,8 ± 2,1 | +1,0 ± 0,4 (8/2) |
| Không hướng | 8,7 ± 1,0 | **24,9 ± 4,0** | −0,5 ± 1,2 (4/6) | **36,8 ± 2,1** | −1,0 ± 0,8 (4/6) |

Chỉ phép cạnh ngẫu nhiên tách được khỏi bản đầy đủ: cạnh sai gây hại hơn là không có cạnh. Bỏ hết cạnh gần ngang bản đầy đủ, giống kết quả trên VG ∩ COCO.

Nhóm cột trong bản LaTeX: Gallery 772 ảnh (3 cột); Gallery 160 địa điểm (2 cột).

Nguồn: `docs/vn-heritage-results.md`.

```latex
\begin{table*}[t]
  \centering
  \caption{Ablation đồ thị trên VN Heritage, truy vấn gián tiếp, tập test (\%). Mỗi biến thể huấn luyện lại trên 10 cách chia $\times$ 5 seed. Cột chênh lệch là bản đầy đủ trừ biến thể, ghép cặp theo cách chia, $\pm$ sai số chuẩn; trong ngoặc là số cách chia thắng/thua}
  \label{tab:t3-vn-ablation}
  \footnotesize
  \setlength{\tabcolsep}{3pt}
  \begin{tabular}{|l|c|c|c|c|c|}
    \hline
    \multirow{2}{*}{Biến thể} & \multicolumn{3}{c|}{Gallery 772 ảnh} & \multicolumn{2}{c|}{Gallery 160 địa điểm} \\
    \cline{2-4} \cline{5-6}
     & R@1 & R@10 & Đầy đủ $-$ biến thể & R@10 & Đầy đủ $-$ biến thể \\
    \hline
    Đầy đủ (đồ thị Wikidata) & 8,6 $\pm$ 1,0 & 24,4 $\pm$ 3,9 &  & 35,8 $\pm$ 2,8 &  \\
    \hline
    Bỏ hết cạnh & 8,8 $\pm$ 0,8 & 23,3 $\pm$ 5,1 & +1,2 $\pm$ 1,8 (6/4) & 34,7 $\pm$ 2,4 & +1,1 $\pm$ 1,1 (7/3) \\
    \hline
    Cạnh ngẫu nhiên & \textbf{9,0 $\pm$ 1,0} & 21,7 $\pm$ 4,3 & \textbf{+2,8 $\pm$ 1,5 (8/2)} & 31,4 $\pm$ 2,5 & \textbf{+4,4 $\pm$ 1,0 (9/1)} \\
    \hline
    Bỏ nhãn quan hệ & 8,4 $\pm$ 1,5 & 24,6 $\pm$ 3,1 & $-$0,2 $\pm$ 1,0 (5/4) & 34,8 $\pm$ 2,1 & +1,0 $\pm$ 0,4 (8/2) \\
    \hline
    Không hướng & 8,7 $\pm$ 1,0 & \textbf{24,9 $\pm$ 4,0} & $-$0,5 $\pm$ 1,2 (4/6) & \textbf{36,8 $\pm$ 2,1} & $-$1,0 $\pm$ 0,8 (4/6) \\
    \hline
  \end{tabular}
\end{table*}
```

### Bảng 23: VN Heritage: AdaMF-MAT

**Caption.** AdaMF-MAT trên VN Heritage: truy vấn gián tiếp, tập test, chấm theo địa điểm (%). 3 cách chia claim × 5 seed. Cột cuối là MRR dự đoán liên kết của chính mô hình. RotatE là AdaMF-MAT bỏ ảnh và văn bản.

| Phương pháp | R@1 | R@10 | MRR dự đoán liên kết |
|---|---|---|---|
| CLIP | 7,1 | 30,8 | – |
| CLIP + GraphSAGE | 8,5 | 37,2 | – |
| CLIP + AdaMF-MAT | **11,0** | **40,1** | **0,292** |
| + cạnh ngẫu nhiên | 5,5 | 29,0 | 0,080 |
| CLIP + RotatE | 6,5 | 26,6 | 0,084 |

AdaMF-MAT hơn CLIP 3,9 điểm R@1 và rơi xuống dưới CLIP khi xáo cạnh. Nó không so ngang được với GraphSAGE vì được cho sẵn anchor và quan hệ của truy vấn.

Nguồn: `docs/vn-heritage-results.md`.

```latex
\begin{table}[t]
  \centering
  \caption{AdaMF-MAT trên VN Heritage: truy vấn gián tiếp, tập test, chấm theo địa điểm (\%). 3 cách chia claim $\times$ 5 seed. Cột cuối là MRR dự đoán liên kết của chính mô hình. RotatE là AdaMF-MAT bỏ ảnh và văn bản}
  \label{tab:t3-vn-adamf}
  \footnotesize
  \setlength{\tabcolsep}{3pt}
  \begin{tabular}{|l|c|c|c|}
    \hline
    Phương pháp & R@1 & R@10 & MRR dự đoán liên kết \\
    \hline
    CLIP & 7,1 & 30,8 & -- \\
    \hline
    CLIP + GraphSAGE & 8,5 & 37,2 & -- \\
    \hline
    CLIP + AdaMF-MAT & \textbf{11,0} & \textbf{40,1} & \textbf{0,292} \\
    \hline
    + cạnh ngẫu nhiên & 5,5 & 29,0 & 0,080 \\
    \hline
    CLIP + RotatE & 6,5 & 26,6 & 0,084 \\
    \hline
  \end{tabular}
\end{table}
```

## Phụ lục

### Bảng 24: Truy vấn gián tiếp qua khái niệm cha (IsA)

**Caption.** Truy vấn gián tiếp qua khái niệm cha WordNet IsA trên VG ∩ COCO (%), điểm mô hình không cộng CLIP, 3 seed. KG là đồ thị có thêm cạnh IsA; “che IsA” là xoá cạnh IsA của ảnh đúng rồi chấm lại.

| Mô hình | Đồ thị | R@1 | Confuser acc@1 | R@1 | Confuser acc@1 |
|---|---|---|---|---|---|
| CLIP (tham chiếu) | không dùng | 3,8 | 23,9 | 7,6 | 27,3 |
| AdaMF L2 | base | **5,3** | 24,2 | 9,1 | 27,2 |
| AdaMF L2 | KG (+ IsA) | 5,0 | 25,0 | 8,4 | 26,7 |
| AdaMF L2 | KG, che IsA | 4,1 | 24,3 | 8,4 | 26,9 |
| AdaMF `so0.3` | base | **5,3** | 24,7 | **9,5** | **28,6** |
| AdaMF `so0.3` | KG (+ IsA) | **5,3** | 25,2 | 9,1 | 27,7 |
| AdaMF `so0.3` | KG, che IsA | 4,7 | **25,8** | 9,2 | 28,3 |

Mô hình có dùng cạnh IsA (che đi thì R@1 gián tiếp tụt) nhưng IsA không giúp so với đồ thị gốc.

Nhóm cột trong bản LaTeX: Gián tiếp (1.387 cặp) (2 cột); Trực tiếp (1.387 cặp) (2 cột).

Nguồn: README, mục Indirect queries.

```latex
\begin{table*}[t]
  \centering
  \caption{Truy vấn gián tiếp qua khái niệm cha WordNet IsA trên VG $\cap$ COCO (\%), điểm mô hình không cộng CLIP, 3 seed. KG là đồ thị có thêm cạnh IsA; ``che IsA'' là xoá cạnh IsA của ảnh đúng rồi chấm lại}
  \label{tab:t2-abl-isa}
  \small
  \setlength{\tabcolsep}{3pt}
  \begin{tabular}{|l|l|c|c|c|c|}
    \hline
    \multirow{2}{*}{Mô hình} & \multirow{2}{*}{Đồ thị} & \multicolumn{2}{c|}{Gián tiếp (1.387 cặp)} & \multicolumn{2}{c|}{Trực tiếp (1.387 cặp)} \\
    \cline{3-4} \cline{5-6}
     &  & R@1 & Confuser acc@1 & R@1 & Confuser acc@1 \\
    \hline
    CLIP (tham chiếu) & không dùng & 3,8 & 23,9 & 7,6 & 27,3 \\
    \hline
    AdaMF L2 & base & \textbf{5,3} & 24,2 & 9,1 & 27,2 \\
    \hline
    AdaMF L2 & KG (+ IsA) & 5,0 & 25,0 & 8,4 & 26,7 \\
    \hline
    AdaMF L2 & KG, che IsA & 4,1 & 24,3 & 8,4 & 26,9 \\
    \hline
    AdaMF \texttt{so0.3} & base & \textbf{5,3} & 24,7 & \textbf{9,5} & \textbf{28,6} \\
    \hline
    AdaMF \texttt{so0.3} & KG (+ IsA) & \textbf{5,3} & 25,2 & 9,1 & 27,7 \\
    \hline
    AdaMF \texttt{so0.3} & KG, che IsA & 4,7 & \textbf{25,8} & 9,2 & 28,3 \\
    \hline
  \end{tabular}
\end{table*}
```
