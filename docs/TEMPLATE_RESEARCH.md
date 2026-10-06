# Mẫu báo cáo hoặc slide nghiên cứu — T4

**Cách dùng:** Sao chép mẫu thành bản riêng trong `docs/`, thay các phần `[điền …]` bằng nội dung của bạn. Có thể nộp **báo cáo hoặc slide ngắn**; mỗi bản cần đủ 5 mục dưới đây. Nếu làm slide, chuyển mỗi mục thành một slide; có thể thêm trang tiêu đề và nguồn. Mẫu này chưa phải bản nộp hoàn chỉnh.

| Thông tin | Nội dung |
|---|---|
| Họ và tên | [điền họ tên] |
| MSSV | [điền MSSV] |
| Nhóm | omai — 4 thành viên |
| Chủ đề | T4 — Time sync / motion compensation LiDAR–radar |
| Phần nghiên cứu phụ trách | [điền phần phụ trách theo bảng phân công] |
| URL repository chung | https://github.com/hieulovecat/K4-Track4-Day04-omai-Sensor-Reality-Sprint |

## 1. Problem — Bài toán

- **Nền tảng và tính năng:** [xe ADAS; tính năng sử dụng kết quả kết hợp LiDAR–radar].
- **Sensor:** [tần số đo, nhiễu và sensor làm mốc thời gian].
- **Failure thực tế:** [radar đo ở thời điểm nào, timestamp ghi ra lệch thế nào, nguyên nhân nào là tình huống giả định].
- **Claim ban đầu:** [khi offset tăng, metric nào dự kiến tăng/giảm; điều gì xảy ra sau bù chuyển động].
- **Phạm vi:** Dữ liệu tổng hợp 2D; [điền điều mô phỏng này kiểm tra được và chưa chứng minh được trên xe thật].

## 2. Method — Nguồn và phương pháp

| Nội dung | Ghi chép của bạn |
|---|---|
| Paper chính | [tên, tác giả, năm, link nguồn đã đọc] |
| Repository và phiên bản | [link và commit/version; ghi rõ chỉ đọc hay đã chạy] |
| Phương pháp gốc nhận gì, trả gì? | [input → output] |
| Nguồn dùng dữ liệu và metric nào? | [dataset, metric, điều kiện thí nghiệm; vị trí bảng/hình/mục] |
| Giả định và giới hạn nguồn nêu | [điền, kèm vị trí trong nguồn] |
| Nhóm tái hiện phần nào? | [ý tưởng áp dụng; khác biệt camera–IMU của nguồn với LiDAR–radar mô phỏng] |

**Giải thích bằng lời của bạn:**

- `none`: [cách xử lý khi không bù].
- `comp_known`: [bù khi biết offset; vận tốc lấy từ đâu].
- `comp_est`: [ước lượng offset thế nào, rồi bù ra sao; điều kiện để ước lượng có ý nghĩa].
- **Quy ước dấu và đơn vị:** [định nghĩa Δ, đổi ms sang s, quan hệ với ký hiệu trong paper nếu dùng].

