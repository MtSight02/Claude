"""Chapter 3: Skinner box, pocket slot machine, tolerance graph, the cage."""
from functools import lru_cache

import numpy as np

from engine import (W, H, new, rect, hline, vline, pset, line, thick, disc, text, glow, blit, sprite,
                    scale_sprite, mask_poly, mask_rrect, mask_ellipse, border, paint, smooth, lerp,
                    clamp01, back_out, text_width, dilate)
import style as S
import chibi as C
import events as E
from timeline import L, SCENE_T, word_t
from scenes_a import pop

CREAM = S.CREAM


# ------------------------------------------------------------ skinner box
def _presses(t):
    """(count, last press time, mode) at time t."""
    fixed = [p for p in E.FIXED_PRESSES if p <= t]
    rnd = [p for p in E.RANDOM_PRESSES if p <= t]
    count = len(fixed) + 9 * len(rnd) + (int((t - E.RANDOM_PRESSES[0]) * 3) % 7 if rnd else 0)
    last = max(fixed + rnd, default=-9)
    return count, last


PELLET = sprite([".bb.", "bBbb", "bbbb", ".bb."], {"b": (170, 110, 60), "B": (220, 160, 90)})


def skinner(t):
    a = new(S.BG)
    S.brick_wall(a, 60, 430)
    rect(a, 0, 430, W, H - 430, (22, 16, 20))
    hline(a, 0, W - 1, 430, (70, 44, 46))
    S.spotlight(a, 180, 60, 430, 80, 330, (200, 170, 140), 0.3)
    # box
    x0, y0, x1, y1 = 48, 196, 312, 404
    rect(a, x0, y0, x1 - x0, y1 - y0, (34, 38, 52))
    rect(a, x0, y1 - 18, x1 - x0, 18, (26, 28, 40))
    for x in range(x0 + 4, x1 - 2, 8):
        vline(a, x, y1 - 18, y1 - 1, (70, 74, 90))
    # dispenser tube + tray
    rect(a, 112, y0, 10, 150, (90, 110, 130))
    vline(a, 113, y0, y0 + 149, (170, 200, 220))
    rect(a, 100, y0 + 150, 34, 12, (120, 128, 150))
    rect(a, 100, y0 + 150, 34, 2, (200, 206, 220))
    # lever housing + lever
    rect(a, x0 + 4, 312, 16, 52, (110, 116, 136))
    rect(a, x0 + 4, 312, 16, 2, (180, 186, 206))
    cnt, last = _presses(t)
    down = 0 <= t - last < 0.12
    ly = 334 + (6 if down else 0)
    thick(a, x0 + 18, 334, x0 + 50, ly, 2.0, (210, 60, 50))
    disc(a, x0 + 50, ly, 3, (240, 90, 70))
    # pellets dropping + pile
    rewards = [p for p in E.FIXED_PRESSES] + E.RANDOM_REWARDS
    pile = 0
    for p in rewards:
        dt = t - p
        if 0 <= dt < 0.35:
            blit(a, scale_sprite(PELLET, 2), 113, y0 + 4 + dt / 0.35 * 140)
        elif dt >= 0.35:
            pile += 1
    for k in range(min(pile, 6)):
        blit(a, scale_sprite(PELLET, 2), 104 + (k % 3) * 9, y0 + 142 - (k // 3) * 5)
    # rat
    sleeping = E.SLEEP_T <= t < L(10, 0.0)
    frantic = t >= L(10, 0.0)
    if sleeping:
        spr = C.rat(0)
        S.put(a, spr, 196, y1 - 16, k=3)
        rect(a, 196 - 39 + 12, y1 - 16 - 54 + 27, 3, 3, (236, 234, 240))  # close the eye
        for i in range(3):
            u = (t * 0.7 + i / 3) % 1
            text(a, "z", 214 + u * 30, y1 - 70 - u * 40, (220, 220, 255), scale=1 + (u > 0.5),
                 outline=(40, 40, 70), alpha=1 - u)
    else:
        fr = 1 if (0 <= t - last < 0.16 and t >= E.FIXED_PRESSES[0]) else 0
        jitter = int(np.sin(t * 40) * 1) if frantic else 0
        S.put(a, C.rat(fr), 140 + (0 if fr else 8) + jitter, y1 - 16, k=3)
        if frantic:
            mark = "?" if int(t * 6) % 2 else "!"
            text(a, mark, 150, 284 - int(abs(np.sin(t * 9)) * 6), (255, 214, 90), scale=2,
                 outline=(40, 20, 10))
            if int(t * 5) % 3 == 0:
                rect(a, 178, 300, 2, 4, (150, 210, 255))
    # glass + frame
    gl = np.zeros((H, W), np.float32)
    gl[y0:y1, x0:x1] = 0.06
    from engine import light_field
    light_field(a, gl, 0, 0, (160, 200, 230))
    for k in range(3):
        line(a, x0 + 20 + k * 8, y0 + 40, x0 + 60 + k * 8, y0, (120, 150, 170))
    for (rx, ry, rw, rh) in ((x0 - 4, y0 - 6, x1 - x0 + 8, 6), (x0 - 4, y1, x1 - x0 + 8, 6),
                             (x0 - 4, y0 - 6, 4, y1 - y0 + 12), (x1, y0 - 6, 4, y1 - y0 + 12)):
        rect(a, rx, ry, rw, rh, (150, 154, 170))
    hline(a, x0 - 4, x1 + 3, y0 - 6, (220, 224, 236))
    # counter
    text(a, "按压次数", 206, 166, (220, 200, 170), align="right")
    S.odometer(a, 214, 164, cnt, ndig=4)
    # labels
    if t >= word_t(8, "斯金纳") - 0.1:
        q = pop(t, word_t(8, "斯金纳") - 0.1)
        S.label(a, "斯金纳箱 · 1930s", 180, 98 + int((1 - q) * 12), "gold", scale=2, color=(252, 214, 120))
    if L(9, 0.0) - 0.1 <= t < L(10, 0.0) - 0.05:
        S.label(a, "奖励：固定（按一次 = 1 颗）", 180, 136, "goldtag")
        if sleeping:
            S.label(a, "吃饱了，不按了", 252, 296, "goldtag", color=(160, 230, 170))
    elif t >= L(10, 0.0) - 0.05:
        blink = int(t * 6) % 2 == 0
        S.label(a, "奖励：随机 ？？？", 180, 136, "red", color=(255, 140, 120) if blink else CREAM)
    S.vignette(a, 0.75)
    return a


# --------------------------------------------------------- slot machine
def _icon(kind, sz=30):
    s = np.zeros((sz, sz, 4), np.uint8)
    yy, xx = np.mgrid[0:sz, 0:sz].astype(float)
    u, v = (xx - sz / 2 + 0.5) / (sz * 0.38), -(yy - sz / 2 + 2) / (sz * 0.38)
    if kind == "heart":
        m = (u * u + v * v - 1) ** 3 - u * u * v ** 3 < 0
        s[m] = (230, 50, 80, 255)
        s[m & (u < -0.2) & (v > 0.2)] = (255, 130, 150, 255)
    elif kind == "star":
        pts = []
        for k in range(10):
            r = 14 if k % 2 == 0 else 6
            ang = -np.pi / 2 + k * np.pi / 5
            pts.append((sz / 2 + r * np.cos(ang), sz / 2 + 1 + r * np.sin(ang)))
        m = mask_poly(pts, sz, sz)
        s[m] = (250, 200, 60, 255)
        s[m & (yy < sz / 2)] = (255, 236, 140, 255)
    elif kind == "gem":
        m = (np.abs(u) + np.abs(v) * 0.8 < 0.95) & (v < 0.6)
        s[m] = (70, 170, 250, 255)
        s[m & (v > 0.2)] = (160, 220, 255, 255)
    elif kind == "seven":
        s[:] = 0
    elif kind == "q":
        pass
    al = s[..., 3] > 0
    ring = dilate(al, 1) & ~al
    s[ring] = (30, 20, 30, 255)
    return s


ICONS = ["heart", "star", "gem", "seven", "q"]
STRIP = ["heart", "star", "gem", "heart", "seven", "star", "q", "gem"]


def _reel(a, x, y, w, h, pos, spinning):
    rect(a, x, y, w, h, (244, 238, 228))
    cell = h
    k0 = int(np.floor(pos))
    frac = pos - k0
    for j in (-1, 0, 1):
        kind = STRIP[(k0 - j) % len(STRIP)]
        cy = y + int((j + frac) * cell)
        if cy + cell < y or cy > y + h:
            continue
        if spinning:
            col = {"heart": (230, 60, 90), "star": (250, 200, 60), "gem": (70, 170, 250),
                   "seven": (220, 50, 50), "q": (150, 100, 220)}[kind]
            for xx in range(x + 8, x + w - 8, 3):
                y_a, y_b = max(y, cy + 6), min(y + h, cy + cell - 6)
                if y_b > y_a:
                    vline(a, xx, y_a, y_b, col)
            continue
        sub = new(alpha=True, w=w, h=cell)
        if kind == "seven":
            text(sub, "7", w / 2, 6, (220, 50, 50), scale=3, align="center", outline=(30, 20, 30))
        elif kind == "q":
            text(sub, "?", w / 2, 6, (150, 100, 220), scale=3, align="center", outline=(30, 20, 30))
        else:
            ic = _icon(kind)
            sub[(cell - 30) // 2:(cell - 30) // 2 + 30, (w - 30) // 2:(w - 30) // 2 + 30] = ic
        top = max(0, y - cy)
        bot = min(cell, y + h - cy)
        if bot > top:
            blit(a, sub[top:bot], x, cy + top)
    rect(a, x, y, w, 3, (180, 170, 160))
    rect(a, x, y + h - 3, w, 3, (180, 170, 160))


def _reel_pos(t, i):
    targets = [(0, 0, 1), (0, 0, 0), (0, 0, 0)]  # heart heart star / jackpot hearts
    pos, spinning = float((2, 6, 1)[i]), False  # idle: gem ? star
    for n, p in enumerate(E.PULLS):
        if t < p:
            break
        stop = E.STOPS[n][i]
        tgt = targets[n][i] + 8 * (6 + n * 4 + i * 2)
        if t < stop:
            pos, spinning = (t - p) * 22.0, True
        else:
            d = t - stop
            pos = tgt - 0.25 * np.exp(-d * 9) * np.cos(d * 30)
            spinning = False
    return pos, spinning


HEART = sprite([".rr.rr.", "rRrrrrr", "rrrrrrr", ".rrrrr.", "..rrr..", "...r..."],
               {"r": (240, 60, 90), "R": (255, 160, 180)})


def slot(t):
    a = new(S.BG)
    jack = clamp01(1 - (t - E.JACKPOT_T) / 1.6) if t >= E.JACKPOT_T else 0.0
    S.sunburst(a, 180, 250, t * 0.25, (70 + int(120 * jack), 50 + int(80 * jack), 20),
               (30, 22, 14), n=18, radius=430)
    S.vignette(a, 0.8)
    t0 = SCENE_T["slot"][0]
    k = pop(t, t0, 0.35)
    oy = int((1 - k) * 60)
    x0, y0, w, h = 92, 120 + oy, 176, 300
    # golden cabinet with bulbs
    S.panel(a, x0 - 8, y0 - 8, w + 16, h + 16, "gold", fill=(60, 40, 20))
    for j in range(0, (w + 16) // 12):
        on = (j + int(t * 6)) % 2 == 0 or jack > 0 and int(t * 12) % 2 == 0
        c = (255, 240, 160) if on else (120, 90, 40)
        disc(a, x0 - 2 + j * 12, y0 - 4, 2, c)
        disc(a, x0 - 2 + j * 12, y0 + h + 4, 2, c)
    pm = mask_rrect(x0, y0, w, h, 16)
    paint(a, pm, (30, 30, 40))
    paint(a, border(pm), (90, 90, 110))
    sx, sy, sw, sh = x0 + 10, y0 + 22, w - 20, h - 44
    rect(a, sx, sy, sw, sh, (26, 20, 44))
    rect(a, x0 + w // 2 - 14, y0 + 8, 28, 4, (60, 60, 76))  # speaker
    text(a, "推荐", sx + 8, sy + 6, (240, 240, 250))
    text(a, "关注", sx + 40, sy + 6, (130, 130, 150))
    # pull-to-refresh
    for p in E.PULLS:
        if 0 <= t - p < 0.45:
            u = smooth((t - p) / 0.3)
            hy = sy + 30 + int(u * 40)
            text(a, "↓ 下拉刷新", 180, sy + 28 + int(u * 8), (200, 190, 230), align="center", alpha=1 - u * 0.5)
            hand = sprite(["..w..", "..w..", ".www.", "wwwww", "wwwww", ".www."],
                          {"w": (250, 230, 210)})
            blit(a, scale_sprite(hand, 3), 200, hy)
    # reels
    rx, ry = sx + 8, sy + 92
    rect(a, rx - 4, ry - 4, sw - 8, 70, (200, 150, 60))
    for i in range(3):
        pos, sp = _reel_pos(t, i)
        _reel(a, rx + i * 44, ry, 40, 62, pos, sp)
    if E.NEAR_MISS_T <= t < E.PULLS[1]:
        S.label(a, "差一点！", 180, ry + 74, "red", color=(255, 160, 140))
    if E.PULLS[1] <= t < E.JACKPOT_T:
        text(a, "？？？", 180, ry + 76, (200, 160, 255), scale=2, align="center", outline=(20, 10, 30))
    if t >= E.JACKPOT_T:
        q = pop(t, E.JACKPOT_T, 0.3)
        text(a, "+99", 168, ry + 70 - int(q * 6), (255, 214, 90), scale=3, align="center",
             outline=(60, 20, 10), shadow=(160, 60, 20))
        blit(a, scale_sprite(HEART, 3), 222, ry + 78 - int(q * 6))
        for j in range(14):
            d = t - E.JACKPOT_T
            if d < 1.6:
                ang = j / 14 * 6.283
                r = 30 + d * 120
                hx, hy = 180 + np.cos(ang) * r, ry + 30 + np.sin(ang) * r * 0.8 + d * d * 60
                blit(a, scale_sprite(HEART, 2), hx, hy, alpha=1 - d / 1.6)
    S.label(a, "口袋老虎机", 180, y0 - 34, "gold", scale=2, color=(252, 214, 120))
    return a


# ----------------------------------------------------------------- graph
SPIKES = [70, 112, 152, 190, 226, 262, 298]


def _curve(xs, base0=196, base1=236):
    b = base0 + (base1 - base0) * np.clip((xs - 50) / 270, 0, 1)
    y = b.copy()
    for i, sx in enumerate(SPIKES):
        h = 62 - i * 6
        y -= h * np.exp(-((xs - sx) / 4.5) ** 2)
        y += (14 + i * 3) * np.exp(-((xs - sx - 13) / 9.0) ** 2)
    return y, b


def graph(t):
    a = new((12, 14, 24))
    for x in range(0, W, 20):
        vline(a, x, 90, 440, (18, 22, 36))
    for y in range(90, 440, 20):
        hline(a, 0, W - 1, y, (18, 22, 36))
    S.vignette(a, 0.8)
    x0, y0, x1, y1 = 22, 98, 338, 304
    rect(a, x0, y0, x1 - x0, y1 - y0, (16, 18, 30))
    for (rx, ry, rw, rh) in ((x0, y0, x1 - x0, 1), (x0, y1, x1 - x0, 1), (x0, y0, 1, y1 - y0), (x1, y0, 1, y1 - y0 + 1)):
        rect(a, rx, ry, rw, rh, (70, 70, 96))
    text(a, "多巴胺水平", x0 + 8, y0 + 6, (252, 214, 120))
    text(a, "时间 →", x1 - 4, y0 + 6, (110, 116, 150), align="right")
    vline(a, 40, y0 + 22, y1 - 6, (90, 96, 130))
    hline(a, 40, x1 - 8, y1 - 6, (90, 96, 130))
    g0, g1 = E.GRAPH_DRAW
    p = clamp01((t - g0) / (g1 - g0))
    xe = 40 + 290 * p
    xs = np.arange(40, 331, dtype=float)
    ys, bs = _curve(xs)
    # stimulus bars (growing)
    for i, sx in enumerate(SPIKES):
        if sx <= xe:
            hh = 6 + i * 3
            rect(a, sx - 2, y1 - 6 - hh, 5, hh, (80, 170, 220))
    text(a, "刺激", 44, y1 - 34, (80, 170, 220))
    # baseline (red dashed)
    for xx in range(40, 331):
        if xx <= xe and (xx // 5) % 2 == 0:
            pset(a, xx, int(bs[xx - 40]), (230, 70, 60))
    if xe > 60:
        text(a, "基线 ↓", min(xe, 300) + 2, int(bs[int(min(xe, 330)) - 40]) + 4, (230, 90, 70))
    # dips below baseline
    for xx in range(40, int(xe)):
        yc, yb = ys[xx - 40], bs[xx - 40]
        if yc > yb + 1:
            vline(a, xx, int(yb) + 1, int(yc), (120, 30, 40))
    for xx in range(40, int(xe)):
        thick(a, xx, ys[xx - 40], xx + 1, ys[min(len(ys) - 1, xx - 39)], 1.0, (252, 200, 80))
    if p < 1:
        glow(a, xe, ys[int(xe) - 40], 16, (255, 220, 120), 0.8)
    # volume panel / boring cards
    if E.VOLUME_T <= t < E.GREY_T[0] - 0.25:
        q = pop(t, E.VOLUME_T)
        py = 318 + int((1 - q) * 20)
        S.panel(a, 30, py, 300, 50, "gold")
        text(a, "大脑音量", 44, py + 10, CREAM, scale=2)
        lvl = 10 - sum(1 for s in E.VOLUME_STEPS if t >= s)
        for i in range(10):
            on = i < lvl
            hh = 6 + i * 2
            rect(a, 162 + i * 15, py + 40 - hh, 11, hh, (252, 200, 80) if on else (50, 46, 60))
    if t >= E.GREY_T[0] - 0.25:
        dull = t >= E.DULL_T
        names = [("读书", (90, 150, 230)), ("散步", (90, 200, 120)), ("发呆", (180, 160, 240))]
        for i, (nm, col) in enumerate(names):
            if t < E.GREY_T[i] - 0.15:
                continue
            q = pop(t, E.GREY_T[i] - 0.15)
            cx = 66 + i * 114
            cy = 318 + int((1 - q) * 16)
            c = tuple(int(sum(col) / 3 * 0.6) for _ in range(3)) if dull else col
            S.panel(a, cx - 48, cy, 96, 92, "gold" if not dull else "boss", fill=(28, 26, 36))
            _mini_icon(a, i, cx, cy + 38, c)
            text(a, nm, cx, cy + 62, (150, 150, 160) if dull else CREAM, scale=2, align="center")
            if dull:
                text(a, "无聊", cx + 28, cy + 4, (230, 70, 60), align="center", outline=(30, 10, 10))
    return a


def _mini_icon(a, i, cx, cy, c):
    if i == 0:  # book
        rect(a, cx - 18, cy - 14, 17, 24, c)
        rect(a, cx + 1, cy - 14, 17, 24, c)
        vline(a, cx, cy - 14, cy + 10, (30, 30, 40))
        for k in range(4):
            hline(a, cx - 14, cx - 5, cy - 9 + k * 5, (240, 240, 250))
            hline(a, cx + 5, cx + 14, cy - 9 + k * 5, (240, 240, 250))
    elif i == 1:  # tree
        disc(a, cx, cy - 6, 13, c)
        rect(a, cx - 3, cy + 4, 6, 10, (130, 90, 60) if c[0] != c[1] else (90, 90, 90))
    else:  # cloud
        disc(a, cx - 10, cy, 9, c)
        disc(a, cx + 2, cy - 6, 12, c)
        disc(a, cx + 13, cy + 1, 8, c)
        rect(a, cx - 10, cy, 24, 9, c)


# ------------------------------------------------------------------ cage
NOTES = ["♥ +1", "新消息", "@你", "99+", "直播中", "赞 +8", "红包"]


def _note(a, x, y, s, alpha=None, badge=True):
    tw = text_width(s)
    w, h = tw + 12, 18
    rect(a, x - w // 2, y, w, h, (244, 240, 246), alpha=alpha)
    rect(a, x - w // 2 + 1, y - 1, w - 2, 1, (244, 240, 246), alpha=alpha)
    rect(a, x - w // 2 + 1, y + h, w - 2, 1, (244, 240, 246), alpha=alpha)
    text(a, s, x, y + 2, (40, 30, 40), align="center", hl=(220, 50, 60), alpha=alpha)
    if badge:
        disc(a, x + w // 2 - 1, y, 4, (230, 50, 60))


def cage(t):
    a = new(S.BG)
    glow(a, 180, 290, 260, (110, 18, 34), 0.8, power=1.3)
    S.spotlight(a, 180, 60, 430, 60, 240, (200, 160, 170), 0.25)
    rect(a, 0, 430, W, H - 430, (18, 12, 16))
    cx, top, bot = 180, 176, 396
    rx = 78
    # orbiting notifications (back half)
    notes = []
    for i, s in enumerate(NOTES):
        ang = t * 0.6 + i / len(NOTES) * 6.283
        nx, ny = cx + np.cos(ang) * 150, 266 + np.sin(ang) * 26 + np.sin(t * 2 + i) * 6 - 40 + i * 12
        notes.append((np.sin(ang), nx, ny, s))
    for z, nx, ny, s in sorted(notes):
        if z < 0:
            _note(a, nx, ny, s, alpha=0.55)
    # cage back bars
    gold, gold_dk, gold_hi = (226, 170, 70), (120, 80, 30), (255, 230, 150)
    for j in range(12):
        th = j / 12 * 6.283
        x = cx + np.sin(th) * rx
        if np.cos(th) < 0:
            vline(a, int(x), top, bot, gold_dk)
    S.shadow(a, cx, bot + 4, 90, 10, 0.6)
    fr = int(t * 4) % 2
    S.put(a, C.sit_phone("glow", fr), cx, bot - 2, k=3)
    glow(a, cx, bot - 50, 50, (60, 170, 220), 0.5)
    # front bars + dome + base
    for j in range(12):
        th = j / 12 * 6.283
        x = cx + np.sin(th) * rx
        if np.cos(th) >= 0:
            rect(a, int(x) - 1, top, 3, bot - top, gold)
            vline(a, int(x) - 1, top, bot, gold_hi)
    dome = mask_ellipse(cx, top, rx, 58) & (np.arange(H)[:, None] <= top)
    inner = mask_ellipse(cx, top, rx - 3, 55)
    paint(a, dome & ~inner, gold)
    for j in range(-3, 4):
        x = cx + j * rx / 4
        yb = top - int(np.sqrt(max(0, 1 - ((x - cx) / rx) ** 2)) * 58)
        line(a, x, top, cx, top - 58, gold_dk)
    rect(a, cx - rx - 6, bot, 2 * rx + 12, 12, gold)
    rect(a, cx - rx - 6, bot, 2 * rx + 12, 2, gold_hi)
    rect(a, cx - rx - 6, bot + 10, 2 * rx + 12, 2, gold_dk)
    rect(a, cx - rx, top - 2, 2 * rx, 4, gold)
    disc(a, cx, top - 64, 7, gold)
    disc(a, cx, top - 64, 4, S.BG)
    vline(a, cx, 60, top - 71, (120, 110, 100))
    # front notifications
    for z, nx, ny, s in sorted(notes):
        if z >= 0:
            _note(a, nx, ny, s)
    for p in E.PINGS:
        if 0 <= t - p < 0.25:
            glow(a, 180, 300, 120, (120, 30, 40), 0.4 * (1 - (t - p) / 0.25))
    if t >= E.Q_T:
        q = pop(t, E.Q_T, 0.3)
        r = 1 + 0.08 * np.sin(t * 10)
        glow(a, cx, 262, 50 * r, (255, 200, 90), 0.6 * q)
        rect(a, cx - 18, 240, 36, 40, (250, 246, 236))
        rect(a, cx - 20, 242, 40, 36, (250, 246, 236))
        text(a, "?", cx, 246, (220, 60, 60), scale=2, align="center")
        S.label(a, "下一次 · 可能", cx, 200, "goldtag", color=(252, 214, 120))
    S.vignette(a, 0.9)
    return a
