"""Scene 1 / 7a: the bedroom at 2:47 am (and at dawn)."""
from functools import lru_cache

import numpy as np

from engine import (W, H, new, rect, vgrad, glow, light_field, paint, mask_poly, mask_rrect,
                    mask_ellipse, border, disc, thick, pset, line, hline, vline, blit, sprite,
                    lerpc, BAY, text)
import characters as C

WIN = (112, 120, 136, 148)  # window opening x, y, w, h
DIGITS = {
    "0": ["111", "101", "101", "101", "111"], "1": ["010", "110", "010", "010", "111"],
    "2": ["111", "001", "111", "100", "111"], "3": ["111", "001", "111", "001", "111"],
    "4": ["101", "101", "111", "001", "001"], "5": ["111", "100", "111", "001", "111"],
    "6": ["111", "100", "111", "101", "111"], "7": ["111", "001", "010", "010", "010"],
    "8": ["111", "101", "111", "101", "111"], "9": ["111", "101", "111", "001", "111"],
}


def seg_text(a, s, x, y, c, colon_on=True):
    for ch in s:
        if ch == ":":
            if colon_on:
                pset(a, x, y + 1, c)
                pset(a, x, y + 3, c)
            x += 2
            continue
        for j, row in enumerate(DIGITS[ch]):
            for i, v in enumerate(row):
                if v == "1":
                    pset(a, x + i, y + j, c)
        x += 4


# palettes for night (0) and dawn (1)
PAL = {
    0: dict(sky=[(10, 10, 34), (18, 18, 54), (34, 28, 82), (62, 42, 104), (92, 56, 120)],
            city=(18, 16, 40), city_hi=(30, 26, 60),
            wall=(34, 30, 64), wall2=(30, 26, 58), wall_dk=(22, 20, 44),
            wood=(84, 54, 52), wood_hi=(116, 78, 66), wood_dk=(52, 34, 40),
            floor=(46, 36, 52), floor_hi=(60, 46, 62), floor_dk=(32, 26, 40),
            cur=(98, 36, 70), cur_hi=(128, 52, 88), cur_dk=(64, 22, 50),
            sheet=(112, 114, 170), sheet_dk=(80, 82, 132),
            blanket=(62, 56, 126), blanket_hi=(84, 78, 156), blanket_dk=(42, 36, 92),
            hem=(118, 66, 136), beam=(46, 54, 96)),
    1: dict(sky=[(88, 104, 186), (150, 130, 196), (236, 150, 160), (255, 180, 130), (255, 214, 150)],
            city=(108, 84, 140), city_hi=(132, 104, 160),
            wall=(92, 72, 112), wall2=(84, 66, 104), wall_dk=(64, 50, 88),
            wood=(140, 92, 72), wood_hi=(178, 124, 90), wood_dk=(96, 60, 56),
            floor=(110, 78, 84), floor_hi=(136, 98, 98), floor_dk=(80, 56, 68),
            cur=(176, 72, 96), cur_hi=(214, 104, 120), cur_dk=(128, 46, 76),
            sheet=(222, 210, 226), sheet_dk=(176, 160, 190),
            blanket=(120, 110, 196), blanket_hi=(154, 146, 222), blanket_dk=(86, 76, 156),
            hem=(214, 120, 160), beam=(120, 70, 30)),
}


def blanket_top(x):
    g = lambda c, s: np.exp(-((x - c) / s) ** 2)
    return 404 - (16 * g(165, 34) + 13 * g(215, 30) + 32 * g(272, 21) + 14 * g(318, 18) + 4)


