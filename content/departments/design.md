# Phòng Design · Fashionista Café (FC)

Thiết lập 2026-10-24. Phòng Design nhận bài viết đã final từ phòng Viết bài (thread "Viết bài cho FC") hoặc yêu cầu trực tiếp từ Khôi qua CEO, rồi làm hình ảnh cho bài.

Tài liệu gốc phải đọc trước mỗi job:
- `/mnt/project-files/brand-style-template/brand-style-guide.md` (mục 3, 4, 6, 7)
- `/mnt/project-files/posts/visual-style-refs.md`
- `/mnt/project-files/competitor-refs/refs.md` (khi cần tham chiếu bố cục đối thủ)

---

## 1. Sơ đồ

```
Khôi
 └── CEO (Claude tổng, project chat)
      ├── Marketing Leader  ── phòng Viết bài ──┐  bài final
      └── Design Leader (thread này) ◄──────────┘
           ├── Art Director
           ├── Photo Researcher / Image Generator
           ├── Photo Retoucher
           ├── Layout & Typography Designer
           └── QA Reviewer (soát chéo)
```

## 2. Vai trò

| Vai trò | Việc chính | Đầu ra |
|---|---|---|
| **Design Leader** | Đọc bài final, viết brief thiết kế, chia việc, chấm đạt / không đạt, trình CEO | Brief, bản chấm điểm, bộ file nộp CEO |
| **Art Director** | Chọn concept hình: mạch kể (nguyên liệu → bàn tay → thành phẩm), bố cục (hero + ảnh phụ / ảnh đơn / story), ánh sáng, bảng màu | Moodboard + 2 đến 3 hướng concept |
| **Photo Researcher / Image Generator** | Chọn ảnh thật của Khôi trong `assets/photos/...`; nếu thiếu thì viết prompt và tạo ảnh AI (không chữ, không logo) | Danh sách ảnh dùng / ảnh AI kèm prompt |
| **Photo Retoucher** | Chỉnh màu về low-key, một nguồn sáng, crop đúng tỉ lệ, làm sạch | Ảnh đã chỉnh, đúng kích thước |
| **Layout & Typography Designer** | Dựng chữ, logo, gradient, vùng an toàn; xuất file | PNG cuối 1080x1350 (feed), 1080x1920 (story), 1080x1080 (nếu cần) |
| **QA Reviewer** | Soát chéo theo checklist mục 5 trước khi nộp Leader; không phải người đã làm file đó | Danh sách lỗi hoặc "đạt" |

Vai trò bổ sung khi có nhu cầu: Motion Designer (video dọc ngắn, reels), Print Designer (menu, thẻ series, thiệp in).

## 3. Quy trình

1. **Nhận đầu vào.** Bài final từ phòng Viết bài (caption VI/EN, dạng bài, ý chính về hình) hoặc yêu cầu của Khôi. Thiếu ảnh gốc hay chưa rõ dạng bài thì Leader hỏi Khôi một lần, gom hết câu hỏi.
2. **Brief.** Leader viết brief theo mẫu mục 4 và giao cho Art Director.
3. **Concept.** Art Director ra 2 đến 3 hướng. Leader chọn một (hoặc trình Khôi chọn nếu hướng đi thay đổi mục tiêu bài).
4. **Sản xuất.** Researcher/Generator lo ảnh → Retoucher chỉnh → Layout dựng chữ và xuất file.
5. **Soát chéo.** QA Reviewer chấm theo checklist, trả lỗi về đúng người làm.
6. **Leader duyệt.**
   - Đạt: gửi lên CEO.
   - Không đạt: Leader ghi rõ lỗi, giao lại đúng khâu, quay lại bước 4.
7. **CEO duyệt.**
   - Đạt: file ra **final**, giao Khôi.
   - Không đạt: trả về Leader. Leader **viết brief mới** (nêu điều CEO yêu cầu, điều giữ, điều đổi), giao lại team, quay lại bước 3 hoặc 4, rồi lặp lại bước 5 đến 7.
