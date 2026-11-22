# Hướng dẫn: cảnh 3D điện ảnh chạy theo thao tác cuộn trang

Tài liệu này mô tả đúng cách đã dùng để làm phần mở đầu (hero) của demo trang chủ Fashionista Café: một cảnh 3D dựng trong Blender, kết xuất dò tia thành chuỗi ảnh, rồi cho trình duyệt lật ảnh theo vị trí cuộn. Viết cho một phiên Claude khác đọc và làm theo.

Mã nguồn tham chiếu nằm trong repo `cntkhoi/fashionistacafe`, nhánh `claude/project-thread-z9axq4`, thư mục `website-demo/`:

- `homepage-demo.html`: trang hoàn chỉnh (HTML, CSS, JS trong một file).
- `img/`: ảnh đã xuất.
- `3d-source/`: `build.py`, `stage2.py`, `seq.py`, `process.py`, `coords.py`, các file `jobs*.json`.

Nếu đọc được repo, hãy đọc các file này trước rồi mới viết mã mới.

## 1. Ý tưởng cốt lõi

Không tính 3D trực tiếp trên máy người xem. Thay vào đó:

1. Dựng cảnh trong Blender bằng mã Python (`bpy`), không cần giao diện.
2. Kết xuất bằng Cycles (dò tia) dọc theo một đường máy quay, ra N ảnh tĩnh.
3. Nén ảnh thành WebP.
4. Trên trang, một `<canvas>` được ghim vào màn hình. Vị trí cuộn quyết định vẽ ảnh thứ mấy.

Đây là cách các trang sản phẩm cao cấp làm (chuỗi ảnh lật theo cuộn). Lý do chọn: bản đầu dùng Three.js chạy trực tiếp bị chủ dự án đánh giá là thô, thiếu chất liệu và ánh sáng. Dò tia ngoại tuyến cho phản chiếu, khúc xạ thủy tinh, bóng mềm và độ mờ hậu cảnh thật, mà điện thoại yếu vẫn chạy được vì chỉ phải vẽ ảnh.

Đánh đổi: đổi góc máy, vật thể hay ánh sáng là phải kết xuất lại. Người xem không tự xoay được góc nhìn.

## 2. Yêu cầu chất lượng bắt buộc

Đây là tiêu chuẩn của chủ dự án, không được bỏ qua:

- Phong cách điện ảnh: ánh sáng ấm, tương phản có chủ ý, hậu cảnh mờ, hạt phim nhẹ.
- Chất liệu thật: vải có nếp, thủy tinh khúc xạ, kim loại phản chiếu, gỗ có vân.
- **Không vật thể nào được xuyên qua nhau.** Phải có bước kiểm tra tự động (mục 5).
- Tốc độ tải trang rất quan trọng (mục 8).
- Chuyển động khi cuộn phải mượt (mục 7 và 9).
- Phông chữ: không dùng phông có số kiểu cổ nhảy hàng (Cormorant Garamond, Playfair Display, Bona Nova). Đang dùng Noto Serif Display, EB Garamond, Montserrat, kèm `font-variant-numeric:lining-nums`.

## 3. Môi trường

```bash
pip install bpy pillow numpy      # bpy 5.3.0 = Blender 5.3 dạng thư viện Python
```

- Chạy được trên máy chỉ có CPU (đã chạy trên 4 nhân, không GPU).
- Thư mục làm việc tạm: `/tmp/fc3d/`. Thư mục này mất khi máy bị thu hồi, nên mã phải nằm trong repo.
- Tài nguyên CC0 từ Poly Haven (tải qua `https://api.polyhaven.com/files/<tên>` để lấy đường dẫn file): ghế `dining_chair_02` (gltf, 2k), vân gỗ `herringbone_parquet`, ảnh môi trường `stuttgart_suburbs` (HDRI). Tự dựng bằng mã mọi thứ còn lại.

## 4. Dựng cảnh (`build.py`, rồi `stage2.py`)

Chia hai bước để không phải mô phỏng vải lại mỗi lần chỉnh ánh sáng.

**`build.py` → `stage1.blend`** (hình học và chất liệu):

