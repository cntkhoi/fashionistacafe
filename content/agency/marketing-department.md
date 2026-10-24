# Phòng Marketing FC: cơ cấu, vai trò và quy trình duyệt bài

> Thiết lập 24/10/2026 theo mô hình "văn phòng marketing thực thụ" Khôi đề ra.
> Phòng này chạy trong thread **Viết bài cho FC**. Thiết kế hình ảnh chạy ở thread **Thiết kế hình ảnh cho FC**.
> Mọi bài phải theo: [writing-voice-guide.md](../brand-style-template/writing-voice-guide.md), [brand-style-guide.md](../brand-style-template/brand-style-guide.md), [refs đối thủ](../competitor-refs/refs.md).

---

## 1. Sơ đồ

```
Khôi (chủ)
  └── CEO (Claude tổng, project chat)
        ├── Marketing Leader  ← thread "Viết bài cho FC"
        │     ├── Researcher (nghiên cứu nội dung)
        │     ├── Planner (kế hoạch, lịch đăng)
        │     ├── Content Writer VI
        │     ├── Content Writer EN
        │     ├── Cross-editor / Brand Reviewer (sửa chéo)
        │     ├── Social Content Manager (định dạng kênh, hashtag, lịch)
        │     └── Performance & Digital Marketer (khi chạy chiến dịch, quảng cáo)
        ├── Design Leader     ← thread "Thiết kế hình ảnh cho FC"
        │     └── (art director, photo editor, layout designer, motion...)
        └── IT / Web Leader   (sau này: website FC từ repo cntkhoi/fashionistacafe)
```

Khôi chỉ nói chuyện với CEO (hoặc trực tiếp vào thread phòng ban khi muốn). Marketing Leader nhận việc từ CEO, chia việc cho team, duyệt, rồi nộp lên.

---

## 2. Vai trò trong phòng Marketing

| Vai trò | Làm gì | Đầu ra |
|---|---|---|
| **Marketing Leader** | Nhận việc từ CEO, viết brief, chia việc, gửi câu hỏi cho Khôi, chấm đạt/không đạt, viết brief sửa khi trượt, nộp CEO, chuyển bài final sang phòng Design | Brief, phiếu chấm, bài nộp |
| **Researcher** | Bước 1 của quy trình viết: nguồn gốc, ý nghĩa tên, điển tích, văn chương Pháp/Việt, khoa học kỹ thuật, cầu nối Pháp Việt. Tách rõ sự thật và truyền thuyết, ghi nguồn | research.md |
| **Planner** | Với chiến dịch: mục tiêu, trụ nội dung, lịch đăng theo tuần, tỉ lệ dạng bài, dịp lễ, phối hợp với Researcher | plan.md |
| **Content Writer VI** | Viết bản tiếng Việt theo khung 6 nhịp, lối Floraison + refs đối thủ | caption VI |
| **Content Writer EN** | Viết bản tiếng Anh riêng (không dịch), gọn, understated | caption EN |
| **Cross-editor / Brand Reviewer** | Sửa chéo hai bản, chạy checklist tự kiểm (mục 7 bước 5 của voice guide), soát từ cấm, kiểm chứng chi tiết | bản sửa + ghi chú |
| **Social Content Manager** | Ghép caption hoàn chỉnh (VI — EN — thành phần — hashtag), đề xuất ảnh/bố cục cho Design, giờ đăng | bài đăng sẵn sàng |
| **Performance & Digital** | Chỉ khi có chiến dịch/quảng cáo: kênh, ngân sách, chỉ số đo, biến thể A/B, vẫn giữ giọng không bán hàng | đề xuất phân phối |

Mỗi nhân viên là một agent con do Marketing Leader giao brief. Không phải bài nào cũng cần đủ người: bài lẻ dùng Researcher, 2 Writer, Cross-editor; chiến dịch thêm Planner, Social, Performance.

---

## 3. Quy trình một bài viết

