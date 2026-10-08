"""Chunky big-head protagonist (drawn at 'art' resolution, blitted at 2x-4x)."""
from functools import lru_cache

import numpy as np

from engine import new, rect, pset, disc, thick, outlined, hline, vline

OUT = (40, 24, 32)
HAIR, HAIR_HI, HAIR_DK = (58, 42, 52), (98, 72, 80), (40, 28, 36)
SKIN, SKIN_SH, SKIN_HI = (248, 202, 162), (222, 158, 120), (255, 226, 196)
WHITE, PUPIL = (250, 248, 244), (32, 22, 30)
BLUSH, BROW, MOUTH, TONGUE = (240, 136, 126), (52, 34, 40), (104, 36, 44), (214, 84, 92)
HOOD, HOOD_SH, HOOD_HI = (46, 128, 146), (30, 90, 110), (88, 178, 186)
PANTS, PANTS_SH = (52, 54, 96), (36, 36, 70)
SHOE, SHOE_SH = (236, 234, 240), (168, 164, 186)
CYAN = (140, 236, 255)


def _head_base():
    s = new(alpha=True, w=16, h=16)
    # skull
    rect(s, 2, 1, 12, 14, SKIN)
    rect(s, 1, 3, 14, 10, SKIN)
    rect(s, 3, 0, 10, 1, HAIR)
    # hair cap + messy fringe
    rect(s, 1, 1, 14, 5, HAIR)
    rect(s, 2, 0, 12, 2, HAIR)
    rect(s, 0, 3, 2, 6, HAIR)
    rect(s, 14, 3, 2, 6, HAIR)
    for x, h in ((2, 2), (4, 1), (5, 2), (8, 1), (9, 2), (12, 1), (13, 2)):
        rect(s, x, 6, 1, h, HAIR)
    rect(s, 5, 1, 4, 1, HAIR_HI)
    rect(s, 4, 2, 2, 1, HAIR_HI)
    pset(s, 10, 2, HAIR_HI)
    rect(s, 1, 6, 1, 3, HAIR_DK)
    rect(s, 14, 6, 1, 3, HAIR_DK)
    # ears
    rect(s, 0, 9, 1, 3, SKIN_SH)
    rect(s, 15, 9, 1, 3, SKIN_SH)
    # jaw shade
    hline(s, 3, 12, 14, SKIN_SH)
    pset(s, 2, 13, SKIN_SH)
    pset(s, 13, 13, SKIN_SH)
    # nose
    pset(s, 8, 11, SKIN_SH)
    return s


@lru_cache(maxsize=None)
def head(expr="normal"):
    s = _head_base()
    L, R = 4, 10  # left edge of each eye (2px wide)
    if expr in ("normal", "excited", "glow", "sad", "tired", "worried"):
        if expr == "tired":
            for x in (L, R):
                rect(s, x, 9, 2, 1, SKIN_SH)
                rect(s, x, 10, 2, 1, PUPIL)
                rect(s, x, 11, 2, 1, (210, 150, 150))
        else:
            for x, inner in ((L, L + 1), (R, R + 1)):
                rect(s, x, 9, 2, 2, WHITE)
                rect(s, inner, 9, 1, 2, CYAN if expr == "glow" else PUPIL)
            if expr == "excited":
                pset(s, L + 1, 9, WHITE)
                pset(s, R + 1, 9, WHITE)
    elif expr in ("closed", "happy"):
        for x in (L, R):
            if expr == "happy":
                pset(s, x, 10, PUPIL)
                pset(s, x + 1, 9, PUPIL)
                pset(s, x + 2, 10, PUPIL)
            else:
                rect(s, x, 10, 3, 1, PUPIL)
    # brows
    if expr == "sad" or expr == "worried":
        pset(s, L, 8, BROW); pset(s, L + 1, 7, BROW); pset(s, L + 2, 7, BROW)
        pset(s, R + 1, 8, BROW); pset(s, R, 7, BROW); pset(s, R - 1, 7, BROW)
    elif expr == "excited":
        rect(s, L - 1, 7, 3, 1, BROW)
        rect(s, R, 7, 3, 1, BROW)
    elif expr != "tired":
        rect(s, L - 1, 8, 3, 1, BROW)
        rect(s, R, 8, 3, 1, BROW)
    # cheeks
    if expr not in ("tired", "sad"):
        pset(s, 2, 12, BLUSH)
        pset(s, 13, 12, BLUSH)
    # mouth
    if expr in ("excited", "happy"):
        rect(s, 6, 12, 4, 2, MOUTH)
        rect(s, 7, 13, 2, 1, TONGUE)
        hline(s, 6, 9, 12, (250, 240, 236))
    elif expr == "sad" or expr == "worried":
        rect(s, 6, 13, 4, 1, MOUTH)
        pset(s, 5, 14, MOUTH)
        pset(s, 10, 14, MOUTH)
    elif expr == "tired":
        rect(s, 6, 13, 4, 1, MOUTH)
    else:
        rect(s, 6, 13, 4, 1, MOUTH)
        pset(s, 10, 12, MOUTH)
    return s


