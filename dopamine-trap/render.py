"""Render the video.

    python render.py preview OUTDIR t1 t2 ...   # preview PNGs (2x) for given timestamps
    python render.py video out.mp4              # all frames -> silent mp4 (1080x1920)
"""
import os
import subprocess
import sys
from multiprocessing import Pool

import numpy as np
from PIL import Image

from engine import W, H, FPS, SCALE, new, clamp01, smooth
from timeline import SCENES, DUR, scene_at
import ui
import scenes_a as A
import scenes_b as B
import scenes_c as Cc

FN = {
    "intro": A.intro, "bedroom": A.bedroom, "molecule": A.molecule, "wantlike": A.wantlike,
    "carrot": A.carrot, "skinner": B.skinner, "slot": B.slot, "graph": B.graph, "cage": B.cage,
    "unlock": Cc.unlock, "skills": Cc.skills, "sunrise": Cc.sunrise, "follow": Cc.follow,
}
NAMES = [n for n, s, e in SCENES]
XF = 0.22          # cross-fade length
DIP = {"unlock"}   # scenes entered through black (chapter change)


def frame(t):
    i = NAMES.index(scene_at(t))
    name, s, e = SCENES[i]
    a = FN[name](t)
    if i > 0 and t < s + XF:
        k = (t - s) / XF
        if name in DIP:
            a = (a * smooth(k)).astype(np.uint8)
        else:
            prev = FN[NAMES[i - 1]](t)
            a = (prev * (1 - smooth(k)) + a * smooth(k)).astype(np.uint8)
    if i + 1 < len(NAMES) and NAMES[i + 1] in DIP and t > e - XF:
        a = (a * (1 - smooth((t - (e - XF)) / XF))).astype(np.uint8)
    ui.overlays(a, t)
    if t > DUR - 0.5:
        a = (a * (1 - smooth((t - (DUR - 0.5)) / 0.5))).astype(np.uint8)
    return a


def frame_bytes(i):
    return frame(i / FPS).tobytes()


def preview(ts, outdir):
    os.makedirs(outdir, exist_ok=True)
    for t in ts:
        a = frame(float(t))
        Image.fromarray(a).resize((W * 2, H * 2), Image.NEAREST).save(os.path.join(outdir, "t%05.2f.png" % float(t)))


def video(out):
    n = int(round(DUR * FPS))
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
           "-r", str(FPS), "-i", "-", "-vf", f"scale={W * SCALE}:{H * SCALE}:flags=neighbor",
           "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-tune", "animation",
           "-pix_fmt", "yuv420p", "-movflags", "+faststart", out]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    with Pool(os.cpu_count()) as pool:
        for i, buf in enumerate(pool.imap(frame_bytes, range(n), chunksize=4)):
            proc.stdin.write(buf)
            if i % 300 == 0:
                print(f"frame {i}/{n}", flush=True)
    proc.stdin.close()
    proc.wait()


if __name__ == "__main__":
    if sys.argv[1] == "preview":
        preview(sys.argv[3:], sys.argv[2])
    else:
        video(sys.argv[2])
