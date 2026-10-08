"""Timing derived from the generated voice-over (build/vo/timing.json)."""
import json
import os

from script import LINES, LEAD_IN, CHAPTERS

HERE = os.path.dirname(os.path.abspath(__file__))
_TIM = json.load(open(os.path.join(HERE, "build", "vo", "timing.json")))["lines"]

LT = []  # (start, end) of each spoken line
_t = LEAD_IN
for ln, tm in zip(LINES, _TIM):
    LT.append((_t, _t + tm["dur"]))
    _t += tm["dur"] + ln["pause"]
DUR = round(_t + 0.3, 2)


def L(i, frac=0.0):
    """Time at a fraction of line i (0 = start, 1 = end)."""
    s, e = LT[i]
    return s + (e - s) * frac


def char_t(i, k):
    """Approximate time the k-th spoken character of line i is heard."""
    from script import spoken
    n = len(spoken(LINES[i]["caption"]))
    return L(i, min(1.0, (k + 0.5) / n))


def word_t(i, word, end=False):
    from script import spoken
    s = spoken(LINES[i]["caption"])
    k = s.find(word)
    if k < 0:
        return L(i, 0.5)
    return char_t(i, k + (len(word) - 1 if end else 0))


# scenes: start slightly before their first line so the picture leads the voice
SCENES = []
for i, ln in enumerate(LINES):
    if not SCENES or SCENES[-1][0] != ln["scene"]:
        start = 0.0 if i == 0 else max(LT[i - 1][1] + 0.05, LT[i][0] - 0.3)
        if SCENES:
            SCENES[-1][2] = start
        SCENES.append([ln["scene"], start, DUR])
SCENES = [tuple(s) for s in SCENES]
SCENE_T = {n: (s, e) for n, s, e in SCENES}


def scene_at(t):
    for n, s, e in SCENES:
        if s <= t < e:
            return n
    return SCENES[-1][0]


def chapter_at(t):
    for i in range(len(LINES) - 1, -1, -1):
        if t >= LT[i][0] - 0.3:
            return LINES[i]["ch"]
    return 0


def caption_at(t):
    for i, (s, e) in enumerate(LT):
        nxt = LT[i + 1][0] if i + 1 < len(LT) else DUR
        if s - 0.05 <= t < min(nxt - 0.05, e + 0.45):
            return i, LINES[i]["caption"]
    return None, None
