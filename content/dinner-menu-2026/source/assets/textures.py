import numpy as np
from scipy import ndimage as nd
from PIL import Image
import sys
out = sys.argv[1]
rng = np.random.default_rng(7)

def noise(h, w, sy, sx):
    return nd.gaussian_filter(rng.standard_normal((h, w)), (sy, sx), mode='wrap')

def norm(a):
    a = a - a.mean(); return a / (a.std() + 1e-9)

# ---------- PAPER (cold-press, ~420dpi on 141.5x217.7mm) ----------
H, W = 3600, 2340
h = (norm(noise(H, W, 5, 11)) * 1.0 + norm(noise(H, W, 2.5, 5)) * .55 +
     norm(noise(H, W, 12, 26)) * .6 + norm(noise(H, W, 1.0, 1.4)) * .18)
gy, gx = np.gradient(h)
# light from top-left
shade = -(gy * .85 + gx * .35)
shade = norm(shade)
shade = np.clip(shade, -3.5, 3.5)
base = np.array([238.0, 236.6, 231.6])
amp = np.where(shade < 0, 6.5, 3.2)  # shadows deeper than highlights
img = base[None, None, :] + (shade * amp)[..., None] * np.array([1.0, 1.0, 1.06])[None, None, :]
# gentle large-scale tone variation
img += norm(noise(H, W, 300, 300))[..., None] * 1.2
Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).save(f'{out}/paper.jpg', quality=93)

# ---------- CIRCLES ----------
D = 2200
yy, xx = np.mgrid[0:D, 0:D].astype(np.float32)
r = np.hypot(xx - D / 2, yy - D / 2) / (D / 2)

def streaks(angles, scale=1.0):
    acc = np.zeros((D, D), np.float32)
    for ang, wgt in angles:
        n = rng.standard_normal((D, D)).astype(np.float32)
        n = nd.gaussian_filter(n, 1.2)
        n = nd.rotate(n, ang, reshape=False, mode='wrap', order=1)
        n = nd.gaussian_filter(n, (0.8 * scale, 14 * scale))
        n = nd.rotate(n, -ang, reshape=False, mode='wrap', order=1)
        acc += norm(n) * wgt
    return norm(acc)

def edge(alpha_soft=1.5):
    return np.clip((1 - r) * D / 2 / alpha_soft, 0, 1)

def rim_shade(strength):  # darker toward the rim -> slight sphere/inset feel
    return 1 - strength * np.clip((r - .55) / .45, 0, 1) ** 2.2

# charcoal stone: scratchy grey strokes in crossing directions
s = streaks([(25, 1.0), (-35, .8), (70, .5)])
fine = norm(nd.gaussian_filter(rng.standard_normal((D, D)), .7))
m = np.clip((s - .35) * .9 + fine * .12, 0, 1.6)
v = 28 + m * 70
v = v * rim_shade(.55)
stone = np.stack([v, v * 1.0, v * 1.02], -1)
a = edge()
Image.fromarray(np.dstack([np.clip(stone, 0, 255), a * 255]).astype(np.uint8), 'RGBA').save(f'{out}/circle_stone.png')

# blue water marble: horizontal wavy bands, domain-warped
wx = norm(nd.gaussian_filter(rng.standard_normal((D, D)), 60)) * 38
wy = norm(nd.gaussian_filter(rng.standard_normal((D, D)), 60)) * 18
base_n = nd.gaussian_filter(rng.standard_normal((D, D)), (5, 42), mode='wrap')
base_n = nd.map_coordinates(base_n, [yy + wy, xx + wx], order=1, mode='wrap')
mid = nd.gaussian_filter(rng.standard_normal((D, D)), (2, 16), mode='wrap')
mid = nd.map_coordinates(mid, [yy + wy * .5, xx + wx * .5], order=1, mode='wrap')
f = norm(norm(base_n) + norm(mid) * .55 + fine * .12)
t = np.clip((f + .2) / 1.5, 0, 1)
t = t ** 1.15
deep = np.array([22, 44, 88.0]); midc = np.array([52, 92, 158.0]); light = np.array([150, 186, 228.0])
col = np.where(t[..., None] < .55,
               deep + (midc - deep) * (t[..., None] / .55),
               midc + (light - midc) * ((t[..., None] - .55) / .45))
col = col * rim_shade(.5)[..., None]
Image.fromarray(np.dstack([np.clip(col, 0, 255), a * 255]).astype(np.uint8), 'RGBA').save(f'{out}/circle_water.png')
print('done')
