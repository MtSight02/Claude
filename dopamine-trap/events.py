"""Key moments, derived from the voice-over timing. Used by both picture and sound."""
import numpy as np

from timeline import L, word_t, SCENE_T

# --- intro
INTRO_POP = [0.15, 0.45, 0.75, 0.95, 1.15]
COUNT = (1.4, 3.1)

# --- bedroom
_b0, _b1 = SCENE_T["bedroom"]
FEED = [t for t in np.arange(_b0 + 0.3, L(2, 0.05), 0.75)] + \
       [t for t in np.arange(L(2, 0.05), L(2, 1.0), 0.28)] + \
       [t for t in np.arange(L(2, 1.0) + 0.3, L(3, 0.3), 0.7)]
BUBBLE_T = word_t(1, "最后一条") - 0.2
CLOCK_FF = (L(2, 0.05), L(2, 0.9))
PLUS1H_T = word_t(2, "一个小时") - 0.1
ZOOM = (L(3, 0.0), L(3, 0.34))
BRAIN_CUT = L(3, 0.34)
DOPA_LABEL_T = word_t(3, "多巴胺") - 0.1
BURSTS = [BRAIN_CUT + 0.35, BRAIN_CUT + 0.85, BRAIN_CUT + 1.25, DOPA_LABEL_T + 0.05]

# --- molecule
HAPPY_CARD_T = word_t(4, "快乐分子") - 0.15
STRIKE_T = L(5, 0.08)
WANT_CARD_T = word_t(5, "渴望分子") - 0.15

# --- want / like panel
SATISFY_T = word_t(6, "满足") - 0.05
WANT_T = word_t(6, "想要") - 0.05

# --- skinner box
FIXED_PRESSES = [L(9, 0.08), L(9, 0.3), L(9, 0.52)]
SLEEP_T = L(9, 0.72)
RANDOM_PRESSES = list(np.arange(L(10, 0.0), SCENE_T["skinner"][1] - 0.05, 0.21))
_rng = np.random.default_rng(4)
RANDOM_REWARDS = [p for i, p in enumerate(RANDOM_PRESSES) if i in (3, 11) or _rng.random() < 0.07]

# --- slot machine
PULLS = [L(11, 0.4), L(12, 0.0) + 0.05, L(12, 0.84)]
STOPS = [(PULLS[0] + 0.55, PULLS[0] + 0.8, PULLS[0] + 1.2),
         (word_t(12, "不知道", end=True) + 0.15, word_t(12, "不知道", end=True) + 0.35,
          word_t(12, "不知道", end=True) + 0.6),
         (99.0, 99.0, 99.0)]
NEAR_MISS_T = STOPS[0][2]
JACKPOT_T = STOPS[1][2]

# --- graph
GRAPH_DRAW = (L(13, 0.0), L(13, 0.62))
VOLUME_T = word_t(13, "关小音量") - 0.3
VOLUME_STEPS = [VOLUME_T + 0.15 + k * 0.16 for k in range(7)]
GREY_T = [word_t(14, "读书"), word_t(14, "散步"), word_t(14, "发呆")]
DULL_T = word_t(14, "索然无味")

# --- cage
_c0, _c1 = SCENE_T["cage"]
_rng2 = np.random.default_rng(12)
PINGS = sorted(_c0 + 0.2 + _rng2.random(10) * (_c1 - _c0 - 0.8))
Q_T = word_t(15, "下一次可能") - 0.1

# --- unlock
UNLOCK_T = word_t(16, "可以恢复") - 0.05

# --- skills
CHEST_T = L(17, 0.0) - 0.1
CARDS_T = L(17, 0.3)
SKILL_T = [L(18, 0.0) - 0.25, L(19, 0.0) - 0.2, L(20, 0.0) - 0.2]
SKILL_HIT = [L(18, 0.7), L(19, 0.7), L(20, 0.7)]

# --- sunrise / follow
BOSS_DOWN_T = L(21, 0.1)
CLICK_T = word_t(23, "点个关注") + 0.25
