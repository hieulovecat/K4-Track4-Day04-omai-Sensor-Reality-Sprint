# Phân công nghiên cứu — Nhóm omai

Nhóm gồm 4 thành viên. Chủ đề chung: **T4 — Lệch thời gian và bù chuyển động giữa LiDAR–radar trong xe ADAS**.

Mỗi người nghiên cứu sâu phần được giao, chia sẻ bằng chứng cho nhóm và tự hoàn thiện **một báo cáo hoặc bộ slide riêng** theo [mẫu nghiên cứu](TEMPLATE_RESEARCH.md). Bản cá nhân vẫn cần đủ cả 5 mục, không chỉ phần mình phụ trách.

## 1. Phân công

| Thành viên | MSSV | Phần nghiên cứu chính | Việc cần làm | Sản phẩm bàn giao |
|---|---|---|---|---|
| Phạm Minh Hiếu | 2A202602030 | Paper và phương pháp | Đọc Qin & Shen 2018 và README VINS-Mono; kiểm tra input, output, giả định, quy ước dấu offset; giải thích điểm giống/khác với mô phỏng của nhóm. | Tóm tắt nguồn có link và vị trí trích dẫn; giải thích thuật toán không bù, bù biết offset, bù tự ước lượng. |
| Đoàn Quang Thắng | 2A202602395 | Bài toán, tổng hợp và trình bày | Nêu tình huống ADAS, claim và ảnh hưởng tới tính năng; tổng hợp kết quả của các bạn; chọn bảng/plot chính; chuẩn bị lời trình bày 3–5 phút. | Nội dung Problem; bản trình bày chung; phần giải thích quyết định và đánh đổi bằng câu ngắn. |
| Nguyễn Tuấn Khanh | 2A202602819 | Mã nguồn và benchmark | Đọc `benchmark.py`; kiểm tra dữ liệu tổng hợp, baseline, offset, tốc độ, seed, công thức metric; đối chiếu CSV với bảng/plot; phụ trách chạy lại nếu nhóm cần. | Bảng cấu hình và kết quả; giải thích cách đo, đơn vị, log và cách tái hiện. |
| Nguyễn Hữu Chương | 2A202602601 | Failure case và cải tiến | Phân tích jitter, đứng yên, phanh/rẽ; tách quan sát với suy luận; nêu giới hạn mô phỏng và chọn cải tiến/fallback cùng cách kiểm chứng. | Một failure case có số đo và bằng chứng; đề xuất kỹ thuật, điều kiện áp dụng và phép thử tiếp theo. |

## 2. Bằng chứng dùng chung

- [Báo cáo kỹ thuật chung](../t4_time_sync/README.md).
- [Mã benchmark](../t4_time_sync/benchmark.py) và [mã demo](../t4_time_sync/demo_video.py).
- [Bảng kết quả](../t4_time_sync/results/summary.md), [CSV từng lần thử](../t4_time_sync/results/results_raw.csv), [CSV tổng hợp](../t4_time_sync/results/results_agg.csv), [log chạy](../t4_time_sync/results/run_log.txt).
- [Timeline](../t4_time_sync/results/fig1_timeline.png), [sai số theo offset](../t4_time_sync/results/fig2_metrics_vs_offset.png), [kiểm tra công thức](../t4_time_sync/results/fig3_formula_check.png).
- [Các tình huống lỗi](../t4_time_sync/results/fig4_scenarios.png), [chi phí ước lượng offset](../t4_time_sync/results/fig6_offset_cost.png), [GIF demo](../t4_time_sync/results/demo_time_sync.gif).

## 3. Cách phối hợp

1. Mỗi người hoàn thành phần nghiên cứu chính, ghi nguồn và đường dẫn bằng chứng.
2. Cả nhóm đối chiếu số liệu, thuật ngữ và phạm vi kết luận trước khi tổng hợp.
3. Mỗi người tạo bản riêng theo mẫu, đủ Problem → Method → Benchmark → Failure case → Engineering decision. Có thể dùng kết quả chung nhưng cần tự giải thích được.
4. Lưu bản cá nhân trong `docs/`, ví dụ `research-2A202602395.md` hoặc `research-2A202602395.pdf`. Nếu dùng slide, lưu bộ slide và/hoặc bản xuất PDF, dẫn tới bằng chứng chung.
5. Tập pitch 3–5 phút; mỗi người tự nộp bản của mình và cùng URL repository trên VLearn, rồi kiểm tra lại liên kết đã nộp.

## 4. Tự kiểm trước bàn giao

- [ ] Đã có 4 bản báo cáo/slide cá nhân, ghi đúng họ tên và MSSV.
- [ ] Mỗi bản đủ 5 mục, có baseline, điều kiện lỗi, metric và đơn vị.
- [ ] Có link nguồn, phiên bản/commit, cấu hình dữ liệu và lệnh chạy.
- [ ] Phân biệt kết quả nhóm đo, kết luận của nguồn và suy luận kỹ thuật.
- [ ] Có failure case, giới hạn, cải tiến và cách kiểm chứng.
- [ ] Các liên kết tới log/CSV/plot truy cập được.
- [ ] Cả 4 người đã hoàn tất lượt nộp riêng trên VLearn.
