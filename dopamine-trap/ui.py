"""Overlays in the reference style: chapter bar, BOSS bar, big pixel subtitles."""
import numpy as np

from engine import W, H, rect, hline, vline, text, smooth, lerp, clamp01, text_width
from script import CHAPTERS
from timeline import LT, DUR, L, chapter_at, caption_at, word_t
from style import panel, CREAM

SUB_FILL = (246, 238, 222)
SUB_HL = (238, 170, 54)
SUB_OUT = (24, 18, 22)


def chapter_bar(a, t):
    y0, h = 28, 20
    rect(a, 0, y0, W, h, (22, 22, 28))
    hline(a, 0, W - 1, y0 + h, (8, 8, 12))
    cur = chapter_at(t)
    seg = W / len(CHAPTERS)
    for i, name in enumerate(CHAPTERS):
        x0 = int(i * seg)
        if i == cur:
            rect(a, x0, y0, int(seg), h, (50, 50, 60))
        if i:
            vline(a, x0, y0 + 5, y0 + h - 5, (70, 70, 80))
        c = (250, 248, 240) if i == cur else (120, 120, 132)
        text(a, name, x0 + seg / 2, y0 + 3, c, align="center")
    text(a, "大脑说明书 · 多巴胺的陷阱", W - 8, y0 + h + 5, (104, 102, 116), align="right")


def boss_hp(t):
    hp = 100.0
    for i, after in ((18, 70), (19, 40), (20, 12)):
        hp = lerp(hp, after, smooth((t - L(i, 0.7)) / 0.5))
    hp = lerp(hp, 0, smooth((t - L(21, 0.1)) / 0.6))
    return hp


def boss_bar(a, t):
    t0, t1 = L(1) - 0.3, L(22, 0.0)
    if not (t0 <= t < t1):
        return
    slide = smooth((t - t0) / 0.35) * (1 - smooth((t - (t1 - 0.35)) / 0.35))
    x0 = int(lerp(-200, 8, slide))
    y0, w, h = 56, 182, 30
    rect(a, x0, y0, w, h, (26, 14, 16))
    panel(a, x0, y0, w, h, "boss", fill=(26, 14, 16))
    hp = boss_hp(t)
    dead = hp < 1
    text(a, "BOSS · 多巴胺陷阱", x0 + 7, y0 + 3, (226, 96, 80))
    text(a, "已击破" if dead else "%d/100" % round(hp), x0 + w - 7, y0 + 3,
         (120, 230, 140) if dead else (226, 140, 120), align="right")
    rect(a, x0 + 7, y0 + 20, w - 14, 5, (60, 24, 24))
    fw = int((w - 14) * hp / 100)
    hit = any(0 <= t - L(i, 0.7) < 0.25 for i in (18, 19, 20))
    rect(a, x0 + 7, y0 + 20, fw, 5, (255, 240, 220) if hit else (214, 58, 46))
    rect(a, x0 + 7, y0 + 20, fw, 1, (255, 140, 110))


def subtitle(a, t):
    i, cap = caption_at(t)
    if cap is None:
        return
    lines = cap.split("\n")
    lh = 30
    y = 470 - (len(lines) - 1) * lh // 2
    pop = smooth((t - (LT[i][0] - 0.05)) / 0.08)
    for k, ln in enumerate(lines):
        text(a, ln, W / 2, y + k * lh, SUB_FILL, scale=2, align="center", hl=SUB_HL,
             outline=SUB_OUT, shadow=(0, 0, 0), sh_off=1, alpha=0.4 + 0.6 * pop)


def overlays(a, t):
    boss_bar(a, t)
    chapter_bar(a, t)
    subtitle(a, t)