@lru_cache(maxsize=2)
def static(tod):
    p = PAL[tod]
    a = new(p["wall"])
    # wallpaper: soft vertical stripes + darker ceiling
    for x in range(0, W, 14):
        rect(a, x, 0, 6, 470, p["wall2"])
    rect(a, 0, 0, W, 40, p["wall_dk"], alpha=0.55)
    rect(a, 0, 40, W, 40, p["wall_dk"], alpha=0.25)
    # baseboard + floor planks
    rect(a, 0, 462, W, 8, p["wood_dk"])
    hline(a, 0, W, 462, p["wood"])
    vgrad(a, 0, 470, W, 170, [p["floor_hi"], p["floor"], p["floor_dk"], p["floor_dk"]])
    for i, y in enumerate(range(470, 640, 12)):
        hline(a, 0, W, y, p["floor_dk"])
        off = (i * 37) % 60
        for x in range(off, W, 60):
            vline(a, x, y, y + 11, p["floor_dk"])
            pset(a, x + 1, y + 1, p["floor_hi"])

    # rug
    rug = mask_ellipse(232, 566, 104, 30)
    paint(a, rug, (96, 44, 74) if tod == 0 else (178, 92, 120))
    paint(a, rug & ~mask_ellipse(232, 566, 96, 25), (130, 66, 96) if tod == 0 else (214, 132, 150))
    paint(a, mask_ellipse(232, 566, 80, 19) & ~mask_ellipse(232, 566, 76, 17), (150, 96, 70) if tod == 0 else (240, 190, 120))
    paint(a, border(rug), (60, 26, 50) if tod == 0 else (120, 60, 90))
    # slippers
    for sx in (92, 108):
        rect(a, sx, 478, 12, 5, (150, 150, 190) if tod == 0 else (230, 220, 240))
        rect(a, sx, 478, 5, 5, (100, 100, 140) if tod == 0 else (190, 180, 210))
    # energy drink can + crumpled snack bag
    rect(a, 300, 470, 7, 11, (40, 160, 170) if tod == 0 else (70, 200, 200))
    rect(a, 300, 470, 7, 2, (170, 180, 190))
    vline(a, 301, 472, 480, (120, 230, 230))
    rect(a, 312, 476, 12, 6, (190, 70, 60) if tod == 0 else (230, 110, 90))
    pset(a, 315, 476, (255, 210, 90))

    # ---- window
    x, y, w, h = WIN
    vgrad(a, x, y, w, h, p["sky"])
    # city skyline
    rng = np.random.default_rng(3)
    bx = x
    while bx < x + w:
        bw = int(rng.integers(10, 22))
        bh = int(rng.integers(20, 64))
        rect(a, bx, y + h - bh, bw, bh, p["city"])
        vline(a, bx, y + h - bh, y + h, p["city_hi"])
        if rng.random() < 0.3:
            vline(a, bx + bw // 2, y + h - bh - 6, y + h - bh, p["city"])
        bx += bw + int(rng.integers(0, 3))
    if tod == 1:  # sun glow on the horizon
        glow(a, 200, y + h, 70, (255, 160, 80), 0.6, steps=5, ry=40)
    # frame
    fr = p["wood"]
    rect(a, x - 6, y - 6, w + 12, 6, p["wood_hi"])
    rect(a, x - 6, y - 6, 6, h + 12, p["wood_hi"])
    rect(a, x + w, y - 6, 6, h + 12, p["wood_dk"])
    rect(a, x - 6, y + h, w + 12, 6, p["wood_dk"])
    rect(a, x + w // 2 - 2, y, 4, h, fr)
    vline(a, x + w // 2 - 2, y, y + h, p["wood_hi"])
    rect(a, x, y + h // 2 - 2, w, 4, fr)
    hline(a, x, x + w, y + h // 2 - 2, p["wood_hi"])
    # glass reflections
    for ox in (14, 86):
        for k in range(10):
            pset(a, x + ox + k, y + 30 - k, (255, 255, 255)) if (k % 3 == 0) else None
    # sill
    rect(a, x - 12, y + h + 6, w + 24, 6, p["wood_hi"])
    rect(a, x - 12, y + h + 11, w + 24, 2, p["wood_dk"])

    # ---- curtains + rod
    for cx0, flip in ((92, False), (236, True)):
        cw = 32
        for i in range(cw):
            col = [p["cur_hi"], p["cur"], p["cur"], p["cur_dk"]][((i + (2 if flip else 0)) // 2) % 4]
            bottom = 304 + int(3 * np.sin(i * 0.7))
            # tie-back pinch
            vline(a, cx0 + i, 108, bottom, col)
        rect(a, cx0 + 4, 230, cw - 8, 4, (200, 160, 80))
    rect(a, 84, 103, 192, 4, p["wood_dk"])
    hline(a, 84, 275, 103, p["wood_hi"])
    disc(a, 84, 105, 3, p["wood_hi"])
    disc(a, 276, 105, 3, p["wood_hi"])

    # ---- poster (mountain dream)
    px, py, pw, ph = 288, 132, 50, 72
    rect(a, px - 2, py - 2, pw + 4, ph + 4, (220, 214, 228) if tod else (128, 124, 150))
    vgrad(a, px, py, pw, ph, [(80, 120, 190), (140, 170, 210), (200, 210, 230)] if tod else
          [(34, 44, 88), (56, 66, 110), (82, 90, 130)])
    mtn = mask_poly([(px, py + 56), (px + 18, py + 24), (px + 28, py + 36), (px + 36, py + 28), (px + pw, py + 50),
                     (px + pw, py + ph), (px, py + ph)])
    paint(a, mtn, (70, 90, 120) if tod else (30, 36, 64))
    snow = mask_poly([(px + 13, py + 32), (px + 18, py + 24), (px + 23, py + 31), (px + 19, py + 29)])
    paint(a, snow, (240, 240, 250) if tod else (150, 150, 180))
    text(a, "GO!", px + pw // 2, py + 4, (255, 230, 120) if tod else (150, 130, 90), align="center")
    pset(a, px + pw // 2, py - 4, (180, 180, 190))  # pin

    # ---- shelf + stuff
    rect(a, 14, 258, 72, 4, p["wood_hi"])
    rect(a, 14, 262, 72, 1, p["wood_dk"])
    for bx_ in (20, 74):
        rect(a, bx_, 263, 3, 6, p["wood_dk"])
    bc = [(150, 60, 70), (60, 110, 150), (200, 160, 70), (90, 140, 90)]
    for i, (bw, bh) in enumerate([(5, 20), (6, 17), (5, 22), (4, 15)]):
        bx_ = 18 + i * 7
        c = bc[i] if tod else tuple(v // 2 for v in bc[i])
        rect(a, bx_, 258 - bh, bw, bh, c)
        hline(a, bx_, bx_ + bw - 1, 258 - bh + 3, tuple(min(255, v + 40) for v in c))
    # wilted plant
    rect(a, 54, 248, 12, 10, (150, 84, 60) if tod else (88, 52, 46))
    rect(a, 53, 247, 14, 2, (176, 104, 72) if tod else (104, 62, 52))
    leaf = (110, 150, 80) if tod else (54, 76, 50)
    for (x0, y0, x1, y1) in [(60, 247, 56, 236), (60, 247, 66, 238), (60, 247, 71, 248), (60, 247, 52, 244)]:
        line(a, x0, y0, x1, y1, leaf)
    # trophy (dusty)
    rect(a, 76, 248, 6, 2, (160, 130, 60) if tod else (96, 80, 46))
    rect(a, 77, 240, 4, 8, (200, 170, 70) if tod else (120, 100, 52))

    # ---- nightstand
    rect(a, 10, 404, 54, 6, p["wood_hi"])
    rect(a, 14, 410, 46, 50, p["wood"])
    rect(a, 14, 410, 46, 2, p["wood_dk"])
    rect(a, 18, 418, 38, 16, p["wood_dk"])
    rect(a, 19, 419, 36, 14, p["wood"])
    rect(a, 34, 424, 6, 2, p["wood_hi"])
    rect(a, 16, 460, 4, 10, p["wood_dk"])
    rect(a, 54, 460, 4, 10, p["wood_dk"])
    # clock body
    rect(a, 19, 390, 28, 14, (20, 18, 26))
    rect(a, 19, 390, 28, 1, (60, 56, 70))
    rect(a, 21, 392, 24, 10, (36, 10, 20))
    # glass of water
    rect(a, 51, 394, 7, 10, (120, 150, 190))
    rect(a, 52, 398, 5, 5, (70, 110, 170))
    vline(a, 51, 394, 403, (200, 220, 240))

    # ---- bed
    rect(a, 64, 334, 12, 136, p["wood"])
    rect(a, 64, 334, 12, 3, p["wood_hi"])
    rect(a, 66, 342, 8, 70, p["wood_dk"])
    rect(a, 74, 334, 2, 136, p["wood_dk"])
    rect(a, 76, 404, 268, 22, p["sheet"])
    rect(a, 76, 422, 268, 4, p["sheet_dk"])
    rect(a, 64, 426, 288, 14, p["wood"])
    hline(a, 64, 351, 426, p["wood_hi"])
    hline(a, 64, 351, 439, p["wood_dk"])
    for lx in (70, 336):
        rect(a, lx, 440, 7, 30, p["wood_dk"])
    rect(a, 342, 380, 10, 90, p["wood"])
    rect(a, 342, 380, 10, 3, p["wood_hi"])
    rect(a, 350, 380, 2, 90, p["wood_dk"])
    # pillow
    pm = mask_rrect(80, 390, 50, 18, 7)
    paint(a, pm, p["sheet"])
    paint(a, pm & ~np.roll(pm, -3, axis=0), p["sheet_dk"])
    paint(a, border(pm), p["sheet_dk"])
    # blanket
    xs = np.arange(122, 346)
    tops = blanket_top(xs.astype(float)).astype(int)
    pts = [(122, 432)] + [(int(xx), int(tt)) for xx, tt in zip(xs, tops)] + [(345, 434)]
    for xx in range(345, 121, -6):
        pts.append((xx, 432 + int(2 * np.sin(xx * 0.4))))
    bm = mask_poly(pts)
    paint(a, bm, p["blanket"])
    yy = np.arange(H)[:, None]
    topmap = np.full(W, 999)
    topmap[122:346] = tops
    hi = bm & (yy < topmap[None, :] + 4)
    paint(a, hi, p["blanket_hi"], alpha=0.65)
    lo = bm & (yy > 418)
    paint(a, lo, p["blanket_dk"], alpha=0.75)
    paint(a, bm & (yy >= 420) & (yy < 424), p["hem"])
    # folds
    for fx in (196, 300):
        top0 = int(blanket_top(np.array([float(fx)]))[0])
        for k in range(10):
            pset(a, fx + k // 3, top0 + 8 + k, p["blanket_dk"])
    paint(a, border(bm), p["blanket_dk"])
    # folded sheet edge at the chest
    rect(a, 120, 384, 7, 44, p["sheet"])
    vline(a, 126, 384, 427, p["sheet_dk"])
    return a


def stars(a, t, tod):
    if tod >= 1:
        return
    x, y, w, h = WIN
    rng = np.random.default_rng(5)
    for i in range(34):
        sx, sy = x + rng.integers(2, w - 2), y + rng.integers(2, h - 60)
        ph = rng.random() * 6.28
        sp = 1 + rng.random() * 3
        b = 0.5 + 0.5 * np.sin(t * sp + ph)
        if abs(sx - (x + w // 2)) < 3 or abs(sy - (y + h // 2)) < 3:
            continue
        c = (255, 255, 230) if b > 0.7 else (150, 150, 200)
        if b > 0.2:
            pset(a, sx, sy, c)
        if i % 9 == 0 and b > 0.85:
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                pset(a, sx + dx, sy + dy, (180, 180, 230))
    # moon
    mx, my = 150, 150
    disc(a, mx, my, 9, (246, 238, 196))
    disc(a, mx + 4, my - 3, 8, (16, 16, 48))
    glow(a, mx, my, 26, (60, 60, 90), 0.5, steps=3)


def city_lights(a, t, tod):
    x, y, w, h = WIN
    rng = np.random.default_rng(9)
    for i in range(46):
        wx = x + 2 + rng.integers(0, w - 4)
        wy = y + h - 4 - rng.integers(0, 44)
        on = rng.random() < (0.55 if tod == 0 else 0.12)
        flick = ((int(t * 0.7 + rng.random() * 10)) % 7) != 0
        if abs(wx - (x + w // 2)) < 3:
            continue
        if on and flick:
            c = (255, 214, 120) if rng.random() < 0.7 else (140, 220, 255)
            pset(a, wx, wy, c)
            pset(a, wx + 1, wy, c)
    # antenna beacon
    if tod == 0 and int(t * 1.5) % 2 == 0:
        pset(a, x + 30, y + h - 66, (255, 60, 60))


FEED_COLS = [(110, 200, 255), (255, 120, 190), (255, 214, 110), (150, 255, 190), (190, 150, 255)]


def phone_color(t, switches):
    k = sum(1 for s in switches if s <= t)
    c = FEED_COLS[k % len(FEED_COLS)]
    last = max([s for s in switches if s <= t], default=-9)
    flash = max(0.0, 1 - (t - last) / 0.18)
    return c, k, flash


HEART = sprite([".r.r.", "rrrrr", "rrrrr", ".rrr.", "..r.."], {"r": (255, 90, 130)})


def draw(a, t, tod=0, phone="hand", eyes="open", clock="02:47", switches=(), sky_mix=None):
    """Draw the bedroom. `sky_mix` (0..1) dissolves night -> dawn."""
    if sky_mix is None:
        a[:] = static(tod)
        stars(a, t, tod)
        city_lights(a, t, tod)
    else:
        a0 = static(0).copy()
        stars(a0, t, 0)
        city_lights(a0, t, 0)
        a1 = static(1).copy()
        city_lights(a1, t, 1)
        m = BAY[:H, :W] < sky_mix
        a[:] = np.where(m[..., None], a1, a0)
        tod = 1 if sky_mix > 0.5 else 0
    p = PAL[tod]
    x, y, w, h = WIN
    # light beam from the window
    beam = mask_poly([(x, y + h), (x + w, y + h), (x + w + 96, 470), (x + 70, 470)])
    f = np.zeros((H, W), np.float32)
    f[beam] = 0.16 if tod == 0 else 0.26
    light_field(a, f, 0, 0, (90, 110, 180) if tod == 0 else (255, 170, 90), steps=3)
    # dust motes in the beam
    rng = np.random.default_rng(21)
    for i in range(18):
        dx = (rng.random() * 120 + t * (2 + rng.random() * 3)) % 150
        dy = (rng.random() * 160 + np.sin(t * 0.8 + i) * 6)
        px_, py_ = x + 20 + dx + dy * 0.45, y + h + 10 + dy
        if beam[int(min(H - 1, py_)), int(min(W - 1, px_))]:
            pset(a, px_, py_, (190, 200, 240) if tod == 0 else (255, 230, 180))

    # clock
    glow(a, 33, 397, 22, (120, 20, 30), 0.6, steps=3)
    seg_text(a, clock, 23, 395, (255, 64, 74), colon_on=(int(t * 2) % 2 == 0))

    # character head on the pillow (face up)
    hd = np.rot90(C.head_profile_big(eyes)).copy()
    if tod == 0:  # moonlit: darker, bluer, so the phone light can model the face
        hd[..., :3] = (hd[..., :3] * np.array([0.42, 0.45, 0.62])).astype(np.uint8) + np.array([8, 8, 22], np.uint8)
    blit(a, hd, 84, 364)

    if phone == "hand":
        col, k, flash = phone_color(t, switches)
        # arm + hands
        thick(a, 128, 396, 138, 370, 2.3, C.HOOD_SH)
        thick(a, 138, 370, 117, 344, 2.1, C.HOOD_SH)
        thick(a, 137, 372, 119, 348, 0.8, (22, 70, 90))
        disc(a, 114, 342, 2.6, C.SKIN_DK)
        disc(a, 90, 342, 2.4, C.SKIN_DK)
        # light cone from the phone down onto the face
        cone = mask_poly([(88, 343), (114, 343), (130, 388), (70, 388)])
        yy = np.arange(H, dtype=np.float32)[:, None]
        f = np.where(cone, np.clip(1 - (yy - 343) / 52.0, 0, 1) * (0.95 + 0.45 * flash), 0).astype(np.float32)
        light_field(a, f, 0, 0, tuple(int(c * 0.5) for c in col), steps=4)
        glow(a, 101, 350, 72, tuple(int(c * 0.28) for c in col), 0.8 + 0.3 * flash, steps=4, power=1.8)
        # the phone itself (seen edge-on, screen facing down)
        rect(a, 87, 338, 28, 4, (26, 26, 38))
        hline(a, 87, 114, 338, (78, 78, 98))
        hline(a, 88, 113, 341, col)
        disc(a, 114, 340, 2.2, C.SKIN)
        # floating hearts
        for i, s_ in enumerate(switches):
            if i % 2 == 0 and 0 <= t - s_ < 1.4:
                u = (t - s_) / 1.4
                blit(a, HEART, 98 + 12 * np.sin(u * 5 + i), 330 - u * 70, alpha=1 - u * 0.9)
    elif phone == "stand":
        rect(a, 226, 271, 16, 3, (28, 28, 40))  # face-down on the windowsill, out of reach
        hline(a, 226, 241, 271, (70, 70, 90))
    # blanket covers the arm when not holding the phone
    return a


def zzz(a, t):
    for i in range(3):
        u = ((t * 0.6 + i / 3.0) % 1.0)
        x = 112 + u * 40 + 4 * np.sin(u * 8 + i)
        y = 360 - u * 70
        sc = 1 if u < 0.5 else 2
        text(a, "Z", x, y, (220, 220, 255), scale=sc, alpha=1 - u, outline=(60, 50, 110))
