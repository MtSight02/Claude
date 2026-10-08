"""Chapter 4: unlock, skill pack, sunrise, follow."""
from functools import lru_cache

import numpy as np

from engine import (W, H, new, rect, hline, vline, pset, line, thick, disc, text, glow, blit, sprite,
                    scale_sprite, mask_poly, mask_rrect, mask_ellipse, border, paint, smooth, lerp,
                    clamp01, back_out, text_width, vgrad)
import style as S
import chibi as C
import events as E
from timeline import L, SCENE_T, word_t
from scenes_a import pop, brain_art

CREAM = S.CREAM


# ---------------------------------------------------------------- unlock
def _lock(a, cx, cy, open_k, col):
    sh_up = int(open_k * 10)
    for r in (9, 8):
        pass
    for ang in np.linspace(np.pi, 2 * np.pi, 40):
        x = cx + np.cos(ang) * 9
        y = cy - 8 - sh_up + np.sin(ang) * 10
        disc(a, x, y, 1.8, (190, 190, 200))
    vline(a, cx - 9, cy - 8 - sh_up, cy - 4, (190, 190, 200))
    if open_k < 0.5:
        vline(a, cx + 9, cy - 8 - sh_up, cy - 4, (190, 190, 200))
    rect(a, cx - 13, cy - 5, 26, 20, col)
    rect(a, cx - 13, cy - 5, 26, 2, tuple(min(255, v + 50) for v in col))
    rect(a, cx - 2, cy + 1, 4, 8, (40, 30, 30))


def unlock(t):
    a = new(S.BG)
    S.stage(a, 430)
    u = clamp01((t - E.UNLOCK_T) / 0.35)
    if t >= E.UNLOCK_T:
        S.sunburst(a, 180, 220, t * 0.2, (70, 54, 24), (24, 20, 16), n=16, fade=smooth(u), radius=300)
        rect(a, 0, 430, W, H - 430, (26, 22, 32))
    S.spotlight(a, 180, 60, 430, 70, 250, (160, 160, 200), 0.3)
    x0, y0, w, h = 96, 116, 168, 176
    S.panel(a, x0, y0, w, h, "gold" if u >= 1 else "boss", fill=(24, 22, 30))
    br = brain_art()
    if u < 1:
        g = br.copy()
        m = g[..., 3] > 0
        lum = g[..., :3].mean(-1)
        g[..., 0] = np.where(m, lum * 0.55, 0)
        g[..., 1] = np.where(m, lum * 0.55, 0)
        g[..., 2] = np.where(m, lum * 0.62, 0)
        blit(a, g, 130, 140, alpha=1 - u)
    if u > 0:
        blit(a, br, 130, 140, alpha=u)
        glow(a, 180, 178, 70, (120, 90, 40), 0.4 * u)
    _lock(a, 180, 236, smooth((t - E.UNLOCK_T) / 0.25), (200, 160, 70) if u > 0.5 else (120, 120, 130))
    if u < 1:
        text(a, "敏感度 · 已下调", 180, 266, (150, 150, 160), align="center")
    else:
        text(a, "敏感度 · 可以恢复", 180, 266, (130, 240, 150), align="center")
        for j in range(6):
            ph = t * 4 + j
            S.sparkle(a, int(100 + (j * 53) % 160), int(124 + (j * 31) % 150), 1 + int(2 * abs(np.sin(ph))))
    expr = "happy" if u >= 1 else "normal"
    S.put(a, C.stand(expr, bob=int(t * 3) % 2), 180, 430, k=3)
    S.vignette(a, 0.8)
    return a


# ---------------------------------------------------------------- skills
def _chest(a, cx, by, open_k):
    rect(a, cx - 44, by - 34, 88, 34, (130, 76, 40))
    rect(a, cx - 44, by - 34, 88, 3, (170, 104, 56))
    for x in (cx - 44, cx - 4, cx + 36):
        rect(a, x, by - 34, 8, 34, (214, 160, 62))
    rect(a, cx - 6, by - 28, 12, 10, (252, 212, 120))
    rect(a, cx - 2, by - 25, 4, 5, (60, 40, 20))
    lid_h = int(20 * (1 - open_k)) + 6
    rect(a, cx - 46, by - 34 - lid_h, 92, lid_h, (150, 90, 46))
    rect(a, cx - 46, by - 34 - lid_h, 92, 3, (190, 120, 64))
    if open_k > 0:
        glow(a, cx, by - 40, 70, (255, 210, 110), 0.8 * open_k, ry=40)


