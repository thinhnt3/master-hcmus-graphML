# Data card: VN Heritage (MMKG tự xây, bản lõi)

MMKG nhỏ về địa điểm và di tích Việt Nam, do nhóm tự xây cho cấp độ 3 của Project 3 (Multimodal XAI, HP3-K35). Mỗi địa điểm có ảnh từ Wikimedia Commons và tri thức từ Wikidata và Wikipedia tiếng Việt. Dùng cho bài toán truy hồi ảnh bằng văn bản có xếp hạng lại bằng đồ thị.

Mọi trường văn bản đều do người viết trên Wikidata, Commons hoặc Wikipedia; không có nội dung nào sinh bằng mô hình.

## 1. Quy mô

| | Số lượng |
|---|---|
| Địa điểm (đều có ảnh) | 160 (train 97 · validation 22 · test 41) |
| Ảnh | 772, mỗi địa điểm 3–5 ảnh (train 464 · validation 108 · test 200) |
| Thực thể trong đồ thị | 849 = 160 địa điểm + 689 đỉnh tri thức |
| Triple tri thức | 1.883 = 889 claim Wikidata của địa điểm + 92 cạnh phân cấp hành chính + 902 cạnh rút từ bài Wikipedia |
| Loại quan hệ | 33 (18 từ Wikidata, 16 từ bài theo sơ đồ `cue`; `located_in_admin` có ở cả hai) |
| Triple mỗi địa điểm | ít nhất 4, trung bình 11,19 |
| Nhóm địa điểm | tôn giáo 65 · lịch sử 36 · công trình 27 · thiên nhiên 20 · bảo tàng, văn hoá 12 |

Đề gợi ý 50–150 thực thể, 300–1.000 triple, 200–500 ảnh; bản lõi này chủ ý lớn hơn. Số liệu máy đọc được: `data/processed/vn_heritage_core/stats.json` và `retrieval/card.json`.

## 2. Các file trong gói

Bảng dưới theo bố cục của gói nộp `vn-heritage-mmkg.zip`. Trong repo có ba chỗ khác:

- Ảnh (`data/raw/vn_heritage/images/`, 186 MB) không nằm trong Git, chỉ có trong gói nộp.
- Báo cáo HTML nằm ở [plans/reports/vn-heritage-261120-0033-mmkg-report.html](../plans/reports/vn-heritage-261120-0033-mmkg-report.html).
- Bảng ghi công ảnh nằm ở `data/processed/vn_heritage_core/IMAGE_CREDITS.csv`.

| Đường dẫn | Nội dung |
|---|---|
| `data/processed/vn_heritage_core/places.jsonl` | 160 địa điểm: QID, nhãn vi/en, mô tả, toạ độ, tỉnh, nhóm, sitelink, đoạn bài Wikipedia, split |
| `data/processed/vn_heritage_core/images.jsonl` | 772 ảnh: địa điểm, trang nguồn, caption, license, tác giả, kích thước, sha256 |
| `data/raw/vn_heritage/images/` | 772 file ảnh (756 JPEG, 16 PNG; thumbnail 960 px), tên file là `image_id` |
| `data/processed/vn_heritage_core/kg_nodes.json` | nhãn và loại của các đỉnh |
| `data/processed/vn_heritage_core/kg_triples.tsv` | đồ thị mặc định (`head`, `relation`, `tail`), sơ đồ đặt tên `cue` |
| `data/processed/vn_heritage_core/kg_triples_<sơ đồ>.tsv` | cùng đồ thị dưới bốn sơ đồ đặt tên cạnh rút từ bài: `generic`, `kind`, `section`, `cue` |
| `data/processed/vn_heritage_core/mention_evidence.jsonl` | bằng chứng của từng cạnh rút từ bài: mục bài, từ khoá, câu chứa liên kết |
| `data/processed/vn_heritage_core/retrieval/` | thực thể, quan hệ, triple, truy vấn và data card của bộ truy hồi; `split-1` … `split-10` là mười cách chia claim |
| `configs/data/vn_heritage_core.yaml` | tham số dựng bản lõi |
| `configs/data/vn_heritage_queries.yaml` | tham số sinh truy vấn |
| `configs/retrieval/vn_heritage_core.yaml` | tham số thí nghiệm truy hồi |
| `scripts/`, `src/data/`, `tests/data/` | code dựng bản lõi và sinh truy vấn, kèm test |
| `docs/vn-heritage-results.md` | kết quả và ablation trên bộ này |
| `docs/vn-heritage-mmkg-report.html` | báo cáo đủ bảng về cách xây, cấu trúc đồ thị, rò rỉ, giấy phép |
| `IMAGE_CREDITS.csv` | ghi công từng ảnh: tác giả, license, trang nguồn |

