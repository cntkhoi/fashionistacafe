# Bộ skill phòng Design FC

Mỗi vị trí có một file skill riêng. Khi Design Leader gọi một agent, prompt của agent đó chỉ gồm:
1. File skill của đúng vị trí đó (không nạp file của vị trí khác, không nạp nguyên brand guide).
2. Brief của job.
3. Đúng các file đầu vào job cần (ảnh, bản nháp trước, nhận xét vòng trước).

Agent chỉ làm phần "Làm", gặp việc ở mục "Không làm" thì ghi lại và trả về Leader, không tự làm thay. Mục tiêu: mỗi agent gọn, đúng chuyên môn, không tốn token đọc thứ không cần.

| File | Vị trí | Gọi khi |
|---|---|---|
| design-leader.md | Design Leader (thread phòng Design) | luôn luôn |
| art-director.md | Art Director | đầu mỗi job, và khi CEO trả về vì concept |
| image-artist.md | Photo Researcher / AI Image Artist | cần chọn ảnh thật hoặc tạo ảnh AI |
| photo-retoucher.md | Photo Retoucher | ảnh thật cần chỉnh màu, crop, làm sạch |
| layout-typography.md | Layout & Typography Designer | dựng chữ, logo, xuất file |
| qa-reviewer.md | QA Reviewer | trước khi nộp Leader, mỗi vòng |

Khi cần thêm Motion Designer hoặc Print Designer, viết thêm file cùng khuôn: Vai trò / Làm / Không làm / Đầu vào / Đầu ra / Kỹ năng chuyên môn / Tự soát / Nguồn.

Research 2026-10-24, nguồn ghi ở cuối từng file.
