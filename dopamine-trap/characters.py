"""Protagonist sprites: hand-drawn heads + procedurally posed bodies."""
from functools import lru_cache

import numpy as np

from engine import new, sprite, outlined, thick, disc, rect, pset, blit, scale2x

K = (26, 18, 38)
HAIR, HAIR_HI, HAIR_DK = (58, 44, 78), (100, 80, 134), (40, 30, 56)
SKIN, SKIN_SH, SKIN_DK = (250, 206, 172), (222, 160, 134), (178, 110, 102)
EYE = (30, 22, 48)
HOOD, HOOD_SH, HOOD_HI = (44, 134, 152), (30, 94, 118), (88, 186, 192)
PANTS, PANTS_SH = (52, 54, 100), (34, 34, 68)
SHOE, SHOE_SH = (238, 238, 248), (160, 160, 186)

CMAP = {
    "k": K, "h": HAIR, "H": HAIR_HI, "j": HAIR_DK,
    "s": SKIN, "S": SKIN_SH, "d": SKIN_DK, "e": EYE,
    "w": (246, 246, 255), "c": (130, 235, 255), "m": (190, 96, 100), "b": (246, 160, 160),
    "t": HOOD, "T": HOOD_SH, "u": HOOD_HI,
}

# Side profile, facing right.
PROFILE = [
    "....kkkkkk.....",
    "..kkhhhhhhkk...",
    ".khhhHHHhhhhk..",
    "khhhHHhhhhhhhk.",
    "khhhhhhhhhhhhk.",
    "khhjhhhhhhshhk.",
    "khhjhhhsssssshk",
    "khhjhhSsssssEsk",
    "khhhdSSsssssEsk",
    ".khhdSssssssssk",
    ".khhhSsssssskk.",
    "..kSSssssssmk..",
    "...kSSssssk....",
    "....kkkkkk.....",
]

# Front view (cage scene).
FRONT = [
    "....kkkkkkkk....",
    "..kkhhhhhhhhkk..",
    ".khhhHHHhhhhhhk.",
    "khhHHhhhhhhhhhhk",
    "khhhhhhhhhhhhhhk",
    "khhhhshhhhhshhhk",
    "khhssssshhsssshk",
    "khsssssssssssshk",
    "khSscwsssssscwSk",
    "khSscwsssssscwSk",
    ".kSssssssssssSk.",
    ".kSsbssssssbsSk.",
    "..kSssssssssSk..",
    "..kSSssmmssSSk..",
    "...kkSSssSSkk...",
    ".....kkkkkk.....",
]


def _variant(rows, eye):
    out = []
    for r in rows:
        if eye == "closed":
            r = r.replace("E", "s")
        elif eye == "glow":
            r = r.replace("E", "c")
        else:
            r = r.replace("E", "e")
        out.append(r)
    return out


@lru_cache(maxsize=None)
def head_profile(eye="open"):
    rows = _variant(PROFILE, eye)
    s = sprite(rows, CMAP)
    if eye == "closed":
        s[8, 11, :3] = K  # a closed-eye lash line
        s[8, 12, :3] = K
    return s


@lru_cache(maxsize=None)
def head_front():
    return sprite(FRONT, CMAP)


def _pt(o, ang, ln):
    """Point at angle `ang` (0 = straight down, +ve = forward/right)."""
    return o[0] + np.sin(ang) * ln, o[1] + np.cos(ang) * ln


def _dk(c, k=0.72):
    return tuple(int(v * k) for v in c)


@lru_cache(maxsize=256)
def runner(qphase, frames=16, happy=False):
    """Side-view running figure, returned as an outlined RGBA sprite (feet at bottom)."""
    ph = qphase / frames * 2 * np.pi
    s = new(alpha=True, w=48, h=60)
    bob = abs(np.sin(ph)) * 2.0
    hip = (22.0, 34.0 - bob)
    lean = 0.22
    neck = (hip[0] + np.sin(lean) * 14, hip[1] - np.cos(lean) * 14)

    def leg(p, back):
        th = 0.8 * np.sin(p)
        knee_flex = 0.25 + 1.45 * max(0.0, np.cos(p))
        knee = _pt(hip, th, 9)
        ankle = _pt(knee, th - knee_flex, 9)
        cp = _dk(PANTS) if back else PANTS
        cs = _dk(SHOE) if back else SHOE
        thick(s, *hip, *knee, 2.2, cp)
        thick(s, *knee, *ankle, 1.8, cp)
        toe = (ankle[0] + 4, ankle[1] + 0.5)
        thick(s, ankle[0] - 1, ankle[1], *toe, 1.3, cs)
        pset(s, ankle[0] - 1, ankle[1] + 1, _dk(SHOE_SH) if back else SHOE_SH)

    def arm(p, back):
        ua = -0.95 * np.sin(p)
        sh = (neck[0] - 1, neck[1] + 3)
        el = _pt(sh, ua, 7)
        hand = _pt(el, ua + 1.7, 6)
        c = _dk(HOOD) if back else HOOD
        thick(s, *sh, *el, 1.7, c)
        thick(s, *el, *hand, 1.5, c)
        disc(s, *hand, 1.4, _dk(SKIN) if back else SKIN)

    arm(ph + np.pi, True)
    leg(ph + np.pi, True)
    # torso (hoodie)
    thick(s, *hip, *neck, 4.6, HOOD)
    thick(s, hip[0] - 3, hip[1] - 2, neck[0] - 4, neck[1] + 2, 1.6, HOOD_SH)
    thick(s, hip[0] + 3, hip[1] - 3, neck[0] + 2.5, neck[1] + 3, 1.0, HOOD_HI)
    disc(s, neck[0] - 4, neck[1] + 1, 3.0, HOOD_SH)  # hood
    rect(s, hip[0] - 4, hip[1] - 1, 9, 3, PANTS_SH)
    leg(ph, False)
    hp = head_profile("open")
    blit(s, hp, neck[0] - 7, neck[1] - 13)
    if happy:
        s2 = s  # smile pixel
        pset(s2, neck[0] + 4, neck[1] - 2, (190, 96, 100))
    arm(ph, False)
    return outlined(s, K)