## 3. Nguồn ảnh và văn bản

| Nguồn | Lấy gì | Giấy phép |
|---|---|---|
| Wikidata | thực thể, nhãn, toạ độ, claim (quan hệ) | CC0 |
| Wikipedia tiếng Việt | danh sách ứng viên, ảnh trong bài, đoạn mở đầu, liên kết trong thân bài | CC BY-SA 4.0 |
| Wikimedia Commons | ảnh, caption, tác giả, license của từng file | theo từng file, xem mục 6 |

Thu thập qua Action API của Wikidata, Wikipedia và Commons (không dùng SPARQL). Mọi phản hồi API được lưu lại, nên dựng lại không cần gọi mạng và không bị nguồn thay đổi giữa chừng.

Bản đầy đủ (1.079 địa điểm, 3.589 ảnh) được dựng qua bảy bước: tìm ứng viên trên Wikidata (quốc gia là Việt Nam, có toạ độ, có ảnh) và bài vi.wikipedia theo 35 tiền tố tên; lấy toạ độ, QID và ảnh đại diện; tải claim và nhãn; lọc lớp và kiểm tra địa điểm ở Việt Nam; chọn ảnh; tải thumbnail 960 px và bỏ trùng; ghi kết quả. Bản lõi trong gói này được cắt từ bản đầy đủ.

## 4. Cách liên kết ảnh với thực thể

- Thứ tự nguồn ảnh của một địa điểm: ảnh P18 trên Wikidata, ảnh đại diện của bài vi.wikipedia, 30 file đầu của Commons category (P373), rồi ảnh trong bài vi.wikipedia.
- Ảnh trong bài chỉ được nhận khi file không xuất hiện ở bài của địa điểm khác; file dùng chung thường là ảnh nhỏ trong hộp điều hướng.
- Mỗi file chỉ gán cho một địa điểm.
- Bỏ file có tên là bản đồ, logo, sơ đồ, cờ, SVG; bỏ ảnh quá nhỏ; bỏ ảnh có caption dưới 3 từ hoặc chỉ lặp tên file; bỏ ảnh không có license.
- Trong bản lõi: 143 địa điểm có 5 ảnh, 6 có 4, 11 có 3. 186 ảnh là ảnh P18 hoặc ảnh đại diện của bài.
- Caption: 305 ảnh có caption tiếng Việt, 276 chỉ có tiếng Anh, 191 không gắn ngôn ngữ; trung vị 9 từ; 336 caption (44%) chứa tên địa điểm.

Trong đồ thị, ảnh nối với địa điểm qua cạnh "ảnh – mô tả – địa điểm"; ảnh không mang cấu trúc riêng.

## 5. Cách tạo triple

Ba loại triple, đều là `(head, relation, tail)` với đầu mút là QID của Wikidata.

**Claim Wikidata của địa điểm (889).** Mỗi claim của địa điểm thành một triple. Bảng ánh xạ thuộc tính → quan hệ nằm trong `configs/data/vn_heritage_core.yaml`:

