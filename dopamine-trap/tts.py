"""Generate the voice-over with Kokoro v1.1-zh (sherpa-onnx, fully offline).

    python tts.py /path/to/kokoro-multi-lang-v1_1 [sid] [speed]

Writes build/vo/NN.wav (24 kHz mono) and build/vo/timing.json.
"""
import json
import os
import sys

import numpy as np
import sherpa_onnx
import soundfile as sf

from script import LINES, spoken

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "build", "vo")


# Pronunciation fixes for the stock lexicon (word -> phone tokens).
LEX_PATCH = {
    "分子": "ㄈ ㄣ 1 ㄗ ㄭ 3",  # molecule: fēnzǐ, not fènzǐ
}


def patched_lexicon(m):
    src = f"{m}/lexicon-zh.txt"
    dst = os.path.join(HERE, "build", "lexicon-zh-patched.txt")
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    with open(src, encoding="utf8") as f, open(dst, "w", encoding="utf8") as g:
        for line in f:
            w = line.split(" ", 1)[0]
            g.write(f"{w} {LEX_PATCH[w]}\n" if w in LEX_PATCH else line)
    return dst


def make_tts(m):
    lex = patched_lexicon(m)
    cfg = sherpa_onnx.OfflineTtsConfig(
        model=sherpa_onnx.OfflineTtsModelConfig(
            kokoro=sherpa_onnx.OfflineTtsKokoroModelConfig(
                model=f"{m}/model.onnx", voices=f"{m}/voices.bin", tokens=f"{m}/tokens.txt",
                data_dir=f"{m}/espeak-ng-data", dict_dir=f"{m}/dict",
                lexicon=f"{m}/lexicon-us-en.txt,{lex}"),
            num_threads=4),
        rule_fsts=f"{m}/date-zh.fst,{m}/phone-zh.fst,{m}/number-zh.fst",
        max_num_sentences=1)
    return sherpa_onnx.OfflineTts(cfg)


def trim(x, sr, thr=0.012):
    """Trim leading/trailing silence, keep 40 ms of air."""
    env = np.convolve(np.abs(x), np.ones(240) / 240, "same")
    idx = np.where(env > thr)[0]
    if len(idx) == 0:
        return x
    pad = int(0.04 * sr)
    return x[max(0, idx[0] - pad):min(len(x), idx[-1] + pad)]


def main():
    m = sys.argv[1]
    sid = int(sys.argv[2]) if len(sys.argv) > 2 else 60
    speed = float(sys.argv[3]) if len(sys.argv) > 3 else 1.08
    os.makedirs(OUT, exist_ok=True)
    tts = make_tts(m)
    timing = []
    for i, ln in enumerate(LINES):
        a = tts.generate(spoken(ln["caption"]), sid=sid, speed=speed)
        x = trim(np.array(a.samples, np.float32), a.sample_rate)
        x = x / (np.abs(x).max() + 1e-9) * 0.89
        path = os.path.join(OUT, "%02d.wav" % i)
        sf.write(path, x, a.sample_rate)
        timing.append(dict(i=i, dur=len(x) / a.sample_rate, sr=a.sample_rate))
        print(i, "%.2fs" % timing[-1]["dur"], spoken(ln["caption"]), flush=True)
    json.dump(dict(sid=sid, speed=speed, lines=timing), open(os.path.join(OUT, "timing.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
