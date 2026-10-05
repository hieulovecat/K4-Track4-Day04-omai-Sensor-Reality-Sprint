# Bước 3 · Thiết kế benchmark có đối chứng

Nguồn: https://vlearn.dev/course/k04-l34-p2-t4/reader?day=D04&part=lab-14687d39-s04-doc

**Thời gian:** Nằm trong giai đoạn chạy 45-95 phút. **Kết quả cần có:** Cấu hình baseline, mức lỗi, công thức metric và cách lưu bằng chứng.

## Vì sao cần cố định điều kiện so sánh?

Benchmark ở đây không cần quy mô lớn; nó cần trả lời claim nhóm đã đặt. Một phép thử dễ đọc là giữ nguyên mẫu dữ liệu và pipeline, sau đó thay đổi một loại lỗi hoặc một mức perturbation. Chẳng hạn, với LiDAR, có thể tăng tỷ lệ point dropout trên cùng một point cloud và theo dõi point density. Với calibration, có thể thay đổi extrinsic từ giá trị baseline rồi đo reprojection error. Nếu đồng thời thay đổi nguồn dữ liệu, model và ngưỡng đánh giá, nhóm sẽ không biết yếu tố nào gây ra khác biệt.

Metric là số đo dùng để so sánh. Hãy viết định nghĩa của nó trước khi chạy, kể cả khi chỉ là proxy. Point density hoặc blur score cho biết dữ liệu đầu vào suy giảm như thế nào, nhưng tự nó chưa chứng minh mAP của model thật giảm bao nhiêu. Detector confidence cũng không tự động là mAP. Khi không có ground truth, hãy nói “proxy metric” và chỉ kết luận trong phạm vi số đo đó.

## Dữ liệu và mức lỗi nên được ghi thế nào?

Đề lab cho phép dùng ảnh/video, point cloud, chuỗi rangefinder, log cảm biến hoặc dữ liệu tổng hợp. Với dữ liệu tổng hợp, lưu cách tạo và tham số mức lỗi; với dữ liệu thật, lưu mẫu hoặc nguồn được phép dùng. Baseline phải đứng cạnh ít nhất một điều kiện lỗi. Nếu đủ thời gian, tạo nhiều mức lỗi để thấy xu hướng thay vì chỉ hai điểm. Tên mức lỗi cần thể hiện tham số thực tế, ví dụ “offset 50 ms” hoặc “yaw lệch 1°”, không chỉ “mức 1”.

1. Chọn dữ liệu và lưu cấu hình baseline. Dùng một tập mẫu nhỏ đủ để chạy lặp lại trong lớp. Ghi số mẫu, nguồn hoặc quy tắc tạo dữ liệu và thông số sensor liên quan.
2. Tạo các điều kiện lỗi từ cùng baseline. Thay một yếu tố có chủ đích; ghi mức blur/dropout/offset/drift/timeout hoặc cấu hình camera đúng theo chủ đề đã chọn.
3. Định nghĩa metric và đơn vị trước khi xem kết quả. Nêu chiều tốt/xấu của metric, và liệu metric đó phản ánh sensor health, chất lượng thuật toán hay tài nguyên hệ thống.
4. Chuẩn bị bằng chứng tái hiện: lưu lệnh chạy, cấu hình, log, ảnh trước/sau hoặc plot. Nếu phép thử có yếu tố ngẫu nhiên, ghi seed hoặc lặp lại để người đọc hiểu độ ổn định của số đo.

| Điều kiện | Tham số thay đổi | Metric (đơn vị) | Bằng chứng cần lưu | Điều metric cho phép kết luận |
|---|---|---|---|---|
| Baseline | Không chủ động gây lỗi | Giá trị đo được | Log/ảnh/plot | Mốc so sánh |
| Lỗi A | Tham số và mức cụ thể | Giá trị đo được | Log/ảnh/plot | Chênh lệch với baseline |
| Lỗi B, nếu có | Tham số và mức cụ thể | Giá trị đo được | Log/ảnh/plot | Xu hướng khi lỗi tăng |

**Tự kiểm tra:** Trước khi chạy, người đo metric phải biết cần điền số vào cột nào và diễn giải “tốt hơn/xấu hơn” ra sao. Khi bảng đã có ít nhất baseline và một mức lỗi, nhóm mới có cơ sở để phân tích failure case ở Bước 5.