| Quan hệ | Thuộc tính | Triple |
|---|---|---|
| `located_in_admin` | P131 | 279 (cộng 92 cạnh phân cấp bên dưới) |
| `instance_of` | P31 | 228 |
| `located_in_province` | suy từ chuỗi P131 | 77 |
| `inception_century` | P571, gom theo thế kỷ | 64 |
| `religion` | P140 | 47 |
| `has_part` | P527 | 37 |
| `diocese` | P708 | 35 |
| `heritage_designation` | P1435 | 32 |
| `part_of` | P361 | 32 |
| `significant_event` | P793 | 30 |
| `heritage_criterion` | P2614 | 23 |
| `architectural_style` | P149 | 21 |
| `location` | P276 | 20 |
| `crosses` | P177 | 17 |
| `named_after` | P138 | 13 |
| `made_from_material` | P186 | 10 |
| `dedicated_to` | P825 | 9 |
| `architect` | P84 | 7 |

Cạnh `located_in_province` trùng cặp (địa điểm, đích) với một cạnh `located_in_admin` đã bị bỏ. Ngày khởi dựng (P571) thành cạnh tới một đỉnh thế kỷ dùng chung giữa các địa điểm cùng thời.

**Cạnh phân cấp hành chính (92).** Đơn vị hành chính → đơn vị cha theo P131, tính trong `located_in_admin`. Chuỗi dừng ở cấp tỉnh, nên đỉnh quốc gia không thành hub.

**Cạnh rút từ bài Wikipedia (902).** Mỗi liên kết trong thân bài vi.wikipedia của một địa điểm tới một thực thể thành một cạnh.

- Bỏ liên kết trong bản mẫu (hộp điều hướng, hộp thông tin), chú thích, và các mục "Xem thêm", "Tham khảo", "Chú thích", "Liên kết ngoài".
- Chỉ nhận đích xác định được loại: người, triều đại hoặc thời kỳ, thần Phật, dân tộc, địa điểm, đơn vị hành chính, vật liệu, phong cách, tôn giáo, sông hồ.
- Thực thể chưa có trong đồ thị phải được ít nhất 3 bài nhắc tới; bỏ đích được hơn 5% số bài nhắc tới.
- Bỏ liên kết đứng ngay sau "đường", "phố", "đại lộ", "ngõ", "hẻm", "quảng trường" (tên đường mang tên người).
- Tên quan hệ theo sơ đồ `cue` (mặc định): từ khoá trong câu chứa liên kết quyết định quan hệ (`worships` 81, `located_in_admin` 82, `dated_to_period` 46, `built_by` 13, `burial_of` 5, `restored_by` 2); 673 cạnh còn lại đặt tên theo loại của đích (`mentions_person`, `mentions_place`, …).
- Bằng chứng của từng cạnh nằm ở `mention_evidence.jsonl`.

**Chọn lõi.** Một địa điểm được giữ khi có từ 4 claim Wikidata (không tính cạnh rút từ bài), từ 3 ảnh, và có nhãn tiếng Việt. Địa điểm thực chất là lớp hoặc danh hiệu bị loại.

## 6. Chia tập và bộ truy vấn

- Chia theo địa điểm (seed 13, 15% validation, 15% test), nên mọi ảnh của một địa điểm nằm cùng một tập. Địa điểm nối với nhau qua `part_of`, `has_part`, `location` vào cùng một tập.
- **Truy vấn trực tiếp:** tên địa điểm, theo split địa điểm (97 · 22 · 41).
- **Truy vấn gián tiếp:** giấu 40% claim Wikidata (15% validation, 25% test); mỗi claim bị giấu thành một câu, ví dụ `a heritage site located in Đà Lạt`. Claim train là cạnh của đồ thị; claim validation và test không bao giờ nằm trong đồ thị. Có mười cách chia claim (`split-1` … `split-10`), mỗi cách khoảng 145 truy vấn gián tiếp trên test.
- Mọi claim nối cùng hai đỉnh vào cùng một tập, nên sự kiện bị giấu không đọc lại được từ quan hệ nghịch.
- Cạnh rút từ bài không bao giờ bị hỏi, chỉ làm bằng chứng trong đồ thị.
- Truy vấn viết bằng tiếng Anh vì CLIP dùng chung chỉ học tiếng Anh; tên riêng giữ tiếng Việt.

