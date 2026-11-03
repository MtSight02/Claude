# Finch & Flare · 07 网站与电商

> 平台建议：Shopify（Basic 起步，用 Shopify Markets 管理美国 + 欧盟）。域名 finchandflare.com（**可用性未核实**）。所有主题、App 价格均为撰写时印象，**未核实**，以官方页面为准。

---

## 1. 整体审美

**一句话**：一本关于"光"的小杂志，恰好可以买东西。

| 维度 | 规范 |
|---|---|
| 底色 | Ivory `#F6F1E9` 为主；区块交替用 Linen `#ECE4D8`；品牌故事 / 夜景区块用 Ink `#1F2433` 满版 |
| 字体 | 标题 Cormorant Garamond（含一个斜体词），UI 与正文 Manrope |
| 按钮 | Ink 底 + Ivory 字、直角或 2px 圆角，全大写 14px；**不用 Ember 做按钮**（对比度不足，见 03 号文件） |
| Ember 用法 | 每屏最多一处：星芒图标、"Limited" 小标签、链接悬停下划线 |
| 动效 | 克制：图片淡入 300ms；唯一的"表演"是首屏视频里真实的火彩 |
| 图片比例 | 商品卡 4:5；首屏视频桌面 16:9 / 手机 9:16 |
| 留白 | 区块上下 96px（桌面）/ 56px（手机）；一屏只讲一件事 |
| 速度 | 移动端 LCP < 2.5 秒；首屏视频 ≤ 2MB、静音自动播放、带海报图 |

---

## 2. 首页：逐块线框描述（14 块）

| # | 区块 | 内容与布局 | 文案示例（English） | 目的 |
|---|---|---|---|---|
| 1 | **公告条** | Ink 底 Champagne 小字，单行，可轮播 2 条 | "Free US shipping over $35 · EU over €39" / "30-day returns" | 消除运费顾虑 |
| 2 | **页眉** | 左：Shop / Ear Map / About；中：主标 Logo；右：搜索、账户、购物袋；Markets 货币切换器在页脚 | — | 极简导航 |
| 3 | **首屏 Hero 视频** | 全宽 9:16 / 16:9 自适应：黑底单光源下 The Flare 缓慢转动；左下叠字 | H1: "Pocket-sized *fireworks*." 副标: "Fireworks-cut studs in 316L steel, from $18." 按钮: [Shop The Flare] [Build your stack] | 3 秒内讲清产品与价格 |
| 4 | **信任条** | 4 个图标 + 短语，Linen 底 | "Fireworks cut" · "316L stainless steel" · "Free shipping over $35" · "30-day returns" | 快速建立信任 |
| 5 | **主打款聚焦** | 左图（佩戴特写）右文：价格、颜色切换、加入购物袋（首页直接加购） | "The Flare — the stud that named the brand. $22 / $24" | 缩短购买路径 |
| 6 | **The Full Show 组合块** | 耳朵示意图上标出 3 个位置 + 三件产品；显示"单买 $68 → $40" | "The whole stack. $40." | 提升 AOV |
| 7 | **按耳洞购物** | 三张卡：First piercing / Second & third / Full ear | "How many holes? We have a plan for each." | 解决"选择困难" |
| 8 | **切工解释** | Ink 满版：左侧刻面示意图（Champagne 细线），右侧 3 行文字 + 8 秒无滤镜微距视频 | "Most studs shine. Ours *spark*." | 讲清核心差异 |
| 9 | **尺寸对比** | 同一只耳朵 4 / 6 / 8mm 三连图，可点击切换 | "Spark, Flare, or Finale?" | 降低尺寸退货 |
| 10 | **UGC / 评价墙** | Judge.me 照片评价轮播，显示星级与总评价数；不足 20 条前用"内测顾客"真实评价 | "Real ears, real light. No filters." | 社会证明 |
| 11 | **包装开箱** | 火柴盒开箱 GIF / 短视频 + 3 行说明 | "It arrives in a matchbox. No matches included." | 送礼与质感 |
| 12 | **材质透明块** | 3 栏：Steel（316L）/ Finish（PVD，18K gold-tone）/ Testing（报告下载，**拿到报告后才显示**） | "What it's made of. What it isn't." | 回应 Persona B 的顾虑 |
| 13 | **邮件订阅** | Ivory 底，一行输入框 | "First light, first. 10% off your first order + early access to drops." | 建立私域 |
| 14 | **页脚** | 导航、政策页（运送、退货、隐私、Cookie、Impressum / 法律信息）、制造商与欧盟责任人信息、货币 / 语言切换、社媒 | — | 合规与信任 |

