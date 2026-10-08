"""Narration script. One entry per voice-over line.

caption: what is shown on screen ({..} = gold highlight, \\n = line break)
scene:   which scene is on screen while this line is spoken
pause:   silence after the line (seconds)
"""

CHAPTERS = ["凌晨两点", "渴望分子", "口袋老虎机", "跳出陷阱"]

LINES = [
    # chapter 0
    dict(scene="intro", ch=0, pause=0.35, caption="你知道，\n你今晚刷了多少条{短视频}吗？"),
    dict(scene="bedroom", ch=0, pause=0.25, caption="凌晨两点四十七，\n你对自己说：{最后一条}。"),
    dict(scene="bedroom", ch=0, pause=0.3, caption="然后，又刷了{一个小时}。"),
    dict(scene="bedroom", ch=0, pause=0.5, caption="这不怪你。你在对抗的，\n是大脑里的{多巴胺}。"),
    # chapter 1
    dict(scene="molecule", ch=1, pause=0.25, caption="很多人以为，\n多巴胺是{快乐分子}。"),
    dict(scene="molecule", ch=1, pause=0.3, caption="其实，它更像{渴望分子}。"),
    dict(scene="wantlike", ch=1, pause=0.3, caption="它不负责让你{满足}，\n只负责让你{想要}。"),
    dict(scene="carrot", ch=1, pause=0.5, caption="就像吊在眼前的胡萝卜，\n{永远差一口}。"),
    # chapter 2
    dict(scene="skinner", ch=2, pause=0.25, caption="心理学家{斯金纳}\n做过一个实验。"),
    dict(scene="skinner", ch=2, pause=0.25, caption="奖励固定时，\n老鼠{吃饱就停}。"),
    dict(scene="skinner", ch=2, pause=0.35, caption="可一旦奖励变得{随机}，\n它就{停不下来}了。"),
    dict(scene="slot", ch=2, pause=0.25, caption="你手里的手机，\n就是一台{老虎机}。"),
    dict(scene="slot", ch=2, pause=0.35, caption="下一条会更好看吗？{不知道}。\n所以你一直刷。"),
    dict(scene="graph", ch=2, pause=0.25, caption="更糟的是，刺激越强，\n大脑越会{关小音量}。"),
    dict(scene="graph", ch=2, pause=0.3, caption="读书、散步、发呆，\n全都变得{索然无味}。"),
    dict(scene="cage", ch=2, pause=0.55, caption="你以为在追快乐，\n其实是在追{下一次可能}。"),
    # chapter 3
    dict(scene="unlock", ch=3, pause=0.25, caption="好消息是，\n大脑{可以恢复}。"),
    dict(scene="skills", ch=3, pause=0.25, caption="送你三个技能，\n{今晚就能用}。"),
    dict(scene="skills", ch=3, pause=0.2, caption="第一，关掉不必要的{通知}。"),
    dict(scene="skills", ch=3, pause=0.2, caption="第二，睡前把手机\n放到{够不到}的地方。"),
    dict(scene="skills", ch=3, pause=0.4, caption="第三，用运动、阅读、\n晒太阳，换回{慢多巴胺}。"),
    dict(scene="sunrise", ch=3, pause=0.3, caption="真正的快乐，\n不需要{下一条}。"),
    dict(scene="sunrise", ch=3, pause=0.4, caption="能看到这里，\n你已经赢了它{一次}。"),
    dict(scene="follow", ch=3, pause=1.2, caption="觉得有用，{点个关注}，\n下一期别错过。"),
]

LEAD_IN = 0.7  # seconds before the first line


def spoken(caption):
    """Text sent to TTS (strip markup)."""
    return caption.replace("{", "").replace("}", "").replace("\n", "")
