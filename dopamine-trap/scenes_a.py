"""Chapters 1-2: intro card, bedroom, brain, molecule, want/like panel, carrot."""
from functools import lru_cache

import numpy as np

from engine import (W, H, new, rect, hline, vline, pset, line, thick, disc, text, glow, blit, sprite,
                    scale_sprite, mask_poly, mask_ellipse, border, paint, value_noise, smooth, lerp,
                    clamp01, back_out, zoom, dilate, text_width)
import style as S
import chibi as C
import events as E
from timeline import L, SCENE_T, word_t

CREAM = S.CREAM


def pop(t, t0, d=0.25):
    return 0.0 if t < t0 else min(1.0, back_out((t - t0) / d))


def xfade(a, b, k):
    k = clamp01(k)
    return (a * (1 - k) + b * k).astype(np.uint8)


# ------------------------------------------------------------------ intro
def intro(t):
    a = new(S.BG)
    S.sunburst(a, 180, 176, t * 0.12, (112, 28, 26), (54, 14, 16), n=16, radius=440)
    S.vignette(a, 0.9)
    S.label(a, "多巴胺的陷阱", 180, 92, "gold", scale=2, color=(252, 214, 120))
    rect(a, 118, 132, 124, 110, (30, 12, 16))
    glow(a, 180, 228, 80, (40, 110, 150), 0.45, ry=44)
    S.put(a, C.portrait("tired"), 180, 240, k=4)
    glow(a, 180, 244, 54, (60, 150, 200), 0.3, ry=12)
    band = mask_poly([(0, 252), (W, 230), (W, 234), (0, 256)])
    paint(a, band, (230, 64, 44))
    if t >= E.INTRO_POP[1]:
        q = pop(t, E.INTRO_POP[1])
        text(a, "你", 180, 250 - int((1 - q) * 20), CREAM, scale=3, align="center",
             outline=(36, 10, 12), shadow=(170, 34, 30), sh_off=1)
    tags = [("凌晨 2:47 · 仍在线", "red"), ("今日屏幕时间 6h12m", "red"), ("多巴胺 · 重度玩家", "goldtag")]
    for i, (s, kind) in enumerate(tags):
        t0 = E.INTRO_POP[2 + i]
        if t >= t0:
            dx = int((1 - smooth((t - t0) / 0.2)) * 120)
            S.label(a, s, 180 + dx, 300 + i * 27, kind=kind,
                    color=(252, 210, 110) if kind == "goldtag" else CREAM)
    if t >= E.COUNT[0]:
        n = int(287 * smooth((t - E.COUNT[0]) / (E.COUNT[1] - E.COUNT[0])))
        s = "%d+" % n
        w1, wn, w2 = text_width("今晚已刷"), text_width("888+") * 3, text_width("条")
        x = 180 - (w1 + wn + w2 + 16) / 2
        text(a, "今晚已刷", x, 398, (230, 200, 160))
        text(a, s, x + w1 + 8 + wn / 2, 384, (252, 196, 80), scale=3, align="center", outline=(40, 18, 10),
             shadow=(120, 50, 20))
        text(a, "条", x + w1 + wn + 16, 398, (230, 200, 160))
    return a


