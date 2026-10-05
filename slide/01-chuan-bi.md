# Bước 1 · Chuẩn bị

Nguồn: https://vlearn.dev/course/k04-l34-p2-t4/reader?day=D04&part=lab-14687d39-s02-doc

## Về bài lab này
Đo tác động của một lỗi sensor, trình bày bằng chứng benchmark và đề xuất quyết định kỹ thuật.

## Bạn làm được gì sau bài này
- Tạo được demo hoặc benchmark nhỏ với ít nhất một metric định lượng.
- Giải thích một failure case của sensor và tác động tới thuật toán hoặc tính năng.
- Trình bày quyết định kỹ thuật dựa trên kết quả nhóm đo và giới hạn của nguồn tham khảo.

**Mục tiêu của lab:** Chọn một bài toán sensor trong xe ADAS, robot mặt đất hoặc drone; tìm paper/repository liên quan; chạy một demo hoặc benchmark nhỏ; và giải thích kết quả trước lớp. Sensor ở đây là hệ đo có lỗi và giới hạn: chất lượng dữ liệu, I/O, latency, calibration, đồng bộ thời gian hoặc điều kiện hoạt động đều có thể làm tính năng phía sau suy giảm.

Mỗi nhóm gồm đúng 5 thành viên, có 120 phút làm việc và 3-5 phút trình bày. Cuối buổi cần có báo cáo hoặc slide ngắn, log/ảnh/plot chứng minh đã chạy, ít nhất một metric, một failure case và một đề xuất cải tiến. Cả 5 thành viên dùng chung repository, nhưng mỗi người nộp một bản riêng trên VLearn. Mục tiêu là có bằng chứng kiểm tra được và giải thích được trade-off thực tế, không phải đạt một con số đẹp.

**Thời gian:** 0-15 phút. **Kết quả cần có:** Một bài toán đủ hẹp để thử trong lớp, một claim ban đầu, metric dự định đo và phân công nhóm.

## Nhóm sẽ kiểm tra điều gì?

Trước khi tìm thuật toán, hãy chọn tình huống sensor có thể sai và tính năng nào sẽ chịu ảnh hưởng. Câu “camera kém khi trời mưa” quá rộng để đo. Một claim hữu ích phải chỉ ra điều kiện thay đổi và dấu hiệu quan sát; ví dụ, “khi ảnh bị nhòe mạnh hơn, blur score thay đổi và detector confidence có thể giảm”. Claim là giả thuyết để thử, không phải kết luận đã được chứng minh.

Trong lab này, baseline là điều kiện dùng để so sánh, còn degraded condition là điều kiện có lỗi được tạo ra hoặc quan sát được. Hai điều kiện phải dùng cùng cách tính metric. Nếu mỗi điều kiện dùng ảnh, cấu hình hoặc cách tính khác nhau, nhóm sẽ khó giải thích phần chênh lệch đến từ sensor hay từ cách thử.

1. Chọn một chủ đề T1-T8 ở Bước 4 và ghi rõ nền tảng: xe ADAS, robot mặt đất hoặc drone. Chọn một chủ đề giúp nhóm dồn thời gian vào bằng chứng thay vì ghép nhiều bài toán chưa hoàn tất.
2. Chỉ định sensor và failure case sẽ kiểm tra: camera, LiDAR, radar, sonar/ToF hoặc multi-sensor; chẳng hạn glare, night, fog, rain, packet loss, rolling shutter, timestamp offset, calibration drift, radar ghost hay range timeout.
3. Viết claim và metric vào cùng một dòng. Nêu metric sẽ tăng hay giảm theo dự đoán, đơn vị đo và cách so sánh baseline với điều kiện lỗi. Nếu chưa có nhãn chuẩn, chọn metric proxy có thể tính được và ghi rõ nó thay thế cho điều gì.
4. Phân công đủ 5 thành viên vào các việc tìm tài liệu, chạy code, ghi benchmark và trình bày. Ghi phần việc của từng người vào bảng; nhiều người có thể cùng phụ trách một việc.

| Nhóm cần chốt | Ghi ngắn trước khi tiếp tục |
|---|---|
| Nền tảng, tính năng, sensor | Xe ADAS/robot/drone; tính năng nào; sensor nào? |
| Failure case | Lỗi xuất hiện trong điều kiện nào? |
| Claim ban đầu | Thay đổi gì → metric dự kiến thay đổi ra sao? |
| Metric và đơn vị | Đo bằng công thức/cách tính nào? |
| Baseline và điều kiện lỗi | Hai cấu hình sẽ so sánh là gì? |
| Phân công 5 thành viên | Ai đọc nguồn, chạy thử, ghi số, trình bày? |

**Tự kiểm tra:** Một người ngoài nhóm đọc bảng trên phải chỉ ra được nhóm sẽ thay đổi yếu tố nào và đo điều gì. Nếu chưa trả lời được, thu hẹp bài toán trước khi chuyển sang tìm paper/repo.
