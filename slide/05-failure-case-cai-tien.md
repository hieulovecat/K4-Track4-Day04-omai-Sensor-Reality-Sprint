# Bước 5 · Giải thích failure case và chọn cải tiến

Nguồn: https://vlearn.dev/course/k04-l34-p2-t4/reader?day=D04&part=lab-14687d39-s06-doc

**Thời gian:** 95-115 phút. **Kết quả cần có:** Một failure case cụ thể, limitation và đề xuất cải tiến có liên hệ với số đo.

## Kết quả nào là quan sát, kết quả nào chỉ là suy luận?

Một failure case không phải danh sách lỗi sensor có thể xảy ra. Nó cần nêu điều kiện đầu vào, tác động tới metric và hệ quả với thuật toán/tính năng. Ví dụ, nếu nhóm chỉ đo mật độ điểm LiDAR, có thể nói mật độ điểm giảm ở mức dropout đã thử. Không thể tự kết luận object recall của một detector chưa chạy giảm một tỷ lệ cụ thể. Những nhận xét về rủi ro của detector hoặc SLAM cần được ghi là suy luận kỹ thuật, trừ khi nhóm đã đo trực tiếp.

Đặt kết quả lớp học cạnh limitation của paper/repo. Dữ liệu tổng hợp, ít mẫu, thiếu ground truth, không đo latency end-to-end hoặc phần cứng khác điều kiện thật đều giới hạn phạm vi kết luận. Mục đích không phải phủ nhận bài thử nhỏ, mà để chọn phép thử hoặc log tiếp theo có ích. Đề xuất cải tiến nên nối trực tiếp với failure vừa thấy: thêm health score cho frame xấu, kiểm tra timestamp, kích hoạt calibration, fallback rangefinder hoặc chọn clip cần gán nhãn.

1. Chọn một hàng kết quả hoặc một frame/clip thể hiện lỗi rõ nhất. Ghi chính xác cấu hình, metric và bằng chứng tương ứng.
2. Viết hai câu tách biệt: “Nhóm quan sát được…” cho kết quả tự đo; “Paper/repo cho biết…” cho kết luận từ nguồn. Nếu nguồn và phép thử không cùng dataset/metric, đừng ghép hai con số như thể so sánh trực tiếp.
3. Nêu limitation của phương pháp hoặc benchmark lớp học và xác định điều nhóm chưa đo được. Ghi một giả thuyết về nguyên nhân nếu cần, nhưng đánh dấu đó là giả thuyết.
4. Đề xuất một cải tiến hoặc fallback rồi chỉ ra metric/log nào sẽ dùng để kiểm tra cải tiến trong vòng thử tiếp theo.

| Câu cần trả lời | Bằng chứng nhóm đưa ra |
|---|---|
| Sensor gặp lỗi gì, ở mức nào? | Tham số lỗi, mẫu/clip, ảnh hoặc log |
| Metric thay đổi ra sao? | Số baseline, số khi lỗi, đơn vị |
| Thuật toán/tính năng bị ảnh hưởng thế nào? | Kết quả đo trực tiếp hoặc suy luận được gắn nhãn |
| Phương pháp còn hạn chế ở đâu? | Limitation từ paper/repo hoặc từ phép thử lớp học |
| Nên làm gì tiếp? | Cải tiến/fallback và cách kiểm chứng |

**Tự kiểm tra:** Một người nghe có thể nhận biết câu nào nhóm đã đo, câu nào nguồn đã báo cáo và câu nào chỉ là giả thuyết. Nếu ba loại câu còn trộn lẫn, sửa trước khi làm slide.