# ---------------------------------------------------------------- bedroom
def _bubble(a, x, y, s, p):
    tw = text_width(s) * 2
    w, h = tw + 16, 34
    x0, y0 = int(x - w / 2), int(y - h - int((1 - p) * 10))
    rect(a, x0 + 2, y0, w - 4, h, (250, 246, 236))
    rect(a, x0, y0 + 2, w, h - 4, (250, 246, 236))
    for k in range(6):
        hline(a, x0 + 18 - k, x0 + 18 + k // 2, y0 + h + 5 - k, (250, 246, 236))
    from engine import border as _b
    m = np.zeros((H, W), bool)
    m[max(0, y0):y0 + h, max(0, x0 + 2):x0 + w - 2] = True
    m[max(0, y0 + 2):y0 + h - 2, max(0, x0):x0 + w] = True
    paint(a, _b(dilate(m)), (40, 24, 32))
    text(a, s, x0 + w / 2, y0 + 3, (40, 24, 32), scale=2, align="center", hl=(214, 64, 52))


def bedroom(t):
    import scene_bedroom as B
    if t >= E.BRAIN_CUT:
        b = brainstage(t)
        if t < E.BRAIN_CUT + 0.25:
            return xfade(_bedroom_raw(t), b, (t - E.BRAIN_CUT) / 0.25)
        return b
    return _bedroom_raw(t)


def _bedroom_raw(t):
    import scene_bedroom as B
    a = new()
    c0, c1 = E.CLOCK_FF
    mins = int(lerp(2 * 60 + 47, 3 * 60 + 47, smooth((t - c0) / (c1 - c0))))
    B.draw(a, t, 0, "hand", "open", "%02d:%02d" % (mins // 60, mins % 60), E.FEED)
    if E.BUBBLE_T <= t < E.BUBBLE_T + 1.9:
        _bubble(a, 132, 318, "{最后一条}！", pop(t, E.BUBBLE_T, 0.2))
    z0, z1 = E.ZOOM
    if t > z0:
        p = smooth((t - z0) / (z1 - z0))
        a = zoom(a, lerp(180, 104, p), lerp(320, 360, p), 1 + 1.8 * p)
    S.vignette(a, 0.7)
    if E.PLUS1H_T <= t < z0:
        q = pop(t, E.PLUS1H_T)
        S.label(a, "02:47 → 03:47", 180, 108 + int((1 - q) * 14), "gold", scale=2, color=(252, 214, 120))
        text(a, "+1 小时", 180, 150, (238, 96, 80), scale=2, align="center", outline=(30, 10, 12),
             alpha=q)
    return a


# ------------------------------------------------------------ brain stage
@lru_cache(maxsize=1)
def brain_art():
    w, h = 100, 76
    yy, xx = np.mgrid[0:h, 0:w].astype(float)
    ell = lambda cx, cy, rx, ry: ((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2 <= 1
    cere = (ell(50, 30, 46, 28) & (yy < 46)) | ell(44, 46, 30, 12) | ell(18, 38, 16, 14)
    cereb = ell(76, 50, 17, 10)
    stem = mask_poly([(58, 46), (70, 46), (73, 64), (69, 72), (62, 72), (59, 62)], w, h)
    P = [(255, 206, 214), (242, 160, 180), (214, 114, 148), (166, 72, 114)]
    SUL, OUT = (114, 40, 86), (62, 22, 52)
    s = np.zeros((h, w, 4), np.uint8)
    s[stem] = (206, 120, 140, 255)
    s[stem & (xx > 66)] = (170, 88, 118, 255)
    s[cereb] = (214, 120, 150, 255)
    cb_lines = cereb & (((yy - 50) + 0.08 * (xx - 76) ** 2 / 4).astype(int) % 3 == 0)
    s[cb_lines] = (150, 64, 104, 255)
    # dome shading of the cerebrum
    nx, ny = (xx - 46) / 46, (yy - 32) / 30
    lam = -0.55 * nx - 0.7 * ny + 0.45 * np.sqrt(np.clip(1 - nx ** 2 - ny ** 2, 0, 1))
    tone = np.clip((lam + 0.5) * 2.2, 0, 3.99).astype(int)
    for i in range(4):
        s[cere & (tone == i)] = P[3 - i] + (255,)
    n = value_noise(h, w, 6.5, 3, 2)
    sulc = cere & (np.abs(n - 0.5) < 0.045)
    inner = cere & ~dilate(~cere, 2)
    sulc &= inner
    # main fissures
    fiss = np.zeros((h, w), bool)
    for x in range(14, 66):
        y = int(44 - (x - 14) * 0.2 + 2 * np.sin(x * 0.3))
        fiss[y, x] = True
    for k in range(30):
        fiss[int(4 + k * 1.05), int(52 - k * 0.45 + np.sin(k * 0.6))] = True
    sulc |= fiss & cere
    s[sulc] = SUL + (255,)
    hl = np.roll(np.roll(sulc, -1, 0), -1, 1) & cere & ~sulc
    s[hl] = P[0] + (255,)
    full = cere | cereb | stem
    s[border(full)] = OUT + (255,)
    s[border(cere) & cereb] = OUT + (255,)
    return s


def _bez(p0, p1, p2, u):
    return ((1 - u) ** 2 * p0[0] + 2 * (1 - u) * u * p1[0] + u * u * p2[0],
            (1 - u) ** 2 * p0[1] + 2 * (1 - u) * u * p1[1] + u * u * p2[1])


def brainstage(t, label=True):
    a = new(S.BG)
    S.stage(a, 426)
    S.spotlight(a, 180, 60, 426, 70, 280, (140, 140, 200), 0.34)
    bx, by = 80, 168 + int(np.sin(t * 1.6) * 2)
    glow(a, 180, by + 70, 130, (90, 40, 70), 0.35, ry=90)
    blit(a, scale_sprite(brain_art(), 2), bx, by)
    vta, nac, pfc = (bx + 124, by + 96), (bx + 70, by + 84), (bx + 38, by + 56)
    for k in range(0, 21):
        u = k / 20
        for p0, p1, p2 in ((vta, (bx + 100, by + 70), nac), (vta, (bx + 90, by + 30), pfc)):
            x, y = _bez(p0, p1, p2, u)
            if k % 2 == 0:
                pset(a, x, y, (255, 214, 110))
    for tb in E.BURSTS:
        dt = t - tb
        if 0 <= dt < 1.2:
            for j in range(12):
                u = (dt - j * 0.035) / 0.5
                if 0 <= u <= 1:
                    for p0, p1, p2 in ((vta, (bx + 100, by + 70), nac), (vta, (bx + 90, by + 30), pfc)):
                        x, y = _bez(p0, p1, p2, u)
                        rect(a, x - 1, y - 1, 3, 3, (255, 244, 170))
            if dt > 0.45:
                k = clamp01((dt - 0.45) / 0.7)
                glow(a, nac[0], nac[1], 20 + 40 * k, (255, 200, 90), 0.9 * (1 - k))
                glow(a, pfc[0], pfc[1], 14 + 30 * k, (255, 200, 90), 0.6 * (1 - k))
    if label and t >= E.DOPA_LABEL_T:
        q = pop(t, E.DOPA_LABEL_T)
        S.label(a, "多巴胺", 180, 98 + int((1 - q) * 12), "gold", scale=2, color=(252, 214, 120))
        text(a, "DOPAMINE", 180, 138, (190, 170, 140), align="center", alpha=q)
    S.vignette(a, 0.8)
    return a


# --------------------------------------------------------------- molecule
def _molecule(a, cx, cy, ang, col=(246, 232, 200), r=2.0):
    R = 34
    v = [(cx + R * np.cos(np.radians(-90 + 60 * k) + ang), cy + R * np.sin(np.radians(-90 + 60 * k) + ang))
         for k in range(6)]
    for k in range(6):
        thick(a, *v[k], *v[(k + 1) % 6], r, col)
    for k in (0, 2, 4):  # inner double bonds
        p, q = v[k], v[(k + 1) % 6]
        sx, sy = (cx - p[0]) * 0.22, (cy - p[1]) * 0.22
        tx, ty = (cx - q[0]) * 0.22, (cy - q[1]) * 0.22
        thick(a, p[0] + sx + (q[0] - p[0]) * 0.18, p[1] + sy + (q[1] - p[1]) * 0.18,
              q[0] + tx - (q[0] - p[0]) * 0.18, q[1] + ty - (q[1] - p[1]) * 0.18, 0.8, col)

    def rot(dx, dy):
        c, s = np.cos(ang), np.sin(ang)
        return dx * c - dy * s, dx * s + dy * c
    # ethylamine chain from v1
    p1 = (v[1][0] + rot(29, 17)[0], v[1][1] + rot(29, 17)[1])
    p2 = (p1[0] + rot(29, -17)[0], p1[1] + rot(29, -17)[1])
    p3 = (p2[0] + rot(20, 12)[0], p2[1] + rot(20, 12)[1])
    thick(a, *v[1], *p1, r, col)
    thick(a, *p1, *p2, r, col)
    thick(a, *p2, *p3, r, col)
    text(a, "NH₂", p3[0] + 2, p3[1] - 12, (140, 210, 255), scale=2, outline=(20, 18, 30))
    o5 = (v[5][0] + rot(-26, -15)[0], v[5][1] + rot(-26, -15)[1])
    o4 = (v[4][0] + rot(-26, 15)[0], v[4][1] + rot(-26, 15)[1])
    thick(a, *v[5], *o5, r, col)
    thick(a, *v[4], *o4, r, col)
    text(a, "HO", o5[0] - 2, o5[1] - 18, (255, 140, 120), scale=2, align="right", outline=(20, 18, 30))
    text(a, "HO", o4[0] - 2, o4[1] - 12, (255, 140, 120), scale=2, align="right", outline=(20, 18, 30))


def _card(a, x, y, w, title, sub, hl=False, dimmed=False):
    S.panel(a, x, y, w, 56, "gold", fill=(34, 26, 22) if not hl else (52, 36, 18))
    text(a, title, x + w / 2, y + 8, (252, 206, 96) if hl else CREAM, scale=2, align="center")
    text(a, sub, x + w / 2, y + 38, (190, 170, 140), align="center")
    if dimmed:
        from engine import dim
        sub_a = a[y:y + 56, x:x + w]
        sub_a[:] = (sub_a * 0.45).astype(np.uint8)


def molecule(t):
    a = new(S.BG)
    S.stage(a, 426)
    S.spotlight(a, 180, 60, 426, 70, 290, (150, 140, 190), 0.3)
    t0 = SCENE_T["molecule"][0]
    q = pop(t, t0 + 0.05, 0.35)
    glow(a, 176, 200, 120, (90, 70, 40), 0.45 * q)
    _molecule(a, 158, 204, 0.06 * np.sin(t * 1.3))
    S.label(a, "C₈H₁₁NO₂ · 多巴胺分子", 180, 100, "goldtag", color=(230, 210, 170))
    if t >= E.HAPPY_CARD_T:
        k = pop(t, E.HAPPY_CARD_T)
        struck = t >= E.STRIKE_T
        _card(a, 26, 306 + int((1 - k) * 20), 146, "快乐分子", "Like · 喜欢", dimmed=struck)
        if struck:
            u = clamp01((t - E.STRIKE_T) / 0.12)
            v = clamp01((t - E.STRIKE_T - 0.12) / 0.12)
            thick(a, 40, 314, 40 + 118 * u, 314 + 42 * u, 2.2, (226, 54, 44))
            if v > 0:
                thick(a, 158, 314, 158 - 118 * v, 314 + 42 * v, 2.2, (226, 54, 44))
    if t >= E.WANT_CARD_T:
        k = pop(t, E.WANT_CARD_T, 0.3)
        glow(a, 262, 334, 90, (200, 140, 40), 0.55 * k)
        _card(a, 188, 306 + int((1 - k) * 24), 146, "[渴望分子]", "Want · 想要", hl=True)
        for j in range(5):
            ph = t * 3 + j * 1.3
            S.sparkle(a, int(196 + (j * 37) % 140), int(300 + (j * 23) % 60), 1 + int(2 * abs(np.sin(ph))))
    S.vignette(a, 0.8)
    return a


# ---------------------------------------------------------- want / like
def wantlike(t):
    a = new(S.BG)
    S.stage(a, 430)
    S.spotlight(a, 180, 60, 430, 70, 260, (140, 150, 210), 0.3)
    t0 = SCENE_T["wantlike"][0]
    k = pop(t, t0 + 0.05, 0.3)
    y0 = 118 + int((1 - k) * 20)
    S.panel(a, 26, y0, 308, 178, "blue", fill=(18, 22, 40))
    S.label(a, "◆ 多巴胺 · 属性面板", 180, y0 - 12, "blue", color=(220, 236, 255))
    rows = [("满足", E.SATISFY_T, 1, (130, 200, 150)), ("想要", E.WANT_T, 10, (255, 150, 60))]
    for i, (name, tt, full, col) in enumerate(rows):
        ry = y0 + 32 + i * 62
        text(a, name, 44, ry, CREAM, scale=2)
        fill = full * smooth((t - tt) / 0.45) if t >= tt else 0
        for s_ in range(10):
            x = 104 + s_ * 18
            on = s_ < fill
            c = col if on else (40, 44, 70)
            if on and full == 10 and fill >= 9.9 and int(t * 8) % 2 == 0:
                c = (255, 230, 120)
            rect(a, x, ry + 4, 15, 20, c)
            if on:
                hline(a, x, x + 14, ry + 4, tuple(min(255, v + 60) for v in c))
        if t >= tt:
            v = "%d/10" % round(fill) if full < 10 or fill < 9.9 else "MAX"
            text(a, v, 326 - 8, ry + 26, (255, 214, 90) if v == "MAX" else (160, 170, 200), align="right")
    text(a, "多巴胺管的是“想要”，不管“满足”", 180, y0 + 154, (130, 140, 180), align="center")
    expr = "excited" if t >= E.WANT_T else "glow"
    S.put(a, C.stand(expr, "phone", bob=int(t * 3) % 2), 180, 430, k=3)
    glow(a, 180, 380, 40, (60, 160, 200), 0.35)
    S.vignette(a, 0.8)
    return a


# ----------------------------------------------------------------- carrot
CARROT = sprite([
    "..g.g..",
    "..ggg..",
    ".gGgGg.",
    "..ooo..",
    "..oOo..",
    "..ooo..",
    "..oOo..",
    "...oo..",
    "...o...",
    "...o...",
], {"g": (80, 190, 90), "G": (40, 130, 70), "o": (250, 140, 40), "O": (220, 100, 30)})


@lru_cache(maxsize=1)
def _carrot_bg():
    a = new((10, 12, 26))
    from engine import vgrad
    vgrad(a, 0, 0, W, 340, [(8, 10, 22), (14, 18, 40), (24, 30, 62)])
    rng = np.random.default_rng(2)
    for _ in range(70):
        x, y = rng.integers(0, W), rng.integers(70, 300)
        pset(a, x, y, (80, 90, 140) if rng.random() < 0.7 else (200, 210, 255))
    return a


def carrot(t):
    a = _carrot_bg().copy()
    v = 120.0
    # far hills
    for x in range(W):
        h1 = 300 + 18 * np.sin((x + t * 24) * 0.02) + 10 * np.sin((x + t * 24) * 0.051)
        vline(a, x, int(h1), 340, (22, 28, 58))
    rect(a, 0, 340, W, H - 340, (34, 46, 84))
    hline(a, 0, W - 1, 340, (70, 90, 140))
    rng = np.random.default_rng(5)
    for _ in range(60):
        gx, gy = rng.integers(0, W * 2), rng.integers(346, 640)
        x = int((gx - t * v * (0.6 + (gy - 340) / 300)) % (W + 20)) - 10
        vline(a, x, gy - 3, gy, (84, 108, 164))
        pset(a, x - 1, gy - 2, (84, 108, 164))
        pset(a, x + 1, gy - 1, (84, 108, 164))
    # dotted path
    for k in range(0, 40):
        x = int((k * 14 - t * v) % (W + 28)) - 14
        y = 412 + int(4 * np.sin((x + t * v) * 0.03))
        rect(a, x, y, 3, 3, (90, 210, 230))
    fr = int(t * 10) % 4
    cx, fy = 132, 424
    S.shadow(a, cx, fy, 44, 7, 0.5)
    # rod strapped to the back (drawn first so the head covers it) + dangling carrot
    sx, sy = cx - 26, fy - 64 + (fr % 2) * 4
    tip = (cx + 152, fy - 246)
    thick(a, sx, sy, *tip, 1.6, (150, 110, 70))
    thick(a, sx, sy, *tip, 0.6, (190, 150, 100))
    w, h = S.put(a, C.run_side(fr), cx, fy, k=4)
    sw = np.sin(t * 5.5) * 0.22
    cx2, cy2 = tip[0] + np.sin(sw) * 96, tip[1] + np.cos(sw) * 96
    line(a, *tip, cx2, cy2, (220, 220, 230))
    glow(a, cx2, cy2 + 20, 56, (220, 130, 40), 0.45)
    blit(a, scale_sprite(CARROT, 4), cx2 - 14, cy2)
    text(a, "满足", cx2, cy2 + 44, (252, 210, 110), scale=2, align="center", outline=(30, 20, 10))
    # speed lines
    for k in range(6):
        y = 250 + k * 22
        x = int((k * 97 - t * 520) % 460) - 60
        hline(a, x, x + 26, y, (90, 110, 160))
    S.label(a, "距离满足：1 cm", 180, 106, "goldtag", color=(252, 214, 120))
    text(a, "（永远都是 1 cm）", 180, 132, (130, 140, 180), align="center",
         alpha=smooth((t - word_t(7, "永远差一口")) / 0.3))
    S.vignette(a, 0.8)
    return a
