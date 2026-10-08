"""Reference-style building blocks: spotlights, sunbursts, gold panels, odometers."""
from functools import lru_cache

import numpy as np

from engine import W, H, rect, hline, vline, pset, text, light_field, glow, mask_poly, blit, scale_sprite

BG = (14, 13, 20)
GOLD, GOLD_HI, GOLD_DK = (214, 158, 62), (252, 212, 120), (130, 88, 36)
CREAM = (246, 238, 220)
RED, RED_DK = (214, 64, 52), (120, 30, 30)

_YY, _XX = np.mgrid[0:H, 0:W].astype(np.float32)


def blend(a, f, color):
    """Alpha-blend a solid colour with a float field f (0..1) over the whole frame."""
    k = np.clip(f, 0, 1)[..., None]
    a[:] = (a * (1 - k) + np.array(color, np.float32) * k).astype(np.uint8)


def add(a, f, color):
    k = np.clip(f, 0, 1)[..., None]
    a[:] = np.clip(a + np.array(color, np.float32) * k, 0, 255).astype(np.uint8)


@lru_cache(maxsize=8)
def _vig(k):
    cx, cy = W / 2, H * 0.42
    d = np.sqrt(((_XX - cx) / (W * 0.62)) ** 2 + ((_YY - cy) / (H * 0.6)) ** 2)
    return (1 - np.clip(d - 0.35, 0, 1) * k).astype(np.float32)[..., None]


def vignette(a, k=0.8):
    a[:] = (a * _vig(k)).astype(np.uint8)


def spotlight(a, cx, top_y, bot_y, top_w, bot_w, color=(150, 160, 200), strength=0.35, floor=True):
    """Soft cone of light from above, plus a pool on the floor."""
    y0, y1 = int(top_y), int(bot_y)
    yy = _YY[y0:y1]
    xx = _XX[y0:y1]
    u = (yy - top_y) / max(1, bot_y - top_y)
    half = (top_w + (bot_w - top_w) * u) / 2
    edge = np.clip(1 - np.abs(xx - cx) / half, 0, 1)
    f = np.clip(edge * 1.6, 0, 1) ** 1.2 * (0.55 + 0.45 * (1 - u)) * strength
    light_field(a, f.astype(np.float32), 0, y0, color)
    if floor:
        glow(a, cx, bot_y, bot_w * 0.6, color, strength * 0.9, power=1.4, ry=bot_w * 0.12)


def sunburst(a, cx, cy, rot, c1, c2, n=14, fade=1.0, radius=420):
    ang = np.arctan2(_YY - cy, _XX - cx) + rot
    rays = ((ang / (2 * np.pi) * n) % 1.0) < 0.5
    out = np.where(rays[..., None], np.array(c1, np.float32), np.array(c2, np.float32))
    d = np.sqrt((_XX - cx) ** 2 + (_YY - cy) ** 2) / radius
    k = np.clip(1 - d, 0, 1) ** 1.2 * fade
    base = np.array(BG, np.float32)
    a[:] = (base * (1 - k[..., None]) + out * k[..., None]).astype(np.uint8)


def panel(a, x, y, w, h, kind="gold", fill=(26, 22, 22)):
    x, y, w, h = int(x), int(y), int(w), int(h)
    rect(a, x, y, w, h, fill)
    if kind == "gold":
        c, hi, dk = GOLD, GOLD_HI, GOLD_DK
        rect(a, x, y, w, 2, c)
        rect(a, x, y + h - 2, w, 2, dk)
        rect(a, x, y, 2, h, c)
        rect(a, x + w - 2, y, 2, h, dk)
        hline(a, x + 1, x + w - 2, y, hi)
        vline(a, x, y + 1, y + h - 2, hi)
        rect(a, x + 4, y + 4, w - 8, 1, (60, 46, 30))
        for cx_, cy_ in ((x + 1, y + 1), (x + w - 4, y + 1), (x + 1, y + h - 4), (x + w - 4, y + h - 4)):
            rect(a, cx_, cy_, 3, 3, hi)
    elif kind == "red":
        rect(a, x, y, w, 1, (110, 86, 64))
        rect(a, x, y + h - 1, w, 1, (110, 86, 64))
        vline(a, x + w - 1, y, y + h - 1, (110, 86, 64))
        rect(a, x, y, 3, h, RED)
    elif kind == "goldtag":
        rect(a, x, y, w, 1, GOLD)
        rect(a, x, y + h - 1, w, 1, GOLD_DK)
        vline(a, x + w - 1, y, y + h - 1, GOLD_DK)
        rect(a, x, y, 3, h, GOLD_HI)
    elif kind == "blue":
        rect(a, x, y, w, 2, (70, 120, 200))
        rect(a, x, y + h - 2, w, 2, (40, 70, 130))
        rect(a, x, y, 2, h, (70, 120, 200))
        rect(a, x + w - 2, y, 2, h, (40, 70, 130))
        hline(a, x + 1, x + w - 2, y, (140, 190, 250))
    elif kind == "boss":
        rect(a, x, y, w, 1, (150, 50, 44))
        rect(a, x, y + h - 1, w, 1, (90, 30, 30))
        vline(a, x, y, y + h - 1, (150, 50, 44))
        vline(a, x + w - 1, y, y + h - 1, (90, 30, 30))