def _card_back(w, h):
    c = new(alpha=True, w=w, h=h)
    S.panel(c, 0, 0, w, h, "gold", fill=(48, 34, 24))
    text(c, "?", w / 2, h / 2 - 16, (252, 212, 120), scale=3, align="center")
    return c


SKILLS = [
    ("技能 1", "关掉通知", "只留电话和家人的消息"),
    ("技能 2", "手机放远", "睡前放到伸手够不到的地方"),
    ("技能 3", "慢多巴胺", "运动 · 阅读 · 晒太阳"),
]


def _skill_icon(c, i, cx, cy):
    if i == 0:  # bell + slash
        disc(c, cx, cy - 4, 22, (230, 180, 70))
        rect(c, cx - 22, cy - 4, 45, 22, (230, 180, 70))
        rect(c, cx - 28, cy + 16, 57, 6, (250, 210, 110))
        disc(c, cx, cy + 26, 5, (200, 150, 60))
        disc(c, cx - 8, cy - 14, 5, (255, 236, 160))
        thick(c, cx - 30, cy - 28, cx + 30, cy + 30, 3.0, (226, 54, 44))
        disc(c, cx + 22, cy - 22, 9, (226, 54, 44))
        text(c, "99", cx + 22, cy - 28, (255, 255, 255), align="center")
    elif i == 1:  # bed .... phone far away
        rect(c, cx - 50, cy + 4, 40, 12, (120, 110, 190))
        rect(c, cx - 50, cy - 2, 12, 8, (240, 240, 250))
        rect(c, cx - 54, cy - 10, 4, 34, (150, 100, 70))
        rect(c, cx - 50, cy + 16, 44, 4, (150, 100, 70))
        for k in range(4):
            rect(c, cx - 2 + k * 9, cy + 4, 5, 3, (252, 212, 120))
        rect(c, cx + 34, cy - 14, 16, 28, (40, 40, 52))
        rect(c, cx + 36, cy - 11, 12, 20, (60, 70, 90))
        text(c, "zZ", cx + 42, cy - 34, (190, 200, 255), align="center")
    else:  # shoe, book, sun
        disc(c, cx - 38, cy, 14, (255, 200, 80))
        for k in range(8):
            ang = k * np.pi / 4
            thick(c, cx - 38 + np.cos(ang) * 18, cy + np.sin(ang) * 18,
                  cx - 38 + np.cos(ang) * 23, cy + np.sin(ang) * 23, 1.2, (255, 200, 80))
        rect(c, cx - 10, cy - 12, 18, 24, (90, 150, 230))
        rect(c, cx - 10 + 18, cy - 12, 2, 24, (240, 240, 250))
        rect(c, cx + 10, cy - 12, 18, 24, (90, 150, 230))
        rect(c, cx + 34, cy + 2, 26, 10, (236, 90, 80))
        rect(c, cx + 34, cy - 6, 12, 10, (236, 90, 80))
        rect(c, cx + 34, cy + 10, 26, 3, (250, 250, 250))