---

## 3. 商品详情页（PDP）结构

| 顺序 | 模块 | 说明 |
|---|---|---|
| 1 | 图片 / 视频画廊（左，桌面 60% 宽） | ① 佩戴 3/4 侧脸 ② 8 秒微距视频 ③ 刻面示意图 ④ 尺寸对比图 ⑤ 火柴盒包装 ⑥ 平铺白底（Linen 底）；手机端可左右滑动 |
| 2 | 标题、副标题、星级（链接到评价） | "The Flare — 6mm Fireworks-Cut Studs" |
| 3 | 价格 + 免邮进度提示 | 欧盟显示含 VAT 价格及"incl. VAT" |
| 4 | 颜色切换（Steel / Gold-tone 色块） | 切换后主图联动 |
| 5 | 加入购物袋 + 动态支付按钮（Shop Pay / Apple Pay / PayPal） | 欧盟加 Klarna / iDEAL / Bancontact 等本地支付（以 Shopify Payments 支持情况为准，**未核实**） |
| 6 | 3 行信任小字 | Ships in 1–2 business days · 30-day returns · Arrives gift-ready |
| 7 | 短描述 + 4 条卖点 | 见 04 号文件 |
| 8 | "Complete the stack" 组合推荐 | The Full Show / The Duet，一键升级 |
| 9 | 折叠面板 | Details & specs / Care / Shipping & returns / Materials & testing |
| 10 | FAQ ×5 | 见 04 号文件 |
| 11 | 评价区（带照片筛选） | 按"颜色""耳洞位置"筛选 |
| 12 | "You might also like" | 最多 4 个 |
| 13 | 手机端吸底加购条 | 滚过加购按钮后出现 |

---

## 4. Shopify 主题推荐

| 主题 | 价格（**未核实**） | 优点 | 缺点 | 适合阶段 |
|---|---|---|---|---|
| **Dawn** | 免费（Shopify 官方） | 速度快、稳定、OS 2.0 全支持；足够做出杂志感 | 需要较多自定义 CSS 才不"模板感" | **精简版首选** |
| Sense / Craft | 免费（官方） | 比 Dawn 更有设计感的默认样式 | 同上 | 精简版备选 |
| **Prestige**（Maestrooo） | 约 $350–$400 一次性 | 高端时尚品牌常用，大图与编辑排版出色 | 稍重，需要压缩视频与图片 | **标准版首选** |
| Impulse（Archetype） | 约 $350–$400 一次性 | 促销、组合、快速购买功能完善 | 默认风格偏"零售"，需调克制 | 标准版备选 |
| Be Yours（Roar Theme） | 约 $300–$400 一次性 | 珠宝美妆类模板多、动效好看 | 动效需克制使用 | 进取版备选 |
| Symmetry / Release 等 | 约 $300–$400 | 功能全面 | — | 备选 |

> 建议：标准版用 **Prestige**；先在 Shopify 主题商店免费试用（**试用政策未核实**），用真实商品图搭好首页与 PDP 再付费。

---

## 5. 必装 App 清单