- Đơn vị là mét, kích thước thật (mặt bàn cao khoảng 0,75 m, đĩa 27 cm, ly cao 20 cm). Kích thước sai là lý do số một khiến cảnh trông giả.
- Vật tròn xoay (đĩa, ly, bình, thân đèn): vẽ biên dạng 2D rồi xoay quanh trục (lathe). Thành ly phải có độ dày thật, không dùng mặt đơn.
- Dao nĩa: khối đặc với tiết diện elip thay đổi dọc chiều dài (cán, cổ, lưỡi). Đừng dùng hộp kéo dài.
- Khăn bàn: lưới đĩa tròn, ghim nhóm đỉnh nằm trên mặt bàn (`vertex_group_mass='pin'`), mô phỏng Cloth 170 khung với va chạm vào mặt bàn, rồi áp dụng modifier và thêm Solidify 1,2 mm. Thông số đã dùng: `quality=7, mass=.25, tension_stiffness=18, bending_stiffness=.35`, tự va chạm bật.
- Sau khi vải rủ xong, lấy cao độ mặt khăn `TZ` làm mặt phẳng đặt đồ. Mọi vật trên bàn được đặt theo `TZ`, không theo số cứng.
- Thủy tinh: Principled BSDF với transmission 1, IOR 1,5. Trộn thêm Transparent BSDF theo `Light Path → Is Shadow Ray` để bóng của ly không đen kịt.
- Kính cửa sổ: dùng Transparent thuần cộng một lớp Glossy mỏng. Kính khúc xạ thật ở cửa sổ gây nhiễu và phản chiếu lạ.

**`stage2.py` → `scene.blend`** (ghế, ánh sáng, máy quay, thiết lập kết xuất, kiểm tra xuyên vật thể):

- Ánh sáng: HDRI ngoài trời cường độ thấp (0,33) làm ánh chạng vạng xanh lạnh qua cửa sổ. Đèn bàn là nguồn phát sáng thật (đĩa LED phát xạ trong chụp đèn). Thêm vài đèn area ấm làm "practical". Tương phản ấm lạnh là thứ tạo cảm giác điện ảnh.
- Hậu cảnh: các quả cầu phát sáng nhỏ ngoài cửa sổ, đặt xa để thành đốm bokeh khi mờ.
- Máy quay: tiêu cự 36 đến 46 mm, bật độ sâu trường ảnh, khẩu f/2,0 đến f/2,8, lấy nét vào một điểm cụ thể trên bàn.
- Thiết lập Cycles đã dùng:

```python
S.cycles.use_denoising=True; S.cycles.denoiser='OPENIMAGEDENOISE'
S.cycles.max_bounces=10; S.cycles.transmission_bounces=10
S.cycles.glossy_bounces=6; S.cycles.transparent_max_bounces=16
S.cycles.caustics_reflective=False; S.cycles.caustics_refractive=False
S.cycles.sample_clamp_indirect=6
S.view_settings.view_transform='AgX'
S.view_settings.look='AgX - Medium High Contrast'
S.render.use_persistent_data=True
```

Khung phim: 1280×960, 44 mẫu, phơi sáng +0,6. Ảnh tĩnh lớn: 1600×1200, 72 đến 96 mẫu.

## 5. Kiểm tra xuyên vật thể (bắt buộc trước mỗi lần kết xuất)

Với mọi cặp vật thể, dựng cây BVH từ lưới đã áp dụng modifier ở tọa độ thế giới và gọi `overlap`. Kết quả phải in ra `INTERSECTIONS 0`.

```python
from mathutils.bvhtree import BVHTree
dg=bpy.context.evaluated_depsgraph_get(); trees={}
for o in S.collection.objects:
    if o.type not in('MESH','CURVE'): continue
    eo=o.evaluated_get(dg); me=eo.to_mesh(); me.transform(o.matrix_world)
    vs=[v.co.copy() for v in me.vertices]; ps=[tuple(p.vertices) for p in me.polygons]
    if ps: trees[o.name]=BVHTree.FromPolygons(vs,ps,epsilon=0.0)
    eo.to_mesh_clear()
bad=[(a,b) for i,a in enumerate(sorted(trees)) for b in sorted(trees)[i+1:]
     if trees[a].overlap(trees[b])]
print('INTERSECTIONS',len(bad))
```

Bản thật trong `stage2.py` có thêm: lọc nhanh bằng hộp bao, và danh sách miễn trừ cho những cặp cố ý chạm nhau (các phần kiến trúc với nhau, chân bàn với mặt bàn, cánh lá của cùng một bông hoa). Danh sách miễn trừ phải ngắn và có lý do.

Cách sửa khi có lỗi: nâng vật lên cho đáy vừa chạm mặt đỡ (tính từ cao độ thấp nhất của lưới), dời vật ra, hoặc sửa biên dạng. Lần đầu có 51 cặp lỗi, sửa về 0 rồi mới kết xuất.

## 6. Đường máy quay và kết xuất chuỗi ảnh (`seq.py`)