def _body_front(s, ox, oy, arms="down", wave=0):
    """Hoodie body under a 16px head placed at (ox, oy)."""
    by = oy + 15
    rect(s, ox + 2, by, 12, 9, HOOD)
    rect(s, ox + 2, by, 2, 9, HOOD_SH)
    rect(s, ox + 12, by, 2, 9, HOOD_SH)
    rect(s, ox + 5, by, 6, 1, HOOD_SH)  # collar
    vline(s, ox + 6, by + 1, by + 4, (230, 230, 236))  # strings
    vline(s, ox + 9, by + 1, by + 4, (230, 230, 236))
    rect(s, ox + 5, by + 6, 6, 2, HOOD_SH)  # pocket
    rect(s, ox + 3, by + 1, 1, 6, HOOD_HI)
    # arms
    if arms == "down":
        rect(s, ox, by + 1, 2, 7, HOOD)
        rect(s, ox + 14, by + 1, 2, 7, HOOD_SH)
        rect(s, ox, by + 8, 2, 2, SKIN)
        rect(s, ox + 14, by + 8, 2, 2, SKIN_SH)
    elif arms == "wave":
        rect(s, ox, by + 1, 2, 7, HOOD)
        rect(s, ox, by + 8, 2, 2, SKIN)
        ang = [-0.4, 0.15][wave % 2]
        x0, y0 = ox + 15, by + 2
        x1, y1 = x0 + 3 + ang * 4, y0 - 6
        thick(s, x0, y0, x1, y1, 1.0, HOOD_SH)
        disc(s, x1, y1 - 1, 1.2, SKIN)
    elif arms == "phone":  # both hands holding a phone at chest height
        rect(s, ox, by + 1, 2, 5, HOOD)
        rect(s, ox + 14, by + 1, 2, 5, HOOD_SH)
        rect(s, ox + 2, by + 5, 3, 2, HOOD)
        rect(s, ox + 11, by + 5, 3, 2, HOOD_SH)
        rect(s, ox + 5, by + 3, 6, 5, (30, 30, 42))
        rect(s, ox + 6, by + 4, 4, 3, CYAN)
        rect(s, ox + 4, by + 6, 2, 2, SKIN)
        rect(s, ox + 10, by + 6, 2, 2, SKIN)
    # legs
    ly = by + 9
    rect(s, ox + 3, ly, 4, 4, PANTS)
    rect(s, ox + 9, ly, 4, 4, PANTS_SH)
    rect(s, ox + 7, ly, 2, 1, PANTS_SH)
    rect(s, ox + 2, ly + 4, 5, 2, SHOE)
    rect(s, ox + 9, ly + 4, 5, 2, SHOE)
    hline(s, ox + 2, ox + 6, ly + 5, SHOE_SH)
    hline(s, ox + 9, ox + 13, ly + 5, SHOE_SH)


@lru_cache(maxsize=None)
def stand(expr="normal", arms="down", wave=0, bob=0):
    s = new(alpha=True, w=22, h=34)
    _body_front(s, 3, 3 + bob, arms, wave)
    hd = head(expr)
    m = hd[..., 3] > 0
    s[3 + bob - 1 + 0:3 + bob - 1 + 16, 3:19][m] = hd[m]
    return outlined(s, OUT)


@lru_cache(maxsize=None)
def portrait(expr="tired"):
    """Head + shoulders for the intro card."""
    s = new(alpha=True, w=24, h=24)
    rect(s, 1, 17, 22, 7, HOOD)
    rect(s, 1, 17, 3, 7, HOOD_SH)
    rect(s, 20, 17, 3, 7, HOOD_SH)
    rect(s, 8, 17, 8, 2, HOOD_SH)
    vline(s, 9, 19, 23, (230, 230, 236))
    vline(s, 14, 19, 23, (230, 230, 236))
    rect(s, 2, 15, 4, 3, HOOD_SH)  # hood behind neck
    rect(s, 18, 15, 4, 3, HOOD_SH)
    hd = head(expr)
    m = hd[..., 3] > 0
    s[2:18, 4:20][m] = hd[m]
    return outlined(s, OUT)


