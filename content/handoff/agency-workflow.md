# FC Agency: mô hình làm việc và bàn giao (2026-10-24)

Khôi muốn Claude làm việc như một công ty marketing thật. Tài liệu này là bàn giao từ thread "Viết bài & thiết kế hình ảnh" (đã đóng) sang hai thread mới.

## 1. Sơ đồ tổ chức

```
Khôi (khách hàng / chủ)
  └── CEO (Claude điều phối của project, kênh chính của project)
        ├── Marketing Leader  ── thread "Phòng Marketing: Viết bài"
        │     ├── Researcher       (nguồn gốc món, tên gọi, truyền thuyết, văn học, kỹ thuật)
        │     ├── Planner          (lịch nội dung, chiến dịch theo tháng/quý)
        │     ├── Content Writer VI
        │     ├── Content Writer EN (viết riêng, không dịch)
        │     ├── Editor           (sửa chéo, soát giọng văn, soát chính tả)
        │     └── Social Content Manager (giờ đăng, hashtag, định dạng từng kênh)
        ├── Design Leader     ── thread "Phòng Design: Thiết kế hình ảnh"
        │     ├── Art Director     (concept, moodboard, bố cục)
        │     ├── Photo/AI Image Artist (tạo/chỉnh ảnh)
        │     ├── Graphic Designer (chữ, logo, story, banner, Canva)
        │     └── QA               (đúng chính tả, đúng brand, đúng kích thước)
        ├── (sau này) Performance / Digital Marketing
        └── (sau này) IT Developer: website FC (repo cntkhoi/fashionistacafe)
```
Nhân viên trong mỗi phòng là các agent con do Leader gọi (Agent tool), không phải thread riêng.

## 2. Vòng duyệt (áp dụng cho mọi việc)

1. Khôi giao việc cho CEO.
2. CEO viết brief, giao cho Leader của phòng phù hợp.
3. Leader chia việc cho nhân viên (ai research, ai viết, ai sửa chéo, ai thiết kế).
4. Nhân viên làm, sửa chéo nhau, nộp cho Leader.
5. Leader chấm theo checklist của phòng:
   - Không đạt: ghi rõ lỗi, trả về team, quay lại bước 4.
   - Đạt: gửi lên CEO.
6. CEO chấm:
   - Đạt: ra bản FINAL, gửi Khôi.
   - Không đạt: trả về Leader kèm nhận xét. Leader tự viết một brief sửa mới cho team, quay lại bước 4.

Mỗi lượt chấm ghi lại: vòng số mấy, ai chấm, đạt/không đạt, lý do. Ví dụ với chiến dịch dài (vd tháng 10 đến 12): Leader giao Planner + Researcher mở đầu, hai người làm việc với các nhân viên khác để ra kế hoạch, rồi vào vòng duyệt như trên.

## 3. Thread Viết bài (Marketing)
- Đọc trước khi viết: writing-voice-guide.md (brand-style-template/), competitor-refs/refs.md, posts/visual-style-refs.md, memory fc-writing-voice.
- Quy trình bắt buộc của Khôi: research → đề xuất 2-3 hướng câu chuyện → gửi Khôi câu hỏi và CHỜ trả lời → viết → tự soát.
- Đầu ra mỗi bài: tên món theo cú pháp menu, caption VI, caption EN (viết riêng), hashtag, và một **Design Brief** cho phòng Design.
- Lưu: /mnt/project-files/posts/<slug>/caption.md và repo content/<slug>/.

### Mẫu Design Brief (Marketing → Design)
```
Bài: <tên>  | Kênh/kích thước: <FB 4:5, story 9:16...> | Ngày đăng: <...>
Thông điệp chính: <1 câu>
Chữ trên ảnh (nếu có, đã duyệt chính tả): <...>
Ảnh thật cần dùng: assets/photos/<thư mục>/<file> (hoặc "chưa có, cần tạo AI")
Mood: <ánh sáng, màu, đạo cụ kể chuyện>
Bố cục: <1 hero + 2-3 phụ / 1 ảnh đơn / story>
```

## 4. Thread Thiết kế (Design)
- Nhận Design Brief từ thread Viết bài (qua CEO hoặc trực tiếp), và yêu cầu riêng của Khôi.
- Quy tắc hình ảnh: posts/visual-style-refs.md và memory fc-visual-style (low-key, một nguồn sáng xiên, wordmark nhỏ màu kem, không chữ trên ảnh món).
- Ưu tiên ảnh thật trong folder Mac /Users/nkblu/Documents/Dev/fashionistacafe/assets/photos/ (space, dishes, drinks, team, events, sets/<set>). Folder này KHÔNG phải git clone; đọc bằng folder tools, commit lên repo từ container.
- Lưu: /mnt/project-files/posts/<slug>/design.md (link ảnh, link Canva, job id) và repo.

### Kinh nghiệm công cụ (đã thử 2026-10-20)
- Higgsfield gpt_image_2_5 (9:16, quality high, 2k): ảnh đẹp, chữ đúng. Container KHÔNG tải được ảnh từ CDN cloudfront (proxy chặn) và không tự xem được ảnh.
- Cách làm được: Canva upload-asset-from-url (lấy thẳng link cloudfront) → separate-image-layers (tách chữ thành lớp chỉnh được) → read-design (xem thumbnail và đọc chữ để soát chính tả). Gửi Khôi link canva.link.
- Credits Higgsfield còn khoảng 46 (gói starter) lúc 2026-10-20; mỗi lần tạo nên 2 phương án.

## 5. Việc đã làm ở thread cũ
- Ghi chú phong cách hình ảnh: posts/visual-style-refs.md
- Story 20/10: posts/2026-10-20-womens-day/story.md (Canva: https://canva.link/4s3lr2oad6jjuzp, https://canva.link/zuyrz9ji327ghry)
- Tuna Tartare: posts/dishes/tuna-tartare.md (viết trước khi có quy trình research; nên làm lại theo quy trình mới nếu Khôi muốn)
- Bộ khung style guide cho brand khác: brand-style-template/brand-style-guide.md
