import numpy as np, math, sys
from scipy import ndimage as nd
from PIL import Image, ImageDraw, ImageFilter
out = sys.argv[1]
rng = np.random.default_rng(11)
D = 2112
def norm(a):
    a = a - a.mean(); return a / (a.std() + 1e-9)
def gn(s, shape=(D, D)):
    return norm(nd.gaussian_filter(rng.standard_normal(shape), s, mode='wrap'))

yy, xx = np.mgrid[0:D, 0:D].astype(np.float32)
r = np.hypot(xx - D / 2 + .5, yy - D / 2 + .5) / (D / 2)
alpha = np.clip((1 - r) * D / 2 / 1.6, 0, 1)
fine = gn(.8)
crumple = gn(3)  # crumpled-paper micro relief
gy, gx = np.gradient(gn(4) + .5 * gn(9))
relief = norm(-(gy + .4 * gx))

# ---------- charcoal stone: hand-scratched short strokes ----------
img = Image.new('L', (D, D), 0)
dr = ImageDraw.Draw(img)
ang_field = gn(140) * 1.4 + 0.5
dens = gn(60)
N = 150000
xs = rng.uniform(0, D, N); ys = rng.uniform(0, D, N)
for x, y in zip(xs, ys):
    ix, iy = int(x) % D, int(y) % D
    if dens[iy, ix] + rng.normal(0, .8) < -1.0:
        continue
    a = ang_field[iy, ix] + rng.normal(0, .55)
    L = rng.uniform(6, 26)
    dx, dy = math.cos(a) * L / 2, math.sin(a) * L / 2
    v = int(rng.uniform(80, 200))
    dr.line([(x - dx, y - dy), (x + dx, y + dy)], fill=v, width=int(rng.choice([1, 2, 2, 3])))
strokes = np.asarray(img.filter(ImageFilter.GaussianBlur(.5)), np.float32) / 255
strokes = np.clip(strokes * (0.75 + .25 * fine), 0, 1)
blotch = np.clip(.75 + .25 * gn(35), .35, 1)
v = 26 + strokes * 125 * blotch + relief * 5 + fine * 4
rim = 1 - .5 * np.clip((r - .6) / .4, 0, 1) ** 2
v = v * rim
stone = np.stack([v * .98, v, v * 1.03], -1)

# ---------- blue water marble ----------
wx = gn(60) * 55; wy = gn(50) * 22
b = nd.gaussian_filter(rng.standard_normal((D, D)), (8, 40), mode='wrap')
b = nd.map_coordinates(b, [yy + wy, xx + wx], order=1, mode='wrap')
m = nd.gaussian_filter(rng.standard_normal((D, D)), (2.5, 13), mode='wrap')
m = nd.map_coordinates(m, [yy + wy * .6, xx + wx * .6], order=1, mode='wrap')
f = norm(norm(b) + .5 * norm(m))
edge_noise = fine * .35 + crumple * .25
dark = np.clip((-(f + edge_noise) + .05) * 2.4, 0, 1)        # rough dark patches
light_mix = np.clip((f + edge_noise * .6 + .6) / 1.8, 0, 1)
lightc = np.array([96, 140, 204.0]); paler = np.array([140, 178, 228.0])
deep = np.array([24, 48, 92.0]); midc = np.array([44, 82, 140.0])
light_layer = lightc + (paler - lightc) * light_mix[..., None]
dark_layer = deep + (midc - deep) * np.clip(.5 + .5 * fine, 0, 1)[..., None]
col = light_layer * (1 - dark[..., None]) + dark_layer * dark[..., None]
col = col + (relief * 7 + fine * 4)[..., None]
rimw = 1 - .55 * np.clip((r - .62) / .38, 0, 1) ** 2
col = col * rimw[..., None]

# ---------- compose (geometry measured from original: sep = 0.739 D) ----------
sep = int(round(D * 260 / 352)); pad = 24
W = D + 2 * pad; H = D + sep + 2 * pad
canvas = np.zeros((H, W, 4), np.float32)
def place(rgb, a, top):
    sl = canvas[top:top + D, pad:pad + D]
    src = np.dstack([rgb, a])
    oa = sl[..., 3:4]; na = a[..., None]
    outa = na + oa * (1 - na)
    sl[..., :3] = (rgb * na + sl[..., :3] * oa * (1 - na)) / np.maximum(outa, 1e-6)
    sl[..., 3:4] = outa
place(stone, alpha, pad)
# soft shadow of the blue disc onto the stone, then blue disc slightly translucent where it overlaps
sh = nd.gaussian_filter(alpha, 30)
top2 = pad + sep
region = canvas[top2 - 30:top2 - 30 + D, pad:pad + D]
region[..., :3] *= (1 - .45 * sh)[..., None]
sl = canvas[top2:top2 + D, pad:pad + D]
under = sl[..., :3].copy(); ua = sl[..., 3:4].copy()
op = np.where(ua[..., 0] > 0, .68, 1.0) * alpha
mixed = col * op[..., None] + under * (1 - op[..., None]) * ua
sl[..., :3] = np.where(alpha[..., None] > 0, mixed / np.maximum(op[..., None] + ua * (1 - op[..., None]), 1e-6), sl[..., :3])
sl[..., 3:4] = np.maximum(ua, alpha[..., None])
Image.fromarray(np.clip(canvas, 0, 255).astype(np.uint8) if False else np.dstack([np.clip(canvas[..., :3], 0, 255), np.clip(canvas[..., 3] * 255, 0, 255)]).astype(np.uint8), 'RGBA').save(f'{out}/circles_hi.png')
print(W, H)