def label(a, s, cx, y, kind="gold", scale=1, color=CREAM, pad=6, hl=(252, 200, 90)):
    from engine import text_width
    tw = text_width(s) * scale
    h = 14 * scale + pad
    x = int(cx - tw / 2 - pad)
    panel(a, x, y, tw + pad * 2, h, kind)
    text(a, s, cx, y + pad // 2 + (1 if scale == 1 else 0), color, scale=scale, align="center", hl=hl)
    return x, tw + pad * 2, h


def odometer(a, x, y, value, ndig=4, roll=0.0, cell=(12, 18)):
    """White digit cells with dark digits (scale 1 font), optional roll of the last digit."""
    cw, ch = cell
    s = str(int(value)).zfill(ndig)[-ndig:]
    rect(a, x - 3, y - 3, ndig * (cw + 2) + 4, ch + 6, (46, 36, 26))
    hline(a, x - 3, x + ndig * (cw + 2), y - 3, GOLD)
    for i, d in enumerate(s):
        cx = x + i * (cw + 2)
        rect(a, cx, y, cw, ch, (236, 230, 216))
        rect(a, cx, y + ch - 3, cw, 3, (196, 188, 172))
        dy = 0
        if i == ndig - 1 and roll:
            dy = int(-roll * ch)
        text(a, d, cx + cw / 2, y + 2 + dy, (30, 24, 28), align="center")
        if i == ndig - 1 and roll:
            text(a, str((int(d) + 1) % 10), cx + cw / 2, y + 2 + dy + ch, (30, 24, 28), align="center")
            rect(a, cx, y - 6, cw, 6, (46, 36, 26))
            rect(a, cx, y + ch, cw, 6, (46, 36, 26))


def stage(a, floor_y=430, color=(20, 18, 28), floor=(26, 22, 32)):
    """Dark theatre backdrop with a subtle floor line."""
    a[:] = color
    rect(a, 0, floor_y, W, H - floor_y, floor)
    hline(a, 0, W - 1, floor_y, (44, 38, 52))


def brick_wall(a, y0, y1, c=(44, 26, 30), mortar=(30, 18, 22), hi=(58, 34, 38)):
    rect(a, 0, y0, W, y1 - y0, c)
    for r, y in enumerate(range(y0, y1, 12)):
        hline(a, 0, W - 1, y, mortar)
        hline(a, 0, W - 1, y + 1, hi)
        off = 0 if r % 2 == 0 else 14
        for x in range(off, W, 28):
            vline(a, x, y, y + 11, mortar)


def put(a, spr, x, y, k=2, flip=False, alpha=None):
    """Blit a chunky sprite scaled by k with its bottom-centre at (x, y)."""
    s = scale_sprite(spr, k)
    blit(a, s, x - s.shape[1] // 2, y - s.shape[0], flip=flip, alpha=alpha)
    return s.shape[1], s.shape[0]


def shadow(a, cx, cy, rx, ry=None, k=0.5):
    ry = ry or max(2, rx // 4)
    f = np.clip(1 - ((_XX - cx) / rx) ** 2 - ((_YY - cy) / ry) ** 2, 0, 1) * k
    a[:] = (a * (1 - f[..., None])).astype(np.uint8)


def sparkle(a, x, y, r, c=(255, 240, 180)):
    r = int(r)
    hline(a, x - r, x + r, y, c)
    vline(a, x, y - r, y + r, c)
    if r > 2:
        pset(a, x - 1, y - 1, c); pset(a, x + 1, y - 1, c)
        pset(a, x - 1, y + 1, c); pset(a, x + 1, y + 1, c)


def check(a, x, y, s=1, c=(120, 230, 140)):
    """Pixel check mark, top-left at (x, y), roughly 9s x 7s."""
    from engine import thick as _thick
    _thick(a, x, y + 3 * s, x + 3 * s, y + 6 * s, 0.6 * s + 0.4, c)
    _thick(a, x + 3 * s, y + 6 * s, x + 9 * s, y, 0.6 * s + 0.4, c)