## 7. Giấy phép và điều kiện sử dụng

Gói này chỉ dùng cho mục đích học tập và nghiên cứu trong khuôn khổ môn học.

- **Tri thức từ Wikidata:** CC0, dùng tự do.
- **Văn bản từ Wikipedia:** CC BY-SA 4.0. Khi dùng lại phải ghi nguồn Wikipedia và phát hành phần phái sinh theo cùng giấy phép.
- **Ảnh từ Wikimedia Commons:** mỗi ảnh giữ giấy phép riêng của nó. `images.jsonl` và `IMAGE_CREDITS.csv` lưu `license`, `license_url`, `artist`, `source_page` cho từng ảnh. Ảnh không có license đã bị loại lúc thu thập.

| License | Số ảnh |
|---|---|
| CC BY-SA 3.0 | 188 |
| CC BY-SA 4.0 | 164 |
| Public domain | 105 |
| CC BY 2.0 | 80 |
| CC0 | 72 |
| CC BY-SA 2.0 | 57 |
| CC BY 4.0 | 49 |
| CC BY 3.0 | 46 |
| CC BY-SA 2.5 | 6 |
| CC BY 2.5 | 2 |
| Attribution | 2 |
| GODL-India | 1 |

Khi phát hành lại hoặc demo công khai:

- Phải ghi công từng ảnh (tác giả, license, trang nguồn) theo `IMAGE_CREDITS.csv`.
- Ảnh CC BY-SA (415 ảnh) kéo theo điều kiện share-alike: phần phái sinh phải phát hành theo cùng giấy phép.
- Ảnh trong gói là thumbnail 960 px đã thu nhỏ từ bản gốc; đây là một thay đổi so với bản gốc và cần nêu khi ghi công.

## 8. Hạn chế đã biết

- **Chưa kiểm tay việc gán ảnh.** Chưa có người kiểm tra một mẫu ngẫu nhiên xem ảnh có đúng địa điểm không; tỉ lệ gán đúng chưa được đo.
- **Chưa thuần tiếng Việt.** Truy vấn và một phần caption là tiếng Anh; 467 trong 772 ảnh không có caption tiếng Việt.
- **Ảnh không mang cấu trúc riêng.** Mọi ảnh của một địa điểm nhận cùng điểm đồ thị.
- **Tỉnh không cùng mốc thời gian.** Tỉnh là trước hoặc sau sáp nhập 2025 tuỳ cách Wikidata ghi; một số địa điểm thiếu tỉnh.
- **Một đỉnh cha hành chính và một đỉnh đích bổ sung không có nhãn** (`stats.json`).
- **Code thu thập bản đầy đủ không nằm trong gói.** Script bước một (`scripts/build_vn_heritage.py`, từ API tới bản đầy đủ) là script local, không nằm trong repo; gói chỉ có code cắt bản lõi và sinh truy vấn. Quy trình bảy bước được mô tả ở mục 3 và trong báo cáo HTML.

## 9. Dựng lại

Chạy từ thư mục gốc của repo, cần Python 3.12 và `pip install -r requirements.txt`:

```bash
python -m scripts.build_vn_heritage_core       # cắt bản lõi từ bản đầy đủ, thêm claim và cạnh rút từ bài
python -m scripts.build_vn_heritage_queries    # sinh truy vấn trực tiếp, gián tiếp và mười cách chia claim
python -m scripts.run_vn_heritage_retrieval    # CLIP và CLIP + GraphSAGE trên bộ này
```

`build_vn_heritage_core` cần bản đầy đủ ở `data/processed/vn_heritage/` và cache API ở `data/raw/vn_heritage/`; hai thư mục này không nằm trong gói.