- Bốn tư thế máy quay K0 đến K3 (vị trí, điểm nhìn, tiêu cự, điểm lấy nét, khẩu độ), nội suy bằng Catmull-Rom. Ba điểm dừng kể chuyện: đứng ngoài nhìn vào, ngồi xuống bàn, nhìn xuống bộ dao nĩa.
- Tham số hóa theo khung: `u_of(frame)` dùng hàm smootherstep cho từng đoạn, để máy quay khởi động và dừng êm. Hiện tại N=95, điểm chia đoạn `split=64`.
- `seq.py` nhận một JSON danh sách việc, bỏ qua file đã có. Nhờ vậy chạy lại sau khi bị ngắt không mất công.
- Tốc độ: khoảng 2 phút mỗi khung trên CPU 4 nhân. 95 khung mất hơn 2 giờ.
- Muốn tăng gấp đôi số khung mà không kết xuất lại khung cũ: giữ nguyên khung cũ ở chỉ số chẵn, kết xuất khung mới ở chỉ số lẻ với N mới = 2N−1 và split mới = 2×split (xem `jobs-inbetween.json`).

**Lưu ý vận hành quan trọng:** tiến trình chạy nền có thể bị dừng giữa các lượt làm việc. Hãy chạy kết xuất theo từng đợt dưới 10 phút ở tiền cảnh (`timeout 560 python3 seq.py ...`) và lặp lại cho tới khi đủ file. Luôn kiểm tra bằng cách đếm file đầu ra, đừng tin vào việc tiến trình còn sống. Khi viết vòng chờ, đừng dùng `pgrep -f` với mẫu trùng tên chính lệnh chờ.

## 7. Xuất ảnh cho web (`process.py`)

- Thêm quầng sáng nhẹ (bloom): lấy vùng sáng trên ngưỡng, thu nhỏ, làm mờ Gaussian, hòa kiểu screen.
- Khung phim máy tính: 1280×960 WebP chất lượng 66. Khoảng 22 KB mỗi khung.
- Khung phim điện thoại: cắt dọc 720×960 từ cùng ảnh (lấy cột 280 đến 1000), chất lượng 64. Khoảng 15 KB mỗi khung.
- Ảnh mở đầu (đèn bật và đèn tắt): bản lớn hơn, chất lượng 80.
- Tạo một ảnh xem trước siêu nhỏ 40×30 nhúng thẳng vào HTML dạng base64 làm nền trong lúc chờ.
- `coords.py` chiếu tọa độ 3D của vài vật (dao, ly, khăn, đèn) ra tọa độ ảnh để đặt chú thích và nút bấm đúng vị trí. Kết quả ghi vào `CFG` trong HTML.

## 8. Trang web

**Bố cục:**

```css
#hero{height:520vh;position:relative}
.pin{position:sticky;top:0;height:100svh;overflow:hidden}
```

`#hero` cao gấp 5,2 lần màn hình để tạo quãng cuộn. `.pin` chứa `<canvas>` và các lớp chữ, được ghim khi cuộn.

**Từ vị trí cuộn ra khung hình:**

```js
prog = clamp(-heroRect.top/(heroRect.height-innerHeight),0,1);
frameAt = p => smooth(.04,.50,p)*SPLIT + smooth(.62,.90,p)*(N-1-SPLIT);
```

Hai đoạn chuyển động, giữa và hai đầu là quãng nghỉ để chữ hiện lên.

**Vẽ:** vòng `requestAnimationFrame`. Khung hiện tại `fS` đuổi theo khung đích bằng giảm chấn mũ `fS += (target-fS)*(1-exp(-dt*6))`. Vẽ khung `floor(fS)` rồi vẽ đè khung kế tiếp với độ trong suốt bằng phần lẻ. Chỉ vẽ lại khi có thay đổi.

**Tải ảnh:**

- `<link rel="preload">` cho ảnh mở đầu, tách theo `media` máy tính và điện thoại.
- Tải khung theo thứ tự thô đến mịn (bước 16, 8, 4, 2, 1), 6 kết nối song song. Nếu khung cần vẽ chưa về thì dùng khung gần nhất đã có.
- Màn hình chờ có thanh tiến độ và số phần trăm. Trang mở khi đủ ảnh, hoặc sau tối đa 12 giây.
- Ảnh các phần bên dưới dùng `loading="lazy"`.

**Giải nén trước:** trình duyệt giải nén ảnh ngay lúc vẽ lần đầu, gây khựng. Dùng `createImageBitmap` cho các khung từ −3 đến +9 quanh vị trí hiện tại theo hướng cuộn, và giữ tối đa khoảng 22 (điện thoại) đến 30 (máy tính) bitmap, đóng những cái ở xa. Đừng giải nén hết một lượt vì 95 khung chiếm vài trăm MB bộ nhớ.