@lru_cache(maxsize=None)
def sit_phone(expr="glow", frame=0):
    """Sitting, hugging knees, phone in hands (front view)."""
    s = new(alpha=True, w=22, h=30)
    ox, oy = 3, 2
    by = oy + 15
    rect(s, ox + 1, by, 14, 8, HOOD)
    rect(s, ox + 1, by, 2, 8, HOOD_SH)
    rect(s, ox + 13, by, 2, 8, HOOD_SH)
    # knees up front
    rect(s, ox + 2, by + 2, 5, 9, PANTS)
    rect(s, ox + 9, by + 2, 5, 9, PANTS_SH)
    rect(s, ox + 2, by + 2, 5, 1, (80, 82, 130))
    rect(s, ox + 9, by + 2, 5, 1, (66, 68, 112))
    rect(s, ox + 1, by + 10, 6, 2, SHOE)
    rect(s, ox + 9, by + 10, 6, 2, SHOE)
    # arms + phone
    rect(s, ox, by + 1, 2, 6, HOOD)
    rect(s, ox + 14, by + 1, 2, 6, HOOD_SH)
    rect(s, ox + 1, by + 5, 4, 2, HOOD)
    rect(s, ox + 11, by + 5, 4, 2, HOOD_SH)
    rect(s, ox + 5, by + 2, 6, 5, (30, 30, 42))
    rect(s, ox + 6, by + 3, 4, 3, CYAN if frame % 2 == 0 else (255, 150, 200))
    rect(s, ox + 4, by + 5, 2, 2, SKIN)
    rect(s, ox + 10, by + 5, 2, 2, SKIN)
    hd = head(expr)
    m = hd[..., 3] > 0
    s[oy:oy + 16, ox:ox + 16][m] = hd[m]
    return outlined(s, OUT)


@lru_cache(maxsize=None)
def sit_back():
    """Back view, sitting (sunrise)."""
    s = new(alpha=True, w=20, h=26)
    rect(s, 2, 1, 16, 12, HAIR)
    rect(s, 3, 0, 14, 2, HAIR)
    rect(s, 1, 3, 18, 8, HAIR)
    rect(s, 5, 1, 5, 1, HAIR_HI)
    rect(s, 4, 2, 3, 2, HAIR_HI)
    rect(s, 0, 6, 1, 3, SKIN_SH)
    rect(s, 19, 6, 1, 3, SKIN_SH)
    rect(s, 3, 12, 14, 9, HOOD)
    rect(s, 5, 12, 10, 3, HOOD_SH)  # hood
    rect(s, 3, 12, 2, 9, HOOD_SH)
    rect(s, 15, 12, 2, 9, HOOD_SH)
    rect(s, 1, 20, 18, 4, PANTS)
    rect(s, 1, 23, 18, 1, PANTS_SH)
    return outlined(s, OUT)


@lru_cache(maxsize=None)
def head_side(expr="excited"):
    """Profile head facing right."""
    s = new(alpha=True, w=17, h=16)
    rect(s, 2, 1, 12, 14, SKIN)
    rect(s, 1, 3, 14, 10, SKIN)
    rect(s, 14, 8, 2, 4, SKIN)
    pset(s, 16, 10, SKIN)  # nose
    pset(s, 15, 11, SKIN_SH)
    # hair: cap + back of head
    rect(s, 2, 0, 12, 2, HAIR)
    rect(s, 1, 1, 14, 5, HAIR)
    rect(s, 0, 3, 7, 9, HAIR)
    rect(s, 1, 12, 4, 1, HAIR)
    for x, h in ((9, 2), (11, 1), (12, 2), (14, 1)):
        rect(s, x, 6, 1, h, HAIR)
    rect(s, 4, 1, 5, 1, HAIR_HI)
    rect(s, 3, 2, 2, 1, HAIR_HI)
    rect(s, 1, 6, 1, 4, HAIR_DK)
    # ear
    rect(s, 6, 8, 2, 3, SKIN_SH)
    pset(s, 7, 9, (190, 120, 100))
    # face
    hline(s, 3, 13, 14, SKIN_SH)
    rect(s, 11, 7, 3, 1, BROW)
    if expr == "closed":
        rect(s, 11, 9, 3, 1, PUPIL)
    else:
        rect(s, 12, 8, 2, 2, WHITE)
        rect(s, 13, 8, 1, 2, PUPIL)
        if expr == "excited":
            pset(s, 13, 8, WHITE)
            rect(s, 13, 9, 1, 1, PUPIL)
    pset(s, 11, 11, BLUSH)
    if expr in ("excited", "happy"):
        rect(s, 12, 12, 3, 2, MOUTH)
        pset(s, 13, 13, TONGUE)
    else:
        rect(s, 12, 13, 3, 1, MOUTH)
    return s


