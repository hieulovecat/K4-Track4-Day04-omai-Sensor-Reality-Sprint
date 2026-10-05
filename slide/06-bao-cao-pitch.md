# Bước 6 · Hoàn thiện báo cáo và pitch

Nguồn: https://vlearn.dev/course/k04-l34-p2-t4/reader?day=D04&part=lab-14687d39-s07-doc

**Thời gian:** 115-120 phút chuẩn bị; sau đó trình bày 3-5 phút/nhóm. **Kết quả cần có:** Bản báo cáo hoặc slide ngắn của từng thành viên, đủ để người khác kiểm tra đường đi từ bài toán tới quyết định kỹ thuật.

## Một trang cần trả lời những gì?

Giữ báo cáo theo năm mục của PDF. Problem nêu nền tảng, tính năng, sensor và failure thực tế. Method nêu paper/repo/thuật toán, input, output và giả định. Benchmark ghi dữ liệu thật hay tổng hợp, cấu hình, metric và kết quả số. Failure case chỉ một tình huống đã phân tích. Engineering decision nêu log, fallback hoặc dữ liệu cần tiếp theo. Đặt link nguồn, commit/version, dataset và lệnh chạy cạnh phần Method/Benchmark để người xem truy vết.

1. Chọn một bảng hoặc plot chính từ Bước 4. Gắn nhãn baseline, mức lỗi, đơn vị và nguồn dữ liệu. Đừng chỉ dán ảnh đẹp mà thiếu số đo.
2. Mỗi thành viên điền năm mục báo cáo bằng câu ngắn, bám bằng chứng chung của nhóm. Ghi rõ đâu là kết luận của paper/repo, đâu là kết quả nhóm tự benchmark.
3. Gắn một failure case và một cải tiến từ Bước 5 vào engineering decision. Người nghe cần thấy vì sao số đo dẫn tới quyết định đó.
4. Tập pitch 3-5 phút theo thứ tự problem → method → benchmark → failure → decision. Kiểm tra có thể mở log/ảnh/plot khi được hỏi nhóm đã chạy gì.

| Tiêu chí trong PDF | Tỷ trọng | Trước khi trình bày, tự đối chiếu |
|---|---|---|
| Benchmark/demo chạy được | 40% | Có code/log/ảnh/plot chứng minh đã chạy, không chỉ nêu ý tưởng. |
| Hiểu failure thực tế | 25% | Nói được nguyên nhân sensor suy giảm và ảnh hưởng tới thuật toán/tính năng. |
| Giải thích thuật toán | 20% | Tóm tắt paper/repo theo input, output, metric, limitation. |
| Trình bày trade-off | 15% | Nói được khi nào nên/không nên dùng phương án trong ADAS/robot/drone. |

## Bản tự kiểm trước pitch
- [ ] Có nền tảng, tính năng và sensor cụ thể.
- [ ] Có metric định lượng, baseline và điều kiện lỗi.
- [ ] Có log/ảnh/plot và một failure case.
- [ ] Có link nguồn, commit/version, dataset, lệnh chạy.
- [ ] Phân biệt kết luận nguồn với kết quả nhóm tự đo.
- [ ] Có một cải tiến hoặc fallback gắn với failure case.
- [ ] Cả 5 thành viên có bản báo cáo/slide riêng để nộp.

**Tự kiểm tra cuối:** Một người không tham gia nhóm có thể nhìn vào từng bản báo cáo/slide, tìm được metric, bằng chứng chạy và quyết định kỹ thuật. Khi phần trình bày đã rõ, hoàn thiện repository chung và lượt nộp cá nhân ở Bước 7.
