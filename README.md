# Sensor Reality Sprint — Nhóm omai

**Chủ đề T4:** Đo ảnh hưởng của lệch thời gian LiDAR–radar và kiểm tra bù chuyển động trong tình huống xe ADAS. Nhóm gồm **4 thành viên**; danh sách và MSSV ở [TEAMMATES.md](TEAMMATES.md).

Benchmark dùng dữ liệu tổng hợp 2D. Ở tốc độ 20 m/s, radar trễ 100 ms tạo sai số vị trí trung bình khoảng **2,01 m**; bù với offset đã biết đưa sai số về **0,19 m**. Khi offset dao động ngẫu nhiên với độ lệch chuẩn 30 ms, bù bằng một hằng số vẫn còn sai số **0,54 m** và tỷ lệ điểm ngoài gate **11,7%**. Đây là kết quả mô phỏng, chưa phải kiểm chứng trên xe hoặc hệ tracking thật.

## Đọc và sử dụng repository

| Tài liệu / thư mục | Nội dung |
|---|---|
| [Báo cáo kỹ thuật T4](t4_time_sync/README.md) | Bài toán, nguồn, thuật toán, hướng dẫn chạy, kết quả, failure case và đánh đổi. |
| [Phân công nghiên cứu](docs/PHAN_CONG_NGHIEN_CUU.md) | Công việc và sản phẩm bàn giao của 4 thành viên. |
| [Mẫu báo cáo hoặc slide](docs/TEMPLATE_RESEARCH.md) | Mẫu bản cá nhân với 5 mục bắt buộc. |
| [Kết quả benchmark](t4_time_sync/results/summary.md) | Bảng số liệu tổng hợp qua 5 seed. |
| [Log chạy](t4_time_sync/results/run_log.txt) | Lệnh, môi trường và cấu hình của lần chạy lưu trong repo. |
| [Demo GIF](t4_time_sync/results/demo_time_sync.gif) | Minh họa baseline, lệch 50/100 ms và jitter. |
| [Hướng dẫn bài lab](slide/01-chuan-bi.md) | Các bước yêu cầu của bài lab; toàn bộ nội dung nằm trong `slide/`. |

Luồng benchmark: **tạo quỹ đạo chuẩn → mô phỏng LiDAR/radar và lỗi timestamp → không bù / bù biết offset / bù tự ước lượng → tính metric → lưu CSV, bảng và plot**.

## Trạng thái và phần cần hoàn tất

- Đã có mã benchmark, 405 dòng kết quả từ 5 seed, 6 biểu đồ, log và GIF demo.
- Đã có phân công nghiên cứu và mẫu bản cá nhân trong `docs/`.
- Còn hoàn thiện **4 bản báo cáo hoặc slide cá nhân**, lưu trong repo, tập pitch 3–5 phút và mỗi người nộp riêng trên VLearn cùng URL repository chung. Mẫu chưa thay thế bản nộp hoàn chỉnh.
- Các đề xuất giám sát online, giữ offset khi đứng yên và đồng bộ bằng phần cứng/PTP chưa được triển khai hoặc đo trong benchmark này. Rolling shutter là phần mở rộng chưa thực hiện.

Để chạy lại và giữ kết quả đã lưu, dùng hướng dẫn ở [mục Chạy lại](t4_time_sync/README.md#chạy-lại-từ-thư-mục-gốc-repository).
