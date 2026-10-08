"""Soundtrack: voice-over + soft chiptune bed (ducked under the voice) + SFX.

    python audio.py build/audio.wav
"""
import os
import subprocess
import sys
import wave

import numpy as np

import events as E
from timeline import LT, DUR, SCENES, SCENE_T, L

SR = 44100
HERE = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(1)


def mtof(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def env(n, a=0.005, d=0.05, s=0.6, r=0.05):
    t = np.arange(n) / SR
    dur = n / SR
    e = np.ones(n)
    e = np.where(t < a, t / max(a, 1e-6), e)
    e = np.where((t >= a) & (t < a + d), 1 - (1 - s) * (t - a) / max(d, 1e-6), e)
    e = np.where(t >= a + d, s, e)
    rel = dur - r
    e = np.where(t > rel, e * np.clip((dur - t) / max(r, 1e-6), 0, 1), e)
    return e


def osc(freq, dur, wave="sine", duty=0.5, slide=0.0):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = freq * (1 + slide * t / max(dur, 1e-6)) if slide else np.full(n, freq)
    ph = np.cumsum(f) / SR
    if wave == "sine":
        return np.sin(2 * np.pi * ph)
    if wave == "tri":
        return 2 * np.abs(2 * (ph % 1) - 1) - 1
    if wave == "square":
        return np.where((ph % 1) < duty, 1.0, -1.0)
    if wave == "saw":
        return 2 * (ph % 1) - 1
    raise ValueError(wave)


def soften(x, k=6):
    return np.convolve(x, np.ones(k) / k, "same")


def noise(dur):
    return rng.uniform(-1, 1, int(dur * SR))


def place(buf, t, sig, vol=1.0):
    i = int(t * SR)
    if i >= len(buf) or i + len(sig) <= 0:
        return
    j0 = max(0, -i)
    j1 = min(len(sig), len(buf) - i)
    buf[i + j0:i + j1] += sig[j0:j1] * vol


# -------------------------------------------------------------------- sfx
def s_tick(v=1.0):
    n = noise(0.012)
    return (n - soften(n, 4)) * np.exp(-np.arange(len(n)) / SR * 300) * v


def s_blip(f=1200, dur=0.06, duty=0.25):
    return soften(osc(f, dur, "square", duty), 3) * env(int(dur * SR), 0.002, 0.02, 0.5, 0.02) * 0.5


def s_pop():
    return osc(320, 0.08, "sine", slide=2.2) * env(int(0.08 * SR), 0.002, 0.03, 0.4, 0.03)


def s_whoosh(dur=0.4, v=1.0):
    n = noise(dur)
    n = soften(n, 3) - soften(n, 30)
    t = np.arange(len(n)) / len(n)
    return n * np.sin(np.pi * t) ** 2 * 1.4 * v


def s_ding(f=1318.5, dur=0.6, v=1.0):
    t = np.arange(int(dur * SR)) / SR
    x = osc(f, dur) + 0.4 * osc(f * 2.01, dur) + 0.15 * osc(f * 3.0, dur)
    return x * np.exp(-t * 7) * 0.45 * v


def s_chime(notes=(84, 88, 91, 96), gap=0.07, v=1.0):
    out = np.zeros(int((gap * len(notes) + 0.7) * SR))
    for k, m in enumerate(notes):
        place(out, k * gap, s_ding(mtof(m), 0.6), 0.7 * v)
    return out


def s_buzz():
    x = osc(110, 0.32, "square", 0.5) + osc(116, 0.32, "square", 0.5)
    return soften(x, 8) * env(int(0.32 * SR), 0.005, 0.1, 0.7, 0.08) * 0.28


def s_coin():
    out = np.zeros(int(0.35 * SR))
    place(out, 0, soften(osc(987.8, 0.07, "square", 0.5), 3) * 0.25)
    place(out, 0.07, soften(osc(1318.5, 0.25, "square", 0.5), 3) * env(int(0.25 * SR), 0.002, 0.2, 0.0, 0.05) * 0.25)
    return out


def s_fanfare():
    out = np.zeros(int(1.2 * SR))
    for k, m in enumerate((72, 76, 79, 84)):
        d = 0.09 if k < 3 else 0.7
        sig = soften(osc(mtof(m), d, "square", 0.25), 4) * env(int(d * SR), 0.003, 0.05, 0.6, 0.15) * 0.25
        place(out, k * 0.09, sig)
        place(out, k * 0.09, soften(osc(mtof(m - 12), d, "tri"), 2) * env(int(d * SR), 0.003, 0.05, 0.6, 0.15) * 0.2)
    return out


def s_clunk():
    t = np.arange(int(0.15 * SR)) / SR
    return (osc(140, 0.15, "sine", slide=-0.5) * 0.7 + soften(noise(0.15), 6) * 0.3) * np.exp(-t * 30) * 0.8


def s_thump(f=55):
    t = np.arange(int(0.25 * SR)) / SR
    return osc(f, 0.25, "sine", slide=-0.4) * np.exp(-t * 16)


def s_heartbeat():
    out = np.zeros(int(0.5 * SR))
    place(out, 0, s_thump(58), 0.9)
    place(out, 0.16, s_thump(50), 0.7)
    return out


def s_ping():
    out = np.zeros(int(0.25 * SR))
    for k, f in enumerate((880, 1318.5)):
        d = 0.09
        place(out, k * 0.08, osc(f, d) * env(int(d * SR), 0.002, 0.03, 0.5, 0.04) * 0.4)
    return out


def s_hit():
    n = noise(0.25)
    t = np.arange(len(n)) / SR
    x = soften(n, 3) * np.exp(-t * 18) * 0.5 + soften(osc(400, 0.25, "square", 0.5, slide=-0.8), 4) * np.exp(-t * 10) * 0.3
    return x


def s_chirp():
    out = np.zeros(int(0.4 * SR))
    for k in range(3):
        d = 0.05
        place(out, k * 0.09, osc(2600 + k * 300, d, "sine", slide=0.5) * env(int(d * SR), 0.003, 0.02, 0.4, 0.02) * 0.18)
    return out


def s_step():
    n = soften(noise(0.05), 20)
    return n * np.exp(-np.arange(len(n)) / SR * 80) * 1.2


def s_ratchet(dur=0.3):
    out = np.zeros(int(dur * SR) + 2000)
    for k in range(int(dur / 0.03)):
        place(out, k * 0.03, s_tick(0.8))
    return out


def s_rise(dur=0.5, f0=400, f1=1600):
    x = soften(osc(f0, dur, "square", 0.25, slide=(f1 / f0 - 1)), 4)
    return x * env(int(dur * SR), 0.01, 0.1, 0.6, 0.1) * 0.18


def s_fall(dur=0.5, f0=900, f1=200):
    x = soften(osc(f0, dur, "square", 0.25, slide=(f1 / f0 - 1)), 4)
    return x * env(int(dur * SR), 0.01, 0.1, 0.6, 0.1) * 0.18


def sfx_track():
    b = np.zeros(int((DUR + 2) * SR))
    # intro
    place(b, 0.1, s_whoosh(0.35), 0.5)
    place(b, E.INTRO_POP[0], s_thump(70), 0.8)
    place(b, E.INTRO_POP[1], s_pop(), 0.6)
    for t in E.INTRO_POP[2:]:
        place(b, t, s_blip(1500, 0.05), 0.5)
    t = E.COUNT[0]
    while t < E.COUNT[1]:
        place(b, t, s_tick(0.6), 0.6)
        t += 0.05
    place(b, E.COUNT[1], s_ding(1760), 0.5)
    # scene changes
    for n, s, e in SCENES[1:]:
        place(b, s - 0.2, s_whoosh(0.4), 0.25)
    # bedroom
    for t in E.FEED:
        if t < E.BRAIN_CUT:
            place(b, t, s_tick(0.5), 0.35)
    place(b, E.BUBBLE_T, s_pop(), 0.6)
    t = E.CLOCK_FF[0]
    while t < E.CLOCK_FF[1]:
        place(b, t, s_tick(1.0), 0.45)
        t += 0.09
    place(b, E.PLUS1H_T, s_ding(1046.5), 0.5)
    place(b, E.ZOOM[0], s_whoosh(1.0), 0.45)
    place(b, E.BRAIN_CUT, s_chime((72, 79, 84), 0.08), 0.35)
    for t in E.BURSTS:
        place(b, t + 0.4, s_rise(0.35, 600, 1800), 0.5)
    place(b, E.DOPA_LABEL_T, s_ding(1568), 0.45)
    # molecule
    place(b, E.HAPPY_CARD_T, s_pop(), 0.6)
    place(b, E.STRIKE_T, s_buzz(), 0.7)
    place(b, E.WANT_CARD_T, s_chime(), 0.55)
    # want / like
    place(b, E.SATISFY_T, s_blip(500, 0.08), 0.5)
    for k in range(10):
        place(b, E.WANT_T + k * 0.045, s_blip(500 + k * 90, 0.04), 0.4)
    place(b, E.WANT_T + 0.5, s_coin(), 0.5)
    # carrot steps
    c0, c1 = SCENE_T["carrot"]
    t = c0
    while t < c1:
        place(b, t, s_step(), 0.5)
        t += 0.2
    # skinner
    for t in E.FIXED_PRESSES + E.RANDOM_PRESSES:
        place(b, t, s_clunk(), 0.45)
    for t in E.FIXED_PRESSES + E.RANDOM_REWARDS:
        place(b, t + 0.35, s_ding(1975.5, 0.3), 0.35)
    # slot
    for k, p in enumerate(E.PULLS):
        if p > DUR:
            continue
        place(b, p, s_ratchet(0.25), 0.5)
        stop = min(E.STOPS[k][2], SCENE_T["slot"][1])
        t = p + 0.1
        while t < stop:
            place(b, t, s_tick(0.7), 0.3)
            t += 0.05
        for st in E.STOPS[k]:
            if st < SCENE_T["slot"][1]:
                place(b, st, s_clunk(), 0.6)
    place(b, E.NEAR_MISS_T + 0.1, s_fall(0.45, 500, 300), 0.6)
    place(b, E.JACKPOT_T, s_fanfare(), 0.6)
    for k in range(8):
        place(b, E.JACKPOT_T + 0.1 + k * 0.09, s_coin(), 0.3)
    # graph
    from scenes_b import SPIKES
    g0, g1 = E.GRAPH_DRAW
    for sx in SPIKES:
        place(b, g0 + (sx - 40) / 290 * (g1 - g0), s_blip(880, 0.05), 0.35)
    for k, t in enumerate(E.VOLUME_STEPS):
        place(b, t, s_blip(700 - k * 70, 0.06, 0.5), 0.45)
    for t in E.GREY_T:
        place(b, t - 0.15, s_pop(), 0.5)
    place(b, E.DULL_T, s_fall(0.6, 300, 120), 0.6)
    # cage
    c0, c1 = SCENE_T["cage"]
    t = c0 + 0.1
    while t < c1 - 0.2:
        place(b, t, s_heartbeat(), 0.8)
        t += 0.85
    for t in E.PINGS:
        place(b, t, s_ping(), 0.35)
    place(b, E.Q_T, s_ding(1046.5, 0.8), 0.5)
    # unlock
    place(b, E.UNLOCK_T, s_clunk(), 0.6)
    place(b, E.UNLOCK_T + 0.08, s_chime((79, 84, 88, 91)), 0.6)
    # skills
    place(b, E.CHEST_T + 0.3, s_chime((84, 91, 96), 0.06), 0.45)
    for j in range(3):
        place(b, E.CARDS_T + j * 0.18, s_pop(), 0.5)
    for t in E.SKILL_T:
        place(b, t, s_whoosh(0.3), 0.4)
        place(b, t + 0.25, s_ding(1568), 0.45)
    for t in E.SKILL_HIT:
        place(b, t, s_hit(), 0.6)
    place(b, E.BOSS_DOWN_T, s_fanfare(), 0.55)
    # sunrise birds
    s0, s1 = SCENE_T["sunrise"]
    for k in range(6):
        place(b, s0 + 0.4 + k * 0.9 + rng.random() * 0.3, s_chirp(), 0.6)
    # follow
    place(b, E.CLICK_T, s_tick(1.0), 0.8)
    place(b, E.CLICK_T + 0.02, s_chime((84, 88, 91, 96), 0.05), 0.5)
    return b


# ------------------------------------------------------------------ music
BEAT = 60 / 84.0


def _chord_pad(buf, t0, dur, notes, vol):
    for m in notes:
        n = int(dur * SR)
        x = osc(mtof(m), dur, "tri") * 0.6 + osc(mtof(m) * 1.003, dur, "sine") * 0.4
        place(buf, t0, x * env(n, 0.25, 0.3, 0.8, 0.4), vol)


def music_track():
    b = np.zeros(int((DUR + 2) * SR))
    secs = [
        (0.0, SCENE_T["molecule"][0], [[57, 60, 64, 67], [53, 57, 60, 64], [48, 52, 55, 59], [55, 59, 62, 65]], 1),
        (SCENE_T["molecule"][0], SCENE_T["skinner"][0], [[57, 60, 64, 67], [53, 57, 60, 64], [55, 59, 62, 65], [52, 56, 59, 62]], 2),
        (SCENE_T["skinner"][0], SCENE_T["cage"][0], [[50, 53, 57, 60], [57, 60, 64, 67], [52, 56, 59, 62], [57, 60, 64, 67]], 2),
        (SCENE_T["cage"][0], SCENE_T["unlock"][0], [[45, 52, 57, 60], [44, 51, 56, 59]], 0),
        (SCENE_T["unlock"][0], DUR, [[48, 52, 55, 59], [55, 59, 62, 66], [57, 60, 64, 67], [53, 57, 60, 64]], 2),
    ]
    for s0, s1, chords, energy in secs:
        bar = BEAT * 4
        t = s0
        k = 0
        while t < s1 - 0.05:
            ch = chords[k % len(chords)]
            d = min(bar, s1 - t)
            _chord_pad(b, t, d + 0.3, ch, 0.05 if energy else 0.07)
            # bass
            root = ch[0] - 12
            for beat in (0, 2):
                if t + beat * BEAT < s1:
                    bd = BEAT * 1.6
                    place(b, t + beat * BEAT, osc(mtof(root), bd, "sine") * env(int(bd * SR), 0.01, 0.2, 0.6, 0.2), 0.16)
            if energy >= 1:
                # soft arpeggio (8ths)
                arp = ch + [ch[1] + 12]
                for j in range(8):
                    tt = t + j * BEAT / 2
                    if tt >= s1:
                        break
                    m = arp[j % len(arp)] + 12
                    x = soften(osc(mtof(m), 0.18, "square", 0.25), 10) * env(int(0.18 * SR), 0.004, 0.08, 0.3, 0.06)
                    place(b, tt, x, 0.035 if energy == 1 else 0.045)
            if energy >= 2:
                for beat in range(4):
                    tt = t + beat * BEAT
                    if tt >= s1:
                        break
                    if beat in (0, 2):
                        place(b, tt, s_thump(60), 0.22)
                    place(b, tt + BEAT / 2, s_tick(0.6), 0.12)
            t += bar
            k += 1
    # end on a held C major chord
    _chord_pad(b, DUR - 2.4, 2.6, [48, 55, 60, 64, 67], 0.06)
    return b


def load_vo(i):
    path = os.path.join(HERE, "build", "vo", "%02d.wav" % i)
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ar", str(SR), "-ac", "1", "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).astype(np.float64)