8. **Lưu trữ.** File final lưu ở `/mnt/project-files/posts/<bài>/design/` và commit vào repo `content/<bài>/design/` (nguồn cho website FC sau này).

Mỗi vòng có ghi lại: phiên bản (v1, v2...), ai làm, kết quả chấm, lý do.

## 4. Mẫu brief thiết kế

```
Bài: [tên bài / slug]            Dạng: [món / nguyên liệu / con người / không gian / thông báo / dịp lễ]
Kênh & định dạng: [FB/IG feed 4:5, story 9:16, carousel N ảnh]
Ý chính của caption (1 câu): [...]
Staccato của bài: [Ba. Từ. Này.]
Mạch hình: [hero = ... / phụ 1 = cận kết cấu ... / phụ 2 = bàn tay ... / phụ 3 = nguyên liệu ...]
Ánh sáng & màu: low-key, một nguồn sáng xiên từ [cửa chớp / đèn đơn], màu mạnh chỉ từ [món]
Nền / chất liệu kể chuyện: [...]
Chữ trên ảnh: [không có ngoài logo / có: nội dung chính xác]
Logo / Michelin: [vị trí; có dùng tem Michelin Selected không]
Nguồn ảnh: [ảnh thật: đường dẫn / ảnh AI: prompt gốc]
Tham chiếu: [ref #.. trong refs.md]
Hạn: [...]
```

## 5. Checklist chấm điểm (đạt khi không có lỗi ở mục bắt buộc)

**Bắt buộc**
- [ ] Ảnh low-key, một nguồn sáng, bóng đổ sâu; màu mạnh chỉ đến từ sản phẩm hoặc nền có chủ đích
- [ ] Ảnh món không có chữ ngoài logo: không giá, không CTA, không sticker, không icon
- [ ] Logo FC wordmark nhỏ, màu kem `#F2EADF`, đúng vị trí và giống nhau giữa các ảnh
- [ ] Không khoe bát đĩa, đạo cụ thừa
- [ ] Chữ (nếu có) đúng chính tả, đúng dấu tiếng Việt, khớp từng chữ với bài final, nằm trong vùng an toàn (story chừa 250px trên/dưới)
- [ ] Đúng kích thước và tỉ lệ kênh
- [ ] Ảnh AI không lỗi giải phẫu (bàn tay, ngón), không chữ rác, không logo lạ

**Chất lượng**
- [ ] Bố cục kể đúng mạch nguyên liệu → bàn tay → thành phẩm (với carousel)
- [ ] Typography: tối đa 2 font, serif mảnh (Cormorant Garamond / Playfair Display), nhãn phụ in hoa giãn chữ 0.2 đến 0.3em, staccato serif nghiêng
- [ ] Bảng màu thiết kế: Kem `#F2EADF`, Vàng mờ `#B89A6A`, Nâu đen `#1A1410`
- [ ] Cảm giác chung: Quiet Luxury, Cinematic, tĩnh, chậm. Nhìn vào thấy villa Pháp, không thấy quảng cáo
- [ ] Tem Michelin Selected dùng tiết chế (chỉ hero hoặc bài thương hiệu)

## 6. Công cụ

- **Ảnh thật:** thư mục `assets/photos/{space,dishes,drinks,team,events,sets/...}` trên máy Khôi / repo.
- **Ảnh AI:** Higgsfield (generate_image); prompt theo mẫu mục 6 của brand guide. Tạo nền không chữ trước, dựng chữ sau.
- **Dựng chữ & xuất file:** HTML/CSS render bằng trình duyệt hoặc Python (Pillow) với font Cormorant Garamond / Playfair Display; Canva khi kết nối hoạt động (hiện kết nối Canva trong phiên này đang lỗi).
- **Trình bày để duyệt:** trang xem trước gom các phiên bản cạnh nhau.

## 7. Bàn giao giữa các phòng

- Phòng Viết bài gửi sang: caption final VI/EN, dạng bài, gợi ý hình (nếu có), đường dẫn file bài.
- Phòng Design gửi lại: link file final, ghi chú nếu hình cần chỉnh caption (ví dụ số ảnh thay đổi).
