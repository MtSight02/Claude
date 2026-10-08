"""Tiny pixel-art rendering engine (numpy).

Everything is drawn at the native 360x640 resolution and upscaled 3x with
nearest-neighbour at encode time, so every "pixel" stays crisp.
Gradients, light and transparency are ordered-dithered (8x8 Bayer) instead of
blended smoothly, which is what gives the 16-bit console look.
"""
import os
from functools import lru_cache

import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 360, 640
FPS = 30
SCALE = 3

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = ImageFont.truetype(os.path.join(HERE, "assets", "fusion-pixel.ttf"), 12)


def _bayer(n):
    if n == 1:
        return np.zeros((1, 1))
    b = _bayer(n // 2)
    return np.block([[4 * b, 4 * b + 2], [4 * b + 3, 4 * b + 1]])


# The reference look uses soft (non-dithered) light; set False for a strict dithered look.
SMOOTH_LIGHT = True

B8 = (_bayer(8) + 0.5) / 64.0
BAY = np.tile(B8, (128, 128)).astype(np.float32)  # 1024 x 1024 threshold map


def rgb(c):
    return np.array(c[:3], np.uint8)


def new(c=(0, 0, 0), w=W, h=H, alpha=False):
    a = np.zeros((h, w, 4 if alpha else 3), np.uint8)
    if not alpha:
        a[:] = c
    return a


def _col(a, c):
    if a.shape[2] == 4 and len(c) == 3:
        return (c[0], c[1], c[2], 255)
    return c


def _box(a, x, y, w, h):
    hh, ww = a.shape[:2]
    x, y, w, h = int(round(x)), int(round(y)), int(round(w)), int(round(h))
    return max(0, x), max(0, y), min(ww, x + w), min(hh, y + h)


# ---------------------------------------------------------------- primitives
def rect(a, x, y, w, h, c, alpha=None):
    x0, y0, x1, y1 = _box(a, x, y, w, h)
    if x1 <= x0 or y1 <= y0:
        return
    if alpha is None:
        a[y0:y1, x0:x1] = _col(a, c)
    else:
        m = BAY[y0:y1, x0:x1] < alpha
        a[y0:y1, x0:x1][m] = _col(a, c)


def pset(a, x, y, c):
    x, y = int(round(x)), int(round(y))
    if 0 <= x < a.shape[1] and 0 <= y < a.shape[0]:
        a[y, x] = _col(a, c)


def hline(a, x0, x1, y, c):
    rect(a, min(x0, x1), y, abs(x1 - x0) + 1, 1, c)


def vline(a, x, y0, y1, c):
    rect(a, x, min(y0, y1), 1, abs(y1 - y0) + 1, c)


def line(a, x0, y0, x1, y1, c, dash=0):
    x0, y0, x1, y1 = int(round(x0)), int(round(y0)), int(round(x1)), int(round(y1))
    dx, dy = abs(x1 - x0), -abs(y1 - y0)
    sx, sy = (1 if x0 < x1 else -1), (1 if y0 < y1 else -1)
    err = dx + dy
    i = 0
    while True:
        if not dash or (i // dash) % 2 == 0:
            pset(a, x0, y0, c)
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x0 += sx
        if e2 <= dx:
            err += dx
            y0 += sy
        i += 1


@lru_cache(maxsize=64)
def _disc(r):
    k = int(np.ceil(r))
    yy, xx = np.mgrid[-k:k + 1, -k:k + 1]
    return (xx * xx + yy * yy) <= r * r + 0.3


def disc(a, cx, cy, r, c):
    m = _disc(float(r))
    k = (m.shape[0] - 1) // 2
    cx, cy = int(round(cx)), int(round(cy))
    x0, y0, x1, y1 = _box(a, cx - k, cy - k, 2 * k + 1, 2 * k + 1)
    if x1 <= x0 or y1 <= y0:
        return
    mm = m[y0 - (cy - k):y1 - (cy - k), x0 - (cx - k):x1 - (cx - k)]
    a[y0:y1, x0:x1][mm] = _col(a, c)


def thick(a, x0, y0, x1, y1, r, c):
    """A rounded thick segment (used for limbs, ropes, bars)."""
    n = int(max(abs(x1 - x0), abs(y1 - y0)) * 1.5) + 1
    for i in range(n + 1):
        t = i / n
        disc(a, x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, r, c)


def mask_poly(pts, w=W, h=H):
    im = Image.new("1", (w, h), 0)
    ImageDraw.Draw(im).polygon([(float(x), float(y)) for x, y in pts], fill=1)
    return np.array(im, bool)


def mask_ellipse(cx, cy, rx, ry, w=W, h=H):
    yy, xx = np.ogrid[:h, :w]
    return ((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2 <= 1.0


def mask_rrect(x, y, w, h, r, W_=W, H_=H):
    im = Image.new("1", (W_, H_), 0)
    ImageDraw.Draw(im).rounded_rectangle([x, y, x + w - 1, y + h - 1], radius=r, fill=1)
    return np.array(im, bool)


def paint(a, m, c, alpha=None):
    if alpha is None:
        a[m] = _col(a, c)
    else:
        hh, ww = a.shape[:2]
        a[m & (BAY[:hh, :ww] < alpha)] = _col(a, c)


def border(m):
    """Outer edge pixels of a mask."""
    p = np.pad(m, 1)
    er = p[1:-1, 1:-1] & p[:-2, 1:-1] & p[2:, 1:-1] & p[1:-1, :-2] & p[1:-1, 2:]
    return m & ~er


def dilate(m, n=1, diag=True):
    for _ in range(n):
        p = np.pad(m, 1)
        d = p[1:-1, 1:-1] | p[:-2, 1:-1] | p[2:, 1:-1] | p[1:-1, :-2] | p[1:-1, 2:]
        if diag:
            d |= p[:-2, :-2] | p[:-2, 2:] | p[2:, :-2] | p[2:, 2:]
        m = d
    return m


def shift(m, dx, dy):
    out = np.zeros_like(m)
    hh, ww = m.shape[:2]
    xs0, xs1 = max(0, -dx), min(ww, ww - dx)
    ys0, ys1 = max(0, -dy), min(hh, hh - dy)
    out[ys0 + dy:ys1 + dy, xs0 + dx:xs1 + dx] = m[ys0:ys1, xs0:xs1]
    return out


# ------------------------------------------------------------- gradients/light
def vgrad(a, x, y, w, h, stops, m=None):
    x0, y0, x1, y1 = _box(a, x, y, w, h)
    if x1 <= x0 or y1 <= y0:
        return
    n = len(stops)
    st = np.array([s[:3] for s in stops], np.uint8)
    pos = (np.arange(y0, y1) - y) / max(1, h - 1) * (n - 1)
    idx = np.clip(np.floor(pos).astype(int), 0, n - 2)
    frac = np.clip(pos - idx, 0, 1)
    pick = idx[:, None] + (BAY[y0:y1, x0:x1] < frac[:, None])
    out = st[pick]
    sub = a[y0:y1, x0:x1]
    if m is None:
        sub[..., :3] = out
        if a.shape[2] == 4:
            sub[..., 3] = 255
    else:
        mm = m[y0:y1, x0:x1]
        sub[..., :3][mm] = out[mm]
        if a.shape[2] == 4:
            sub[..., 3][mm] = 255


def light_field(a, f, x0, y0, color, steps=4, mode="add"):
    """Add a (0..1) intensity field `f` placed at (x0,y0), quantised + dithered."""
    hh, ww = f.shape
    X0, Y0, X1, Y1 = _box(a, x0, y0, ww, hh)
    if X1 <= X0 or Y1 <= Y0:
        return
    f = f[Y0 - y0:Y1 - y0, X0 - x0:X1 - x0]
    if SMOOTH_LIGHT or steps <= 0:
        q = np.clip(f, 0, 1)[..., None]
    else:
        q = np.clip(np.floor(f * steps + BAY[Y0:Y1, X0:X1]) / steps, 0, 1)[..., None]
    sub = a[Y0:Y1, X0:X1, :3].astype(np.float32)
    col = np.array(color[:3], np.float32)
    if mode == "add":
        sub += col * q
    elif mode == "mul":  # darken towards color
        sub = sub * (1 - q) + sub * (col / 255.0) * q
    else:
        sub += (col - sub) * q
    a[Y0:Y1, X0:X1, :3] = np.clip(sub, 0, 255).astype(np.uint8)


def glow(a, cx, cy, r, color, strength=1.0, steps=4, power=1.6, mode="add", ry=None):
    ry = ry or r
    x0, y0 = int(cx - r), int(cy - ry)
    yy, xx = np.mgrid[0:int(2 * ry) + 1, 0:int(2 * r) + 1]
    d = np.sqrt(((xx + x0 - cx) / r) ** 2 + ((yy + y0 - cy) / ry) ** 2)
    f = np.clip(1 - d, 0, 1) ** power * strength
    light_field(a, f, x0, y0, color, steps, mode)


def dim(a, alpha, c=(0, 0, 0)):
    hh, ww = a.shape[:2]
    a[BAY[:hh, :ww] < alpha] = c


def shade(a, k):
    """Multiply brightness (used sparingly)."""
    a[:] = np.clip(a.astype(np.float32) * k, 0, 255).astype(np.uint8)


# ------------------------------------------------------------------- sprites
def sprite(rows, cmap):
    h = len(rows)
    w = max(len(r) for r in rows)
    s = np.zeros((h, w, 4), np.uint8)
    for y, r in enumerate(rows):
        for x, ch in enumerate(r):
            if ch in cmap:
                s[y, x, :3] = cmap[ch][:3]
                s[y, x, 3] = 255
    return s


def scale_sprite(s, k):
    return np.repeat(np.repeat(s, k, 0), k, 1)


def outlined(s, c):
    """Pad a sprite by 1px and add a coloured outline around opaque pixels."""
    s = np.pad(s, ((1, 1), (1, 1), (0, 0)))
    al = s[..., 3] > 0
    ring = dilate(al, 1, diag=False) & ~al
    s[ring, :3] = c[:3]
    s[ring, 3] = 255
    return s


def blit(a, s, x, y, flip=False, alpha=None, tint=None):
    if flip:
        s = s[:, ::-1]
    hh, ww = s.shape[:2]
    x, y = int(round(x)), int(round(y))
    X0, Y0, X1, Y1 = _box(a, x, y, ww, hh)
    if X1 <= X0 or Y1 <= Y0:
        return
    ss = s[Y0 - y:Y1 - y, X0 - x:X1 - x]
    m = ss[..., 3] > 0
    if alpha is not None:
        m &= BAY[Y0:Y1, X0:X1] < alpha
    src = ss[..., :3]
    if tint is not None:
        src = np.empty_like(src)
        src[:] = tint
    if a.shape[2] == 4:
        a[Y0:Y1, X0:X1, :3][m] = src[m]
        a[Y0:Y1, X0:X1, 3][m] = 255
    else:
        a[Y0:Y1, X0:X1][m] = src[m]


# ---------------------------------------------------------------------- text
def _parse(s):
    segs, buf, hl = [], "", 0
    for ch in s:
        if ch in "{[":
            segs.append((buf, hl))
            buf, hl = "", (2 if ch == "{" else 3)
        elif ch in "}]":
            segs.append((buf, hl))
            buf, hl = "", 0
        else:
            buf += ch
    segs.append((buf, hl))
    return [(t, (h or 1)) for t, h in segs if t]


def plain(s):
    return "".join(t for t, _ in _parse(s))


@lru_cache(maxsize=8192)
def text_mask(s, k=None):
    """Index mask (0 bg, 1 normal, 2 '{hl}', 3 '[hl2]') of the first k chars."""
    segs = _parse(s)
    full_w = sum(int(FONT.getlength(t)) for t, _ in segs)
    img = Image.new("L", (full_w + 4, 16), 0)
    d = ImageDraw.Draw(img)
    d.fontmode = "1"
    x, left = 2, (10 ** 9 if k is None else k)
    for t, h in segs:
        shown = t[:max(0, left)]
        left -= len(t)
        if shown:
            d.text((x, 1), shown, font=FONT, fill=h)
        x += int(FONT.getlength(t))
    return np.array(img)


def text_width(s, scale=1):
    return (text_mask(s).shape[1]) * scale


def text(a, s, x, y, color=(255, 255, 255), scale=1, hl=(255, 214, 90), hl2=(255, 120, 170),
         outline=None, shadow=None, align="left", k=None, alpha=None, sh_off=1):
    m = text_mask(s, k)
    full_w = text_width(s)
    if align == "center":
        x = x - full_w * scale / 2
    elif align == "right":
        x = x - full_w * scale
    layers = []
    fg = m > 0
    if shadow is not None:
        layers.append((shift(dilate(fg) if outline is not None else fg, sh_off, sh_off), shadow))
    if outline is not None:
        layers.append((dilate(fg), outline))
    for idx, c in ((1, color), (2, hl), (3, hl2)):
        layers.append((m == idx, c))
    x, y = int(round(x)), int(round(y))
    for mk, c in layers:
        if not mk.any():
            continue
        if scale > 1:
            mk = np.repeat(np.repeat(mk, scale, 0), scale, 1)
        hh, ww = mk.shape
        X0, Y0, X1, Y1 = _box(a, x, y, ww, hh)
        if X1 <= X0 or Y1 <= Y0:
            continue
        sub = mk[Y0 - y:Y1 - y, X0 - x:X1 - x]
        if alpha is not None:
            sub = sub & (BAY[Y0:Y1, X0:X1] < alpha)
        a[Y0:Y1, X0:X1][sub] = _col(a, c)


# ---------------------------------------------------------------- transitions
def dissolve(a, b, p):
    """Bayer dissolve from a to b (p 0..1)."""
    m = BAY[:H, :W] < p
    out = a.copy()
    out[m] = b[m]
    return out


def zoom(a, cx, cy, f, tx=W / 2, ty=H / 2):
    ys = np.clip((cy + (np.arange(H) - ty) / f).astype(int), 0, H - 1)
    xs = np.clip((cx + (np.arange(W) - tx) / f).astype(int), 0, W - 1)
    return a[ys][:, xs]


def pixelate(a, n):
    if n <= 1:
        return a
    small = a[::n, ::n]
    return np.repeat(np.repeat(small, n, 0), n, 1)[:H, :W]


def glitch(a, amount, seed):
    rng = np.random.default_rng(seed)
    out = a.copy()
    for _ in range(int(3 + amount * 10)):
        y0 = rng.integers(0, H - 4)
        h = int(rng.integers(2, 8 + amount * 30))
        dx = int(rng.integers(-1, 2) * rng.integers(2, 4 + amount * 30))
        out[y0:y0 + h] = np.roll(out[y0:y0 + h], dx, axis=1)
    k = int(1 + amount * 4)
    out[..., 0] = np.roll(out[..., 0], k, axis=1)
    out[..., 2] = np.roll(out[..., 2], -k, axis=1)
    return out


def crt_off(a, p):
    """Old-TV switch off: squash to a line, then to a dot."""
    out = np.zeros_like(a)
    if p >= 1:
        return out
    if p < 0.6:
        sy = max(1.0 / H, 1 - p / 0.6)
        sx = 1.0
    else:
        sy = 1.0 / H * 2
        sx = max(0.01, 1 - (p - 0.6) / 0.4)
    h = max(1, int(H * sy))
    w = max(1, int(W * sx))
    ys = (np.arange(h) / h * H).astype(int)
    xs = (np.arange(w) / w * W).astype(int)
    src = a[ys][:, xs]
    if p >= 0.45:
        src = np.clip(src.astype(np.int16) + int((p - 0.45) * 600), 0, 255).astype(np.uint8)
    y0, x0 = (H - h) // 2, (W - w) // 2
    out[y0:y0 + h, x0:x0 + w] = src
    return out


# -------------------------------------------------------------------- noise
def value_noise(h, w, scale, seed, octaves=1):
    rng = np.random.default_rng(seed)
    total = np.zeros((h, w))
    amp, s, norm = 1.0, scale, 0.0
    for _ in range(octaves):
        gh, gw = int(h / s) + 3, int(w / s) + 3
        g = rng.random((gh, gw))
        ys, xs = np.arange(h) / s, np.arange(w) / s
        y0, x0 = ys.astype(int), xs.astype(int)
        fy, fx = ys - y0, xs - x0
        fy, fx = fy * fy * (3 - 2 * fy), fx * fx * (3 - 2 * fx)
        a_ = g[y0][:, x0]
        b_ = g[y0][:, x0 + 1]
        c_ = g[y0 + 1][:, x0]
        d_ = g[y0 + 1][:, x0 + 1]
        top = a_ + (b_ - a_) * fx[None, :]
        bot = c_ + (d_ - c_) * fx[None, :]
        total += (top + (bot - top) * fy[:, None]) * amp
        norm += amp
        amp *= 0.5
        s /= 2
    return total / norm


# ------------------------------------------------------------------- easing
def clamp01(x):
    return max(0.0, min(1.0, x))


def smooth(x):
    x = clamp01(x)
    return x * x * (3 - 2 * x)


def lerp(a, b, t):
    return a + (b - a) * t


def lerpc(c1, c2, t):
    return tuple(int(round(lerp(x, y, t))) for x, y in zip(c1, c2))


def back_out(x, s=1.7):
    x = clamp01(x) - 1
    return x * x * ((s + 1) * x + s) + 1


def scale2x(s):
    """AdvMAME2x / Scale2x: doubles a sprite while keeping diagonal edges smooth."""
    p = np.pad(s, ((1, 1), (1, 1), (0, 0)), mode="edge")
    B, D, E, F, Hh = p[:-2, 1:-1], p[1:-1, :-2], p[1:-1, 1:-1], p[1:-1, 2:], p[2:, 1:-1]
    eq = lambda x, y: np.all(x == y, axis=-1)
    c1 = eq(B, D) & ~eq(B, F) & ~eq(D, Hh)
    c2 = eq(B, F) & ~eq(B, D) & ~eq(F, Hh)
    c3 = eq(D, Hh) & ~eq(D, B) & ~eq(Hh, F)
    c4 = eq(Hh, F) & ~eq(D, Hh) & ~eq(B, F)
    e0 = np.where(c1[..., None], D, E)
    e1 = np.where(c2[..., None], F, E)
    e2 = np.where(c3[..., None], D, E)
    e3 = np.where(c4[..., None], F, E)
    h, w = s.shape[:2]
    out = np.zeros((h * 2, w * 2, s.shape[2]), s.dtype)
    out[0::2, 0::2], out[0::2, 1::2], out[1::2, 0::2], out[1::2, 1::2] = e0, e1, e2, e3
    return out