@lru_cache(maxsize=None)
def run_side(frame):
    """4-frame side-view run cycle, facing right."""
    s = new(alpha=True, w=26, h=34)
    bob = (0, 1, 0, 1)[frame % 4]
    ox, oy = 4, 2 + bob
    # legs (back then front)
    legs = [((-3, 2), (3, -1)), ((0, 0), (0, 0)), ((3, -1), (-3, 2)), ((0, 0), (0, 0))][frame % 4]
    by = oy + 24
    for i, (dx, lift) in enumerate(legs):
        c = PANTS_SH if i == 0 else PANTS
        x = ox + 6 + dx
        rect(s, x, by, 3, 5 - max(0, lift), c)
        rect(s, x - (0 if dx >= 0 else 1), by + 5 - max(0, lift), 4, 2, SHOE_SH if i == 0 else SHOE)
    # body
    rect(s, ox + 3, oy + 15, 10, 9, HOOD)
    rect(s, ox + 3, oy + 15, 3, 9, HOOD_SH)
    rect(s, ox + 1, oy + 14, 4, 4, HOOD_SH)  # hood bump on back
    # arms swing
    sw = (3, 0, -3, 0)[frame % 4]
    thick(s, ox + 8, oy + 17, ox + 8 + sw, oy + 22, 1.0, HOOD_SH)
    thick(s, ox + 9, oy + 17, ox + 9 - sw, oy + 22, 1.0, HOOD)
    disc(s, ox + 9 - sw, oy + 23, 1.0, SKIN)
    # head (profile-ish: shift the front head, add nose)
    hd = head_side("excited")
    m = hd[..., 3] > 0
    s[oy:oy + 16, ox + 1:ox + 18][m] = hd[m]
    return outlined(s, OUT)


@lru_cache(maxsize=None)
def rat(frame=0, mood="idle"):
    """Lab rat, side view facing left. frame 0 = on all fours, 1 = up on lever."""
    W_, G, G2, P, E = (236, 234, 240), (190, 186, 200), (150, 146, 166), (244, 160, 176), (200, 30, 50)
    s = new(alpha=True, w=26, h=18)
    if frame == 0:
        rect(s, 6, 7, 14, 7, W_)
        rect(s, 8, 6, 10, 1, W_)
        rect(s, 6, 12, 14, 2, G)
        rect(s, 2, 8, 6, 5, W_)
        rect(s, 1, 10, 2, 2, W_)
        pset(s, 0, 11, P)
        pset(s, 4, 9, E)
        rect(s, 5, 6, 2, 2, P)
        rect(s, 5, 5, 2, 1, G)
        rect(s, 7, 14, 2, 1, P)
        rect(s, 16, 14, 2, 1, P)
        tail = [(20, 12), (21, 13), (22, 13), (23, 14), (24, 14), (25, 15)]
    else:
        rect(s, 8, 4, 8, 10, W_)
        rect(s, 9, 3, 6, 1, W_)
        rect(s, 8, 11, 8, 3, G)
        rect(s, 4, 1, 6, 5, W_)
        rect(s, 3, 3, 2, 2, W_)
        pset(s, 2, 4, P)
        pset(s, 6, 2, E)
        rect(s, 7, 0, 2, 2, P)
        rect(s, 3, 7, 4, 1, P)  # paws pushing the lever
        rect(s, 9, 14, 2, 1, P)
        rect(s, 14, 14, 2, 1, P)
        tail = [(16, 12), (17, 13), (18, 13), (19, 14), (20, 14), (21, 15)]
    for x, y in tail:
        pset(s, x, y, P)
    return outlined(s, (60, 50, 70))
