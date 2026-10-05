# Bước 4 · Chạy một chủ đề và ghi kết quả

Nguồn: https://vlearn.dev/course/k04-l34-p2-t4/reader?day=D04&part=lab-14687d39-s05-doc

**Thời gian:** 45-95 phút, bao gồm chuẩn bị ở Bước 3. **Kết quả cần có:** Demo hoặc benchmark chạy được, có log/ảnh/plot và ít nhất một kết quả số.

Chỉ thực hiện một trong tám chủ đề dưới đây. Mỗi chủ đề có benchmark tối thiểu và một thử thách mở rộng. Ưu tiên hoàn thành phần tối thiểu trước; phần mở rộng không thay thế cho bằng chứng chạy. Khi một phương pháp không có nhãn tham chiếu, dùng metric phù hợp với dữ liệu đang có thay vì ghi precision/recall không thể kiểm chứng.

1. Mở dữ liệu hoặc demo đã chọn ở Bước 2 và xác nhận baseline chạy được trước khi tạo lỗi.
2. Chạy từng điều kiện theo thiết kế Bước 3, lưu tham số, log và hình/plot tương ứng. Không đổi metric giữa các điều kiện.
3. Điền số vào bảng kết quả ngay sau mỗi lần chạy và kiểm tra hướng thay đổi so với claim ban đầu.
4. Chọn một trường hợp đáng phân tích: kết quả giảm rõ, số đo không đổi dù dự đoán có đổi, hoặc một lỗi mà metric hiện tại không phát hiện được.

## T1 — Sức khỏe camera thay đổi ra sao?

Camera ADAS có thể gặp glare, night, rain, blur, rolling shutter hoặc lens bẩn. Dùng ảnh/video mẫu và tạo 3-5 mức suy giảm bằng blur, brightness, rain/noise. Đo blur score, saturation ratio, entropy; nếu có detector, đo thêm confidence hoặc proxy cho mAP và nêu rõ giới hạn của proxy. Đầu ra là bảng hoặc ảnh trước/sau cùng nhận xét khi nào nên giảm trọng số camera. Mở rộng: thử ngưỡng theo daytime/nighttime hoặc so với confidence của VLM/vision model. Từ khóa: camera image quality assessment for autonomous driving, blur detection, lens soiling detection, nuScenes-C image corruption, adverse weather perception.

## T2 — LiDAR mất thông tin ở mức nào?

Packet loss, point dropout, fog/rain, motion distortion và lỗi phản xạ có thể làm mất vật thể nhỏ hoặc tạo map sai. Dùng point cloud mẫu hoặc điểm tổng hợp; lần lượt thêm dropout, Gaussian noise, missing beams hoặc motion smear. Đo point density theo khoảng cách; nếu có nhãn/cụm tham chiếu, đo thêm object recall hoặc cluster count. Đầu ra là hình point cloud trước/sau và plot mức corruption so với metric. Mở rộng: so sánh camera-only, LiDAR-only, fusion nếu đã có code. Từ khóa: nuScenes-C LiDAR corruption, KITTI-C LiDAR, Robo3D, point cloud corruption robustness, LiDAR fog rain benchmark.

## T3 — Lệch calibration ảnh hưởng tới fusion thế nào?

Rung, tháo lắp hoặc va chạm nhẹ có thể làm sai extrinsic camera-LiDAR/radar dù từng sensor còn hoạt động. Từ baseline, perturb 0,5-2° yaw/pitch hoặc 2-10 cm translation; đo reprojection error hoặc association giữa 2D bbox và LiDAR points. Đầu ra là plot mức lệch so với lỗi chiếu/association và đề xuất dấu hiệu kích hoạt hiệu chuẩn lại. Mở rộng: đọc một repo targetless calibration và nêu input/output, điều kiện chạy, limitation. Từ khóa: targetless LiDAR camera calibration Galibr, CalibRefine, DF-Calib, online extrinsic calibration autonomous driving.

## T4 — Lệch thời gian tạo sai số vị trí bao nhiêu?

