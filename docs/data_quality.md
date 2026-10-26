# Báo Cáo Chất Lượng Dữ Liệu: Gộp Điểm Trùng Lặp

Ngày chạy: 2026-10-26 | Nguồn: Overpass, vùng mẫu (xem data/source_log.json)

## Quy Tắc

- Hai điểm trùng lặp khi cùng loại, cùng tên sau chuẩn hóa (chữ thường, bỏ dấu, gọn khoảng trắng) và cách nhau dưới 50 m.
- Bắc cầu: Các điểm nối nhau theo chuỗi đều vào một cụm.
- Điểm đại diện: Ưu tiên nút hơn đa giác, nếu bằng nhau thì osm_id nhỏ nhất.
- Điểm không có tên không được gộp.

## Kết Quả (Ngưỡng 50 m)

| Loại | Số điểm thô | Sau khi gộp | Số điểm bị gộp | Tỷ lệ gộp | Không có tên |
| --- | --- | --- | --- | --- | --- |
| bus_stop | 246 | 207 | 39 | 15.9% | 6 |
| health | 37 | 37 | 0 | 0.0% | 7 |
| market | 10 | 10 | 0 | 0.0% | 0 |
| park | 84 | 84 | 0 | 0.0% | 57 |
| school | 62 | 62 | 0 | 0.0% | 4 |

## Độ Nhạy Với Ngưỡng

| Ngưỡng | Số điểm bị gộp |
| --- | --- |
| 30 m | 30 |
| 50 m | 39 |
| 100 m | 52 |

## Nhận Xét

- Sự tập trung của dữ liệu trùng lặp: Hiện tượng trùng lặp dữ liệu chỉ xảy ra duy nhất ở nhóm `bus_stop` với 39 điểm bị gộp (chiếm 15.9%). Các nhóm còn lại (`health`, `market`, `park`, `school`) hoàn toàn không ghi nhận điểm trùng lặp nào ở ngưỡng 50 m.
- Tác động của dữ liệu bị thiếu tên: Nhóm `park` ghi nhận lượng lớn điểm không có tên (57/84 điểm), khiến các thuật toán gộp không thể tiếp cận và xử lý theo quy tắc hiện tại, tiềm ẩn nguy cơ bỏ sót các khu vực công viên/mảng xanh bị khai báo trùng.
- Độ nhạy khoảng cách ổn định: Số lượng điểm gộp tăng đều đặn khi mở rộng ngưỡng. Điều này phản ánh khoảng cách phân bố thực tế của các trạm xe buýt thường nằm sát nhau (dưới 50 m), phù hợp với thực tế hạ tầng giao thông đô thị.

## Hạn Chế

- Điểm không có tên không gộp được, có thể còn trùng.
- Hai nơi khác nhau cùng tên và gần nhau (ví dụ bến xe buýt hai chiều) có thể bị gộp nhầm.