| 类别 | 推荐 | 备选 | 价格（**未核实**） | 用途 |
|---|---|---|---|---|
| 评价 | **Judge.me** | Okendo、Loox | 免费起 / 约 $15/月 | 照片评价、评价请求邮件、Google 星级 |
| 邮件 / SMS | **Klaviyo** | Omnisend；SMS 可用 Postscript（美国） | 免费起，按联系人计费 | 欢迎、弃购、浏览放弃、售后流程 |
| 组合 / Bundles | **Shopify Bundles**（官方） | Fast Bundle、Rebuy Bundles | 免费 / 约 $20+/月 | The Duet、The Full Show、Build-your-own |
| 加购 / 追加销售 | **AfterSell** 或 ReConvert | Rebuy | 约 $10–$30/月 起 | 结账后一键加购 The Spark |
| 免邮进度条 | 主题自带或 **Hextom Free Shipping Bar** | — | 免费起 | 推 AOV |
| 翻译 | **Shopify Translate & Adapt**（官方） | Weglot、Langify | 免费 / 约 €15+/月 | 德、法、荷语本地化（人工校对） |
| 货币 / 市场 | **Shopify Markets**（内置） | — | 内置 | 欧元含税价、按国家定价 |
| Cookie / GDPR | Shopify 自带客户隐私横幅 | **Pandectes**、Consentmo | 免费起 | 欧盟 Cookie 同意、Google Consent Mode |
| 法律页面 | Shopify 政策生成器 + 律师审核 | — | — | 退货、隐私、Impressum（德国） |
| 订阅弹窗 | Klaviyo 表单 | Privy | 包含在 Klaviyo | 10% 首单优惠 |
| 达人 / 联盟 | **Shopify Collabs** | UpPromote | 免费 / 低价起 | 专属码与佣金 |
| 客服 | **Shopify Inbox** | Gorgias（规模变大后） | 免费 | 聊天、订单查询 |
| 物流追踪 | 3PL 自带 / **Parcel Panel** | AfterShip | 免费起 | 品牌化追踪页，减少 WISMO 工单 |
| 分析 | GA4 + Meta / TikTok 官方渠道 App（含 Conversions API） | Triple Whale（规模变大后） | 免费 / 付费 | 广告归因 |

> App 越少越快：首发只装 8–10 个，每个都要能说出"它为哪个 KPI 负责"。

---

## 6. 转化率检查清单（上线前逐项打勾）

**首屏与导航**
- [ ] 手机首屏 3 秒内看到：产品是什么、价格从多少、一个按钮
- [ ] 导航 ≤ 4 个一级菜单
- [ ] 搜索可用，搜 "gold" "huggie" "4mm" 都有结果

**商品页**
- [ ] 每个 SKU 至少 1 条真实佩戴视频
- [ ] 尺寸对比图（4/6/8mm 同一只耳朵）
- [ ] 价格附近显示免邮门槛与退货政策
- [ ] 颜色切换联动主图
- [ ] 手机吸底加购条
- [ ] 材质与保养写清楚，**无任何红线词**（上线前用 Ctrl+F 检查红线清单）

**信任**
- [ ] 评价 ≥ 10 条再开广告（内测顾客真实评价）
- [ ] About 页、联系方式、实体地址（GPSR / 德国 Impressum 要求）
- [ ] 检测报告下载链接（拿到报告后）
- [ ] 安全支付图标、Shop Pay、PayPal

**购物车与结账**
- [ ] 抽屉式购物车 + 免邮进度条 + 一个加购推荐（The Spark）
- [ ] 结账页启用 Shop Pay、Apple Pay、Google Pay、PayPal；欧盟本地支付方式按可用性开启
- [ ] 欧盟价格含 VAT，结账无"惊喜"费用；美国订单的关税 / 进口费用规则写清楚
- [ ] 结账字段最少化；自动填充地址

**合规**
- [ ] Cookie 横幅（欧盟访客默认拒绝非必要 Cookie，Consent Mode 已配置）
- [ ] 退货政策：30 天；卫生例外条款经律师确认
- [ ] 商品页 / 页脚有制造商与欧盟责任人信息
- [ ] 达人与评价中涉及赠品的内容已标注

**速度与追踪**
- [ ] PageSpeed 移动端 ≥ 60（主题 + 视频压缩后）
- [ ] 所有图片 WebP、懒加载；首屏视频 ≤ 2MB
- [ ] Meta Pixel + CAPI、TikTok Pixel + Events API、GA4 已测试"加购—结账—购买"三个事件
- [ ] 每周看板：会话、转化率（目标 2.0–3.0%）、AOV、加购率、结账放弃率、邮件订阅率（目标 3–5%）