```
CEO giao việc
  → Leader viết brief, giao Researcher
  → Researcher nộp research + 2–3 góc kể
  → Leader gửi Khôi: góc kể + 9 câu hỏi cố định + 2–4 câu riêng   ⟵ DỪNG, CHỜ KHÔI TRẢ LỜI
  → Writer VI + Writer EN viết song song từ câu trả lời của Khôi
  → Cross-editor sửa chéo, chạy checklist
  → Leader chấm (vòng Leader)
        Không đạt → Leader viết brief sửa mới → team sửa → chấm lại
        Đạt → nộp CEO
  → CEO chấm (vòng CEO)
        Không đạt → trả Leader → Leader ra brief sửa mới cho team → lặp lại
        Đạt → FINAL
  → Final gửi Khôi + chuyển sang thread Thiết kế hình ảnh cho FC
  → Lưu: /mnt/project-files/posts/<slug>/ và repo content/<slug>/
```

## 4. Quy trình một chiến dịch (ví dụ: chiến dịch tháng 10 đến tháng 12)

1. CEO giao Leader. Leader viết brief chiến dịch (mục tiêu, thời gian, dịp lễ, ràng buộc thương hiệu).
2. **Planner + Researcher** làm trước: bối cảnh mùa vụ, dịp lễ (Halloween, Noël, Giao thừa dương lịch, mùa nấm truffle, mùa rượu Beaujolais Nouveau...), chủ đề series, lịch đăng theo tuần.
3. Planner trao đổi với Social và Performance để chốt kênh, tần suất, dạng bài; với Writer để chốt giọng từng series.
4. Leader gửi Khôi các câu hỏi chiến lược (mục tiêu kinh doanh, món/sự kiện chắc chắn có, ngân sách) và chờ trả lời.
5. Team hoàn thiện kế hoạch → vòng Leader → vòng CEO như trên.
6. Kế hoạch được duyệt thì mỗi bài trong lịch chạy theo quy trình mục 3.

---

## 5. Phiếu chấm (dùng cho cả vòng Leader và CEO)

Đạt khi **không có lỗi chặn** và **điểm ≥ 8/10**.

**Lỗi chặn (một lỗi là trượt):**
- Chi tiết bếp không có trong câu trả lời của Khôi (bịa)
- Sai sự thật lịch sử/văn chương, hoặc truyền thuyết không ghi "tương truyền"
- Có emoji, lời mời, từ bán hàng, tính từ rỗng, khen bát đĩa
- Bản EN là bản dịch của bản VI
- Câu chuyện không dẫn về tinh thần Pháp Việt

**Thang điểm (10):**
| Tiêu chí | Điểm |
|---|---|
| Câu chuyện gốc có sức nặng, khớp chủ đề | 2 |
| Mô tả theo lớp, ≥ 3 chi tiết cảm giác cụ thể, có kỹ thuật thật | 2 |
| Nhịp câu, staccato, câu kết suy ngẫm đứng riêng | 2 |
| Bản EN tự nhiên, gọn, understated | 2 |
| Khối thành phần đúng cú pháp menu, hashtag đúng | 1 |
| Cảm giác tổng thể Quiet Luxury, người kể lặng lẽ | 1 |

**Brief sửa khi trượt** phải ghi: lỗi cụ thể (trích câu), vì sao trượt theo tiêu chí nào, hướng sửa, ai sửa, và điều giữ nguyên.

---

## 6. Bàn giao sang phòng Design

Gói gửi thread **Thiết kế hình ảnh cho FC** là caption final kèm một **Design Brief** (mẫu thống nhất với phòng Design, theo [handoff/agency-workflow.md](../handoff/agency-workflow.md)):

```
Bài: <tên>  | Kênh/kích thước: <FB 4:5, story 9:16...> | Ngày đăng: <...>
Thông điệp chính: <1 câu>
Chữ trên ảnh (nếu có, đã duyệt chính tả): <...>
Ảnh thật cần dùng: assets/photos/<thư mục>/<file> (hoặc "chưa có, cần tạo AI")
Mood: <ánh sáng, màu, đạo cụ kể chuyện>
Bố cục: <1 hero + 2-3 phụ / 1 ảnh đơn / story>
```

Quy tắc hình ảnh tham chiếu: [visual-style-refs.md](../posts/visual-style-refs.md).

## 7. Nhật ký duyệt

Mỗi bài có file `/mnt/project-files/posts/<slug>/review-log.md`, mỗi lượt chấm một dòng: vòng số mấy, ai chấm (Leader/CEO), đạt/không đạt, điểm, lý do, brief sửa (nếu có).

## 8. Việc tồn

- `posts/dishes/tuna-tartare.md` được viết trước khi có quy trình research. Làm lại theo quy trình mới nếu Khôi muốn.