Nguồn khởi đầu: [Qin & Shen 2018](https://arxiv.org/abs/1808.00692), [VINS-Mono](https://github.com/HKUST-Aerial-Robotics/VINS-Mono), [tóm tắt của nhóm](../t4_time_sync/README.md). Chỉ ghi “đã đọc” cho nguồn bạn thực sự kiểm tra.

## 3. Benchmark — Cách đo và kết quả

| Điều kiện cần ghi | Cấu hình thực tế |
|---|---|
| Dữ liệu | [cách tạo quỹ đạo 2D, thời lượng, số mẫu được đánh giá] |
| Sensor | [LiDAR/radar: Hz, nhiễu, timestamp] |
| Baseline | [offset và cấu hình mốc] |
| Điều kiện lỗi | [offset cụ thể, tốc độ, kịch bản] |
| Độ lặp lại | [seed, số lần thử, cách tổng hợp] |
| Metric | [công thức, đơn vị, chiều tốt/xấu; metric trực tiếp hay proxy] |

**Lệnh tái hiện từ thư mục gốc repository:**

```bash
cd t4_time_sync
python benchmark.py --out /tmp/omai-t4-research-results
```

Chọn đường dẫn đầu ra mới cho mỗi lần chạy để giữ bằng chứng cũ. Ghi phiên bản Python/thư viện và lệnh thực sự đã dùng; nếu bạn chỉ phân tích kết quả có sẵn, nói rõ điều đó.

| Điều kiện | Phương pháp | Sai số vị trí TB (m) | Ghost rate (%) | Residual RMS (m) |
|---|---|---|---|---|
| Baseline: [điền] | [điền] | [điền] | [điền] | [điền] |
| Lỗi: [điền] | Không bù | [điền] | [điền] | [điền] |
| Cùng điều kiện lỗi | Có bù: [ghi rõ phương pháp] | [điền] | [điền] | [điền] |

**Bằng chứng:** [dẫn bảng/CSV/log và một plot chính; ghi scenario, speed, offset, method để tìm đúng hàng].

**Nhận xét:** [đối chiếu với `sai số ≈ v × Δ`; nêu khi nhiễu hoặc chuyển động khiến xấp xỉ không còn phù hợp]. Ghost rate trong bài là tỷ lệ điểm ngoài gate liên kết, chưa phải số vật thể ảo của một hệ tracking thật.

Tham khảo: [bảng kết quả](../t4_time_sync/results/summary.md), [CSV](../t4_time_sync/results/results_agg.csv), [log](../t4_time_sync/results/run_log.txt), [plot offset](../t4_time_sync/results/fig2_metrics_vs_offset.png).

## 4. Failure case — Một tình huống lỗi

- **Cấu hình:** [chọn jitter hoặc đứng yên; offset, tốc độ, seed/cách tổng hợp].
- **Nhóm quan sát được:** [baseline và số khi lỗi, đơn vị, đường dẫn bằng chứng].
- **Paper/repo cho biết:** [kết luận từ nguồn và vị trí trích dẫn; không so sánh trực tiếp số liệu khác dataset/metric].
- **Ảnh hưởng tới tính năng:** [điều đã đo trực tiếp; gắn nhãn “suy luận kỹ thuật” cho hệ quả chưa đo].
- **Giới hạn:** [dữ liệu tổng hợp, nhiễu, chưa chạy tracker thật, giả định timestamp LiDAR…].
- **Giả thuyết chưa kiểm chứng, nếu có:** [ghi rõ là giả thuyết].

## 5. Engineering decision — Quyết định và đánh đổi

**Từ kết quả trên, tôi đề xuất:** [một cải tiến hoặc fallback cụ thể, lý do dựa trên số đo].

| Câu hỏi | Trả lời |
|---|---|
| Khi nào áp dụng? | [điều kiện và ngưỡng; phân biệt ngưỡng đề xuất với ngưỡng đã kiểm chứng] |
| Lợi ích | [metric/tính năng dự kiến cải thiện] |
| Chi phí hoặc đánh đổi | [tính toán, dữ liệu, phần cứng, độ trễ hoặc điều kiện chuyển động] |
| Khi nào phương án không phù hợp? | [ví dụ jitter lớn hoặc đứng yên làm offset khó ước lượng] |
| Kiểm chứng vòng tiếp theo thế nào? | [tham số sẽ thay đổi, metric/log sẽ đo, tiêu chí đạt] |
| Trạng thái | [mới đề xuất / đã triển khai / đã đo; chỉ ghi trạng thái có bằng chứng] |

## Tự kiểm trước khi nộp

- [ ] Đã thay toàn bộ chỗ trống, ghi họ tên/MSSV và URL repo chung.
- [ ] Đủ 5 mục; số liệu có baseline, đơn vị và bằng chứng.
- [ ] Phân biệt kết quả nhóm, kết luận nguồn và suy luận.
- [ ] Link nguồn, version/commit, dữ liệu, cấu hình và lệnh chạy đầy đủ.
- [ ] Có failure case, cải tiến và đánh đổi.
- [ ] Nếu dùng slide, chữ/số liệu đọc được và trình bày chung trong 3–5 phút.
- [ ] Bản cá nhân đã lưu trong repo; đã nộp riêng trên VLearn và mở lại kiểm tra link/tệp.
