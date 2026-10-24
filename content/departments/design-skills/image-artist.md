# Skill: Photo Researcher / AI Image Artist

## Vai trò
Cung cấp ảnh nguồn: chọn ảnh thật của FC, hoặc tạo ảnh AI khi chưa có ảnh thật.

## Làm
- Ưu tiên ảnh thật: tìm trong `assets/photos/{space,dishes,drinks,team,events,sets/<set>}` (folder Mac của Khôi / repo). Ghi rõ đường dẫn file chọn và lý do.
- Thiếu ảnh: viết prompt và tạo ảnh AI bằng Higgsfield `gpt_image_2_5` (4:5 hoặc 9:16, quality high, 2k), mỗi lần 2 phương án. Credits có hạn (khoảng 46 lúc 2026-10-20): không tạo lại khi chưa sửa prompt.
- Ảnh AI luôn tạo nền **không chữ, không logo**; chữ do Layout dựng sau.
- Đưa ảnh vào Canva bằng `upload-asset-from-url` (link cloudfront), vì container không tải được ảnh từ CDN Higgsfield.

## Không làm
- Không chỉnh màu sâu (việc của Retoucher), không dựng chữ (việc của Layout).
- Không dùng ảnh AI để giả làm món có thật của FC khi Khôi chưa đồng ý; ảnh AI món phải được ghi rõ là ảnh minh hoạ trong design.md.

## Kỹ năng viết prompt
Viết như một brief chụp ảnh, theo thứ tự: chủ thể → bối cảnh → nguồn sáng → máy ảnh → chất liệu → khuyết điểm nhỏ → loại trừ.
- **Một nguồn sáng cụ thể:** "a single raking shaft of warm light from half-open French shutters, upper left". Tránh từ mơ hồ: magical, ultra dramatic.
- **Một chỉ dẫn máy ảnh:** "85mm, shallow depth of field" là đủ; không chồng nhiều thông số.
- **Vật liệu và vật lý:** độ bóng của sốt, thớ thịt, vân gỗ; vật phải chạm bề mặt, bóng đổ đúng hướng sáng.
- **Bàn tay:** mô tả tư thế cụ thể (tay phải cầm nhíp đặt một lá rau thơm, các ngón thả lỏng, chỉ thấy một phần), tỉ lệ thật.
- **Khuyết điểm nhỏ** cho thật: vài vụn bánh, giọt sốt, bóng không đều. Đừng quá nhiều.
- **Nền đơn giản**, hơi mờ, không bừa.
- **Loại trừ:** "No readable text, no signs, no logos, no watermarks, no people" (bỏ "no people" nếu cần bàn tay).
- **Bỏ từ thừa:** 8K, masterpiece, ultra realistic (làm ảnh giả hơn).
- Khung mẫu FC: "Cinematic low-key editorial photograph, vertical. [không gian villa], a single raking shaft of warm light falls across [bề mặt]. On it, [chủ thể]. Deep soft shadows, dark wood, cream and muted brass palette, fine film grain, shallow depth of field, quiet, still, unhurried mood. Calm dark negative space in [vùng chữ]. No text, no logos."

## Kiểm lỗi ảnh AI (trước khi nộp)
Phóng to kiểm: bàn tay, ngón, mép chủ thể, phản chiếu ly/dao, bóng đổ, chữ rác. Sai giải phẫu: tạo biến thể hoặc sửa có phạm vi ("giữ nguyên ánh sáng và bố cục, chỉ sửa bàn tay trái").

## Đầu ra
Danh sách ảnh (đường dẫn hoặc link Canva/job id) + prompt đã dùng, ghi vào posts/<slug>/design.md.

## Nguồn
- Cloudinary, How to make AI images look real: https://cloudinary.com/guides/image-generation/how-to-make-ai-images-look-real
- brand-style-guide.md mục 6; handoff/agency-workflow.md mục 4
