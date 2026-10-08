# 多巴胺的陷阱 · 像素风竖屏短视频

成片：`output/dopamine_trap_9x16.mp4`（1080×1920，30fps，约 83 秒，H.264 + AAC，响度 -14 LUFS）

全部画面由 Python 逐帧绘制：原生 360×640 像素，最近邻放大 3 倍，角色再额外放大 2–5 倍（大颗粒像素）。
配音用 Kokoro v1.1-zh（sherpa-onnx，离线）生成，背景音乐和音效也全部由程序合成。

## 结构

| 文件 | 作用 |
| --- | --- |
| `script.py` | 旁白 / 字幕文案（`{}` 为金色高亮），每句对应的场景和章节 |
| `tts.py` | 生成配音 `build/vo/NN.wav` 和 `timing.json`（含多音字修正） |
| `timeline.py` / `events.py` | 按配音时长推算场景切换点和所有动画、音效的时间 |
| `scenes_a.py` `scenes_b.py` `scenes_c.py` `scene_bedroom.py` | 13 个场景 |
| `chibi.py` | 大头像素主角、老鼠等角色精灵 |
| `ui.py` `style.py` | 顶部章节栏、BOSS 血条、字幕样式、金框面板、聚光灯、放射光 |
| `audio.py` | 配音 + 背景音乐（人声时自动压低）+ 音效混音 |
| `render.py` | 渲染（多进程）与预览 |

## 重新生成

```bash
pip install numpy pillow soundfile sherpa-onnx
# 改了文案才需要重跑配音（模型：k2-fsa/sherpa-onnx releases → tts-models/kokoro-multi-lang-v1_1.tar.bz2）
python tts.py /path/to/kokoro-multi-lang-v1_1 60 1.08     # 参数：模型目录、说话人 ID（58+ 为男声）、语速
python render.py preview /tmp/prev 6.9 40.3                # 预览指定时间点
python render.py video build/video_silent.mp4
python audio.py build/audio.wav
ffmpeg -i build/video_silent.mp4 -i build/audio.wav -map 0:v -map 1:a -c:v copy \
  -af loudnorm=I=-14:TP=-1.5:LRA=11 -c:a aac -b:a 192k -shortest output/dopamine_trap_9x16.mp4
```

字体：Fusion Pixel（TakWolf，SIL OFL 1.1）。配音模型：Kokoro-82M v1.1-zh（Apache-2.0）。