**Điện thoại:** chọn bộ ảnh `m_` khi tỉ lệ màn hình nhỏ hơn 0,8. Trên màn hình dọc, phim chiếm 68% phía trên, chữ nằm bên dưới.

**Hiệu ứng điện ảnh bằng CSS:** lớp phủ chuyển màu, hạt phim (một ô nhiễu 180 px lặp lại), hai dải đen trên dưới khi máy quay chuyển động, canvas phóng nhẹ và trôi theo chuột. Tôn trọng `prefers-reduced-motion`.

**Dung lượng hiện tại:** phim máy tính khoảng 2,1 MB, điện thoại khoảng 1,4 MB, ảnh đầu tiên khoảng 45 KB (27 KB trên điện thoại).

## 9. Lỗi đã gặp, đừng lặp lại

1. **48 khung cho quãng cuộn dài là không đủ.** Người xem thấy như thiếu khung hình vì hai ảnh hòa mờ vào nhau thành bóng ma. 95 khung là mức đã chấp nhận được. Nếu máy quay đi xa hơn thì cần nhiều hơn.
2. **Không khóa cuộn bằng `overflow:hidden` trên thẻ `html`.** Trên iPhone, sau khi mở khóa, `position:sticky` ngừng hoạt động, khung hình trôi mất và cả đoạn mở đầu chỉ còn nền đen. Thay vào đó chặn `touchmove` và `wheel` bằng `preventDefault` trong lúc chờ. Dùng `overflow-x:clip` thay cho `overflow-x:hidden` trên `body`.
3. **Luôn có cơ chế ghim dự phòng.** Mỗi khung, đo vị trí `.pin`. Nếu đang ở trong vùng hero mà `.pin` không nằm ở đỉnh màn hình thì chuyển sang tự ghim bằng `position:fixed` (và `absolute` ở hai đầu). Xem hàm `measure()` trong `homepage-demo.html`.
4. **Ngưỡng làm tròn.** Biến mờ dần của đèn từng kẹt ở 0,9815 trong khi ngưỡng là 0,985 nên phim không bao giờ vẽ. Khi giá trị cách đích dưới 0,02 thì gán thẳng bằng đích.
5. **Canvas đọc ảnh từ `file://` bị khóa** khi kiểm thử. Chạy `python3 -m http.server` rồi mở qua `http://localhost`.
6. **Phông chữ không tải được trong trình duyệt kiểm thử** nếu mạng bị chặn. Tải file phông về và trả lại qua `page.route` của Playwright, nếu không ảnh chụp sẽ hiện phông dự phòng và đánh giá sai.

## 10. Kiểm thử trước khi giao

Dùng Playwright với Chromium có sẵn:

- Hai khung nhìn: 1440×810 và 400×820.
- Chụp ở các vị trí cuộn 0, 0,3, 0,56, 0,93 của hero và ở từng phần bên dưới. **Tự mở ảnh ra xem**, không chỉ kiểm tra là không có lỗi.
- Bắt `pageerror` và lỗi console.
- Giả lập sticky hỏng bằng cách chèn `<style>#pin{position:relative}</style>` và xác nhận cơ chế dự phòng vẫn giữ khung hình.
- Giới hạn cần nói thật với chủ dự án: trình duyệt giả lập không có GPU nên không đo được độ mượt thật, và Chromium không tái hiện được lỗi riêng của Safari trên iPhone. Nhờ họ thử trên máy thật và quay màn hình nếu có lỗi.

## 11. Thứ tự làm việc gợi ý

1. Chốt câu chuyện máy quay: mấy điểm dừng, mỗi điểm nói gì.
2. `build.py`: dựng hình, chất liệu, mô phỏng vải.
3. `stage2.py`: ánh sáng, máy quay, chạy kiểm tra cho tới khi `INTERSECTIONS 0`.
4. Kết xuất thử 3 ảnh ở ba điểm dừng với số mẫu thấp, mở ra xem, sửa cho tới khi đẹp.
5. Kết xuất cả chuỗi theo từng đợt ngắn.
6. `process.py` xuất WebP, `coords.py` lấy tọa độ chú thích.
7. Ráp trang, kiểm thử như mục 10.
8. Giao kèm danh sách những gì còn là tạm (ví dụ cảnh phố ngoài cửa sổ hiện là ảnh môi trường châu Âu, chưa phải góc phố thật).