def _card_front(i, w, h):
    c = new(alpha=True, w=w, h=h)
    S.panel(c, 0, 0, w, h, "gold", fill=(36, 28, 22))
    tag, title, desc = SKILLS[i]
    S.label(c, tag, w / 2, 12, "goldtag", color=(252, 212, 120))
    rect(c, 14, 44, w - 28, 120, (22, 30, 44))
    vgrad(c, 14, 44, w - 28, 120, [(30, 44, 70), (20, 26, 40)])
    _skill_icon(c, i, w // 2, 104)
    text(c, title, w / 2, 178, (252, 236, 210), scale=2, align="center")
    text(c, desc, w / 2, 214, (200, 184, 150), align="center")
    for k in range(3):
        rect(c, w / 2 - 22 + k * 16, 240, 12, 4, (252, 212, 120) if k <= i else (80, 60, 40))
    return c


@lru_cache(maxsize=8)
def _cards(i, w, h):
    return _card_back(w, h), _card_front(i, w, h)


def _flip(a, back, front, k, x, y):
    """Horizontal card flip: k 0..1."""
    src = back if k < 0.5 else front
    sx = abs(np.cos(k * np.pi))
    w = max(1, int(src.shape[1] * sx))
    cols = (np.arange(w) / sx).astype(int).clip(0, src.shape[1] - 1)
    s = src[:, cols]
    blit(a, s, x + (src.shape[1] - w) // 2, y)


def skills(t):
    a = new(S.BG)
    s0 = E.SKILL_T[0]
    if t < s0:
        S.sunburst(a, 180, 300, t * 0.15, (60, 46, 22), (22, 18, 14), n=16, radius=360)
        S.vignette(a, 0.85)
        q = pop(t, E.CHEST_T)
        S.label(a, "技能包 · 今晚就能用", 180, 100 + int((1 - q) * 10), "gold", scale=2, color=(252, 214, 120))
        open_k = smooth((t - E.CHEST_T - 0.3) / 0.4)
        _chest(a, 180, 420, open_k)
        for j in range(3):
            tj = E.CARDS_T + j * 0.18
            if t < tj:
                continue
            k = pop(t, tj, 0.35)
            cx = 76 + j * 104
            cy = int(lerp(380, 196, k)) + int(np.sin(t * 2 + j) * 4)
            back, _ = _cards(j, 88, 120)[0], None
            blit(a, _card_back(88, 120), cx - 44, cy - 60)
        return a
    i = max(j for j in range(3) if t >= E.SKILL_T[j])
    ti = E.SKILL_T[i]
    S.sunburst(a, 180, 262, t * 0.25, (96, 70, 28), (30, 24, 16), n=18, radius=420)
    S.vignette(a, 0.85)
    w, h = 224, 254
    back, front = _cards(i, w, h)
    k = clamp01((t - ti) / 0.45)
    yy = 128 + int((1 - smooth(k * 2)) * 30)
    _flip(a, back, front, smooth(k), 180 - w // 2, yy)
    if k >= 1:
        for j in range(6):
            ph = t * 4 + j * 1.7
            S.sparkle(a, int(70 + (j * 61) % 220), int(120 + (j * 47) % 250), 1 + int(2 * abs(np.sin(ph))))
    # done marks for previous skills
    for j in range(3):
        c = (252, 212, 120) if j < i else (90, 70, 40)
        S.panel(a, 116 + j * 46, 394, 36, 26, "goldtag" if j <= i else "red", fill=(30, 24, 20))
        if j < i:
            S.check(a, 129 + j * 46, 403, 1, (252, 212, 120))
        else:
            text(a, str(j + 1), 134 + j * 46, 400, c, align="center")
    return a


# --------------------------------------------------------------- sunrise
@lru_cache(maxsize=1)
def _sky():
    a = new((0, 0, 0))
    vgrad(a, 0, 0, W, 420, [(34, 46, 110), (90, 80, 160), (220, 120, 150), (255, 170, 120), (255, 214, 150)])
    return a


def sunrise(t):
    t0, t1 = SCENE_T["sunrise"]
    p = clamp01((t - t0) / (t1 - t0))
    a = _sky().copy()
    sy = int(330 - p * 40)
    glow(a, 250, sy, 150, (255, 190, 110), 0.7, power=1.2)
    disc(a, 250, sy, 20, (255, 240, 190))
    disc(a, 250, sy, 16, (255, 250, 220))
    # clouds
    for j, (cx, cy, sc) in enumerate(((60, 150, 1.0), (230, 120, 0.8), (320, 190, 0.7), (130, 230, 0.6))):
        x = (cx + t * 6 * sc) % (W + 80) - 40
        for dx, dy, r in ((0, 0, 12), (14, -6, 14), (30, 0, 11), (16, 6, 10)):
            disc(a, x + dx * sc, cy + dy * sc, r * sc, (255, 200, 200))
        rect(a, x, cy + 4 * sc, 30 * sc, 6 * sc, (255, 200, 200))
        hline(a, int(x), int(x + 30 * sc), int(cy + 10 * sc), (220, 140, 170))
    # hills
    for k, (col, base, amp, fr, sp) in enumerate((((120, 90, 150), 340, 26, 0.018, 3),
                                                   ((70, 96, 120), 368, 20, 0.03, 6),
                                                   ((52, 120, 88), 392, 14, 0.022, 0))):
        for x in range(W):
            y = int(base - amp * np.sin((x + t * sp) * fr + k) - 6 * np.sin((x + t * sp) * fr * 2.7))
            vline(a, x, y, H, col)
            if k == 2:
                pset(a, x, y, (110, 190, 110))
    rect(a, 0, 430, W, H - 430, (40, 92, 66))
    # trees on the middle hill
    for tx in (30, 64, 300, 336):
        y = int(368 - 20 * np.sin(tx * 0.03 + 1))
        for r in range(9):
            hline(a, tx - r // 2 - 1, tx + r // 2 + 1, y - 18 + r * 2, (40, 74, 76))
        vline(a, tx, y, y + 4, (60, 50, 50))
    # birds
    for j in range(4):
        bx = (t * 30 + j * 70) % (W + 40) - 20
        by = 160 + j * 18 + np.sin(t * 2 + j) * 4
        flap = int(t * 6 + j) % 2
        pset(a, bx, by, (60, 40, 60))
        pset(a, bx - 1, by - flap, (60, 40, 60)); pset(a, bx - 2, by - 1 - flap, (60, 40, 60))
        pset(a, bx + 1, by - flap, (60, 40, 60)); pset(a, bx + 2, by - 1 - flap, (60, 40, 60))
    yb = 404
    S.shadow(a, 196, yb + 2, 40, 6, 0.4)
    S.put(a, C.sit_back(), 196, yb + 4, k=3)
    glow(a, 196, yb - 60, 50, (255, 170, 110), 0.2)
    return a


# ---------------------------------------------------------------- follow
HAND = sprite([
    "..kk......",
    ".kwwk.....",
    ".kwwk.....",
    ".kwwkkk...",
    ".kwwwwwkk.",
    "kkwwwwwwwk",
    "kwwwwwwwwk",
    ".kwwwwwwk.",
    "..kwwwwk..",
    "..kkkkkk..",
], {"k": (30, 20, 30), "w": (250, 246, 240)})


def follow(t):
    a = new(S.BG)
    S.stage(a, 430)
    S.spotlight(a, 120, 60, 430, 50, 200, (170, 160, 210), 0.32)
    t0 = SCENE_T["follow"][0]
    S.put(a, C.stand("happy", "wave", wave=int(t * 4) % 2, bob=int(t * 3) % 2), 112, 430, k=3)
    clicked = t >= E.CLICK_T
    bx, by, bw, bh = 196, 268, 132, 44
    squash = 2 if 0 <= t - E.CLICK_T < 0.12 else 0
    m = mask_rrect(bx, by + squash, bw, bh - squash, 10)
    paint(a, m, (120, 120, 130) if clicked else (236, 52, 80))
    paint(a, m & (np.arange(H)[:, None] < by + 6 + squash), (150, 150, 160) if clicked else (255, 110, 130))
    text(a, "已关注" if clicked else "+ 关注", bx + bw / 2 + (12 if clicked else 0), by + 8 + squash,
         (255, 255, 255), scale=2, align="center")
    if clicked:
        S.check(a, bx + 12, by + 14 + squash, 2, (255, 255, 255))
    if clicked:
        d = t - E.CLICK_T
        for j in range(10):
            ang = j / 10 * 6.283
            r = 20 + d * 90
            if d < 1.0:
                S.sparkle(a, int(bx + bw / 2 + np.cos(ang) * r * 1.4), int(by + bh / 2 + np.sin(ang) * r), 2,
                          (255, 220, 140))
    # hand cursor flies in and taps
    u = smooth((t - (E.CLICK_T - 0.7)) / 0.6)
    hx = lerp(330, bx + bw / 2 + 6, u)
    hy = lerp(420, by + bh / 2, u) + (3 if 0 <= t - E.CLICK_T < 0.12 else 0)
    if t > t0 + 0.2:
        blit(a, scale_sprite(HAND, 3), hx, hy)
    q = pop(t, t0 + 0.1)
    S.label(a, "下一期 · 敬请期待", 262, 196 + int((1 - q) * 10), "gold", color=(252, 214, 120))
    S.vignette(a, 0.8)
    return a
