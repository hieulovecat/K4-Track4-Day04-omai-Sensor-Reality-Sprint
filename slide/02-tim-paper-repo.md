# Bước 2 · Tìm paper/repository và chốt đường chạy

Nguồn: https://vlearn.dev/course/k04-l34-p2-t4/reader?day=D04&part=lab-14687d39-s03-doc

**Thời gian:** 15-45 phút. **Kết quả cần có:** Link nguồn, tóm tắt phương pháp và kế hoạch setup khả thi trong lớp.

## Nguồn nào giúp nhóm chạy được trong thời gian còn lại?

Đề lab yêu cầu tìm paper hoặc repository mới, nhưng chỉ đọc tên thuật toán chưa đủ để tạo bằng chứng. README, dữ liệu mẫu và lệnh chạy cho biết nhóm có thể tái hiện phần nào trong 120 phút. Hãy kiểm tra input, output và giả định của phương pháp trước khi cài đặt: nếu repo đòi model hoặc dataset lớn mà lớp không có sẵn, nhóm vẫn có thể dùng benchmark mô phỏng nhỏ. Khi ấy phải nói rõ metric proxy đang đo điều gì, và nó chưa chứng minh được điều gì về hệ thống hoàn chỉnh.

Paper có thể báo cáo kết quả trên một dataset hoặc phần cứng khác. Đó là kết luận của nguồn. Số đo chạy tại lớp là kết quả của nhóm. Giữ hai loại bằng chứng tách biệt ngay trong ghi chép để khi pitch không biến một con số trích dẫn thành kết quả tự đo.

1. Tìm bằng từ khóa của chủ đề ở Bước 4. Chọn một paper/repo có liên hệ trực tiếp với sensor và failure case đã chốt; lưu link đúng nguồn đã đọc.
2. Đọc abstract/README và phần chạy thử. Ghi input, output, dataset, metric, yêu cầu phần cứng/phần mềm, lệnh chạy và limitation được nguồn nêu. Không tự gán limitation chưa thấy trong nguồn cho tác giả.
3. Chọn đường chạy tối thiểu: demo có sẵn, script nhỏ dùng dữ liệu mẫu, hoặc mô phỏng degradation/calibration/log. Nếu chuyển sang mô phỏng, ghi rõ vì sao đường chạy gốc không phù hợp thời gian và proxy nào vẫn kiểm tra được claim ban đầu.
4. Lưu khả năng tái hiện: link paper/repo, commit hoặc phiên bản, dataset hoặc cách tạo dữ liệu, cấu hình và lệnh thực sự định dùng. Sau khi chạy ở Bước 4, cập nhật lại nếu có thay đổi.

| Câu hỏi khi đọc nguồn | Ghi chép tối thiểu |
|---|---|
| Phương pháp nhận gì và tạo gì? | Input → output |
| Nguồn đo chất lượng bằng gì? | Tên metric, dữ liệu, điều kiện đo |
| Chạy được ở lớp không? | Lệnh, dữ liệu, thời gian, giới hạn phần cứng |
| Nhóm sẽ tái hiện phần nào? | Demo gốc hay benchmark mô phỏng; metric thật hay proxy |
| Cần trích lại gì khi báo cáo? | Link, commit/version, dataset, lệnh chạy |

**Nguồn gợi ý trong PDF:** Đây là danh sách để tra cứu, không phải các nguồn nhóm đã dùng. Ghi link chính xác của tài liệu thực sự đọc vào báo cáo.

- S1: NVIDIA Jetson AGX Orin specification - giới hạn camera, USB, PCIe và Ethernet cho embedded robotics.
- S2: PX4 Distance Sensors / Rangefinders - LiDAR-Lite, sonar, LightWare, TeraRanger và ghi chú tích hợp trên drone.
- S3: Basler camera documentation - USB3, GigE, MIPI CSI-2 và cấu hình camera.
- S4: Texas Instruments mmWave automotive radar references - ứng dụng và interface radar cho ADAS/robot.
- S5: Dong và cộng sự, CVPR 2023 - benchmark 3D corruption robustness: KITTI-C, nuScenes-C, Waymo-C.
- S6: MuFoRa, SemanticSpray++, MUSES - dataset đa cảm biến cho thời tiết bất lợi và uncertainty.
- S7: Galibr 2024, CalibRefine 2025, DF-Calib 2025 - LiDAR-camera calibration targetless/online.
- S8: Heidbrink và cộng sự, EuRAD 2024 - radar auto-annotation từ camera và LiDAR tham chiếu.
- S9: Huai và cộng sự, 2021 - rolling-shutter camera-IMU spatiotemporal calibration.

**Tự kiểm tra:** Nhóm có thể nói ngắn gọn “phương pháp nhận gì, trả gì, đo bằng gì” và chỉ ra lệnh hoặc phép thử sẽ chạy. Nếu chưa có đường chạy rõ ràng, quay về một benchmark mô phỏng nhỏ đã được đề lab cho phép.
