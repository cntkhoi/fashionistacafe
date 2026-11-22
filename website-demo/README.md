# Demo trang chủ mới (ý tưởng)

`homepage-demo.html` là bản demo ý tưởng cho trang chủ mới của Fashionista Café. Bản này tách riêng, không liên quan tới website WordPress đang chạy.

## Cách làm (bản 2)
- Cảnh bàn ăn dựng trong Blender 5.3 bằng script (`3d-source/build.py`): khăn bàn mô phỏng vải, ly pha lê, dao nĩa bạc, đèn đồng, hoa, ghế da (Poly Haven, CC0), sàn gỗ xương cá, tường ốp phào. `3d-source/stage2.py` thêm ánh sáng, camera và chạy kiểm tra giao cắt giữa mọi cặp vật thể (phải ra `INTERSECTIONS 0`).
- Render bằng Cycles (ray tracing) thành 48 khung hình chuyển động máy quay + ảnh tĩnh (`3d-source/seq.py`, `jobs.json`, `extras.json`), hậu kỳ và xuất WebP bằng `process.py` vào `img/`.
- Trang web chỉ phát lại các khung hình theo vị trí cuộn trên một canvas, nên nhẹ: ảnh đầu khoảng 100 KB, toàn bộ phim khoảng 1,1 MB (máy tính) hoặc 0,7 MB (điện thoại), tải từ thô tới mịn.
- Cảnh phố ngoài cửa sổ là HDRI minh hoạ (Poly Haven), câu chữ là tạm thời.

File HTML là nội dung trang (không có thẻ html/head/body) để xuất bản dạng Artifact; ảnh nằm trong `img/`.