def main(out):
    n = int((DUR + 0.5) * SR)
    vo = np.zeros(n + SR)
    for i, (s, e) in enumerate(LT):
        place(vo, s, load_vo(i), 1.0)
    mus = music_track()[:len(vo)]
    sfx = sfx_track()[:len(vo)]
    # duck the music under the voice
    envv = np.convolve(np.abs(vo), np.ones(2205) / 2205, "same")
    act = (envv > 0.02).astype(float)
    act = np.convolve(act, np.ones(int(0.25 * SR)) / int(0.25 * SR), "same")
    duck = 1 - 0.45 * np.clip(act * 1.5, 0, 1)
    mix = vo * 1.0 + mus * duck * 1.0 + sfx * 0.55
    fade = np.clip((DUR - np.arange(len(mix)) / SR) / 0.6, 0, 1)
    mix *= fade
    mix = np.tanh(mix * 1.1) / np.tanh(1.1)
    mix = mix[:int(DUR * SR)]
    pcm = (np.clip(mix, -1, 1) * 32000).astype(np.int16)
    st = np.stack([pcm, pcm], 1)
    with wave.open(out, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(st.tobytes())
    print("wrote", out, "%.2fs" % (len(pcm) / SR))


if __name__ == "__main__":
    main(sys.argv[1])