@lru_cache(maxsize=8)
def sitter_front(frame=0):
    """Hugging knees, holding a glowing phone (front view)."""
    s = new(alpha=True, w=40, h=46)
    # hood behind head
    disc(s, 20, 11, 9.5, HOOD_SH)
    # torso
    rect(s, 9, 18, 22, 18, HOOD)
    rect(s, 9, 18, 3, 18, HOOD_SH)
    rect(s, 28, 18, 3, 18, HOOD_SH)
    # knees
    disc(s, 14, 27, 6.2, PANTS)
    disc(s, 26, 27, 6.2, PANTS)
    rect(s, 8, 27, 24, 14, PANTS)
    disc(s, 13, 25, 2.0, (78, 80, 136))
    disc(s, 25, 25, 2.0, (78, 80, 136))
    rect(s, 8, 36, 24, 5, PANTS_SH)
    # shoes
    rect(s, 8, 40, 9, 4, SHOE)
    rect(s, 23, 40, 9, 4, SHOE)
    rect(s, 8, 43, 9, 1, SHOE_SH)
    rect(s, 23, 43, 9, 1, SHOE_SH)
    # arms wrapping the knees
    thick(s, 7, 20, 7, 31, 2.2, HOOD)
    thick(s, 33, 20, 33, 31, 2.2, HOOD)
    thick(s, 8, 31, 16, 33, 2.0, HOOD)
    thick(s, 32, 31, 24, 33, 2.0, HOOD)
    # hands + phone
    disc(s, 17, 31, 2.0, SKIN)
    disc(s, 23, 31, 2.0, SKIN)
    rect(s, 16, 26, 8, 5, (40, 40, 52))
    rect(s, 17, 27, 6, 3, (150, 240, 255) if frame % 2 == 0 else (255, 150, 200))
    blit(s, head_front(), 12, 3)
    return outlined(s, K)


@lru_cache(maxsize=4)
def sitter_back():
    """Back view silhouette sitting on a hill (ending)."""
    s = new(alpha=True, w=30, h=34)
    disc(s, 15, 8, 6.5, HAIR)
    disc(s, 13, 6, 2.0, HAIR_HI)
    rect(s, 6, 14, 18, 14, HOOD)
    disc(s, 15, 16, 7.5, HOOD)
    rect(s, 6, 14, 3, 14, HOOD_SH)
    rect(s, 4, 26, 22, 5, PANTS)
    rect(s, 4, 30, 22, 2, PANTS_SH)
    rect(s, 14, 15, 2, 9, HOOD_SH)
    return outlined(s, K)


@lru_cache(maxsize=None)
def head_profile_big(eye="open"):
    """28px profile head: Scale2x of the small one (without its outline) + hand details."""
    rows = [r.replace("k", ".") for r in _variant(PROFILE, "open")]
    s = scale2x(sprite(rows, CMAP))
    # redraw the eye/mouth area with finer detail
    ex, ey = 24, 14
    s[ey:ey + 4, ex:ex + 2, :3] = SKIN
    if eye == "closed":
        s[ey + 2, ex - 1:ex + 2, :3] = K
        s[ey + 3, ex - 2, :3] = K
    else:
        s[ey:ey + 4, ex:ex + 2, :3] = EYE
        s[ey, ex, :3] = (246, 246, 255) if eye == "open" else (130, 235, 255)
        s[ey + 1, ex, :3] = (130, 235, 255) if eye == "glow" else EYE
        s[ey + 4, ex - 1:ex + 2, :3] = SKIN_SH  # eye bag
        s[ey - 2, ex - 1:ex + 3, :3] = HAIR_DK  # brow
    s[ey + 9, ex - 1:ex + 2, :3] = (190, 96, 100)  # mouth
    s[ey + 6, 27, :3] = SKIN_SH  # nostril hint
    for y in range(15, 21):  # ear
        s[y, 9:12, :3] = SKIN_SH
    s[17, 10, :3] = SKIN_DK
    s[18, 10, :3] = SKIN_DK
    return outlined(s, K)