Các sensor không nhất thiết đo cùng lúc; vật thể hoặc ego đang di chuyển có thể khiến LiDAR projection lệch và radar target bị ghost. Tạo chuyển động 2D/3D đơn giản, thêm offset 50-200 ms, rồi đo sai vị trí trước/sau bù chuyển động. Với tốc độ gần như không đổi, kiểm tra xấp xỉ sai số vị trí ≈ tốc độ × độ lệch thời gian; ghi rõ khi giả định này không phù hợp. Nếu có dữ liệu phù hợp, đo thêm ghost rate hoặc trajectory residual. Đầu ra là timeline multi-sensor, công thức/plot sai số và ngưỡng đáng lo trong tình huống nhóm đặt ra. Mở rộng: thêm rolling-shutter line delay. Từ khóa: camera LiDAR time synchronization, rolling shutter camera IMU calibration, motion compensation LiDAR autonomous driving.

## T5 — Pseudo-label radar được kiểm tra thế nào?

Gán nhãn radar khó và tốn công; camera segmentation cùng LiDAR 3D box có thể hỗ trợ liên kết radar target. Không bắt buộc có radar raw: mô phỏng pipeline camera class + LiDAR 3D box → radar target association. Đo agreement score; chỉ tính precision/recall khi nhóm có nhãn tham chiếu hoặc nêu rõ bộ nhãn giả định. Đầu ra là sơ đồ pipeline và tiêu chí QA để tránh nhãn sai do calibration/time sync. Mở rộng: tìm dataset radar-camera-LiDAR và mô tả field, loại nhãn, task. Từ khóa: automatic annotation radar data camera LiDAR, 4D radar auto-labeling LiDAR detection, SemanticSpray++ radar labels.

## T6 — Rangefinder drone báo lỗi khi nào?

Drone landing/altitude hold phụ thuộc rangefinder; sonar/ToF có thể timeout, nhảy số, saturate dưới nắng hoặc gặp bề mặt phản xạ. Tạo chuỗi range/altitude có noise, timeout, stuck value và out-of-range. So sánh median filter, MAD/z-score hoặc Kalman filter đơn giản; đo range variance, timeout rate hoặc landing risk score theo cách nhóm định nghĩa. Đầu ra là plot raw so với filtered range, bảng phát hiện fault và quy tắc fallback khi lỗi ở mức S2/S3; nhóm phải định nghĩa các mức này và ngưỡng áp dụng. Mở rộng: so sánh sonar, ToF LiDAR, radar altimeter cho hạ cánh trong bụi/gió/ánh sáng mạnh. Từ khóa: PX4 rangefinder fault detection, Lidar-Lite PX4, sonar rangefinder drone landing, range sensor outlier filter.

## T7 — Nhiều camera gây nghẽn ở đâu?

Pipeline có thể chậm vì bandwidth, decode, resize hoặc queue latency chứ không chỉ vì model. Ước lượng dữ liệu thô bằng bandwidth = số camera × chiều rộng × chiều cao × FPS × bit/pixel; ghi rõ bit/pixel và đổi đơn vị nhất quán. Nếu có webcam, đo FPS, latency, dropped frames và CPU/GPU load ở 2-3 độ phân giải. Đầu ra là bảng cấu hình so với FPS/latency/drop frame và đề xuất interface phù hợp. Mở rộng: phác sensor stack 4-8 camera với compute budget cố định. Từ khóa: Jetson multi camera CSI bandwidth, USB3 Vision bandwidth, GigE camera bandwidth, GMSL2 multi camera robotics.

## T8 — Clip hiếm nào đáng gán nhãn trước?

Data loop cần tìm clip khó như night, glare, rain, LiDAR low density, radar ghost hoặc nghi ngờ lệch calibration. Tạo dataframe log giả lập với weather, time, health metrics, detector confidence và near-miss flag; viết quy tắc/query chọn top-k clip. Đo slice coverage hoặc failure discovery rate nếu bảng log có trường cần thiết. Đầu ra là bảng clip được chọn, lý do chọn và lợi ích kỳ vọng cho retraining/benchmark. Mở rộng: tăng độ phủ rare case mà không lấy quá nhiều frame gần trùng. Từ khóa: rare case mining autonomous driving, data loop ADAS, sensor health monitoring, active learning autonomous driving.

**Tự kiểm tra:** Nhóm có thể mở log, ảnh hoặc plot và chỉ đúng giá trị metric ở baseline cùng ít nhất một điều kiện lỗi. Nếu chỉ có sơ đồ hoặc ý tưởng, benchmark chưa đạt yêu cầu chạy được của đề lab.
