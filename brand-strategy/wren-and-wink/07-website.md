# Wren & Wink · 07 独立站方案（Shopify）

> 域名 wrenandwink.com（可用性**未核实**）。下文所有主题、App 价格均为**未核实**，以 Shopify Theme Store / App Store 当期标价为准。

## 1. 整体美学

**一句话**：一张会动的法式咖啡馆菜单——奶油纸底、可可色衬线字、偶尔一点樱桃红，产品图里有光在闪。

| 元素 | 规范 |
|---|---|
| 背景 | Cream #FBF6EE 全站底色；区块交替用 Powder #E9D3D0 或 Oat #E6DCCD 浅底 |
| 文字 | Cocoa #3B2A26；标题 DM Serif Display，正文 DM Sans 16–18px |
| 按钮 | 主按钮：可可底 + 奶油字，直角或 4px 小圆角（不用胶囊大圆角——太"App 感"）；悬停变 Cherry #A3262E |
| 动效 | 只有两种：产品视频自动播放的"转头闪光"、按钮悬停时 & 符号轻微倾斜。不做弹跳、闪烁、彩带 |
| 图片比例 | 产品主图 4:5；首屏视频 16:9（桌面）/ 9:16（移动） |
| 留白 | 每个区块上下留白 ≥ 80px（桌面）/ 48px（移动） |
| 移动优先 | 预计 75%+ 流量来自手机（社媒引流，行业常见印象，**未核实**），所有区块先设计移动端 |

## 2. 首页线框（自上而下 16 个区块）

| # | 区块 | 内容与布局 | 目的 |
|---|---|---|---|
| 1 | **公告栏** | 可可底奶油字，单行轮播："Free US shipping over $35 · Free EU shipping over €39" / "30-day returns on unworn earrings" | 降低运费顾虑 |
| 2 | **导航栏** | 左：主标 A（Wren *&* Wink）；中：Shop by Hole · Sets · Café Colors · Gifts · About；右：搜索、账户、购物车（显示数量）；货币/国家切换 | 一步到达核心入口 |
| 3 | **首屏 Hero 视频** | 全宽视频：模特转头，6mm 耳钉闪光，慢放 1 秒；左下大字 "A little wink of light."；按钮 "Shop The Wink" + 次按钮 "Build your stack" | 3 秒内讲清"会眨眼的耳钉" |
| 4 | **信任条** | 四个小图标 + 短句：316L stainless steel ｜ Gold-tone PVD ≥0.5μm ｜ Water- & tarnish-resistant ｜ 30-day returns | 先建立材质信任 |
| 5 | **英雄款聚焦：Meet The Wink** | 左：微距图 + 烟花切刻面线稿动画；右：价格、两种表面切换、"Add to bag"；底部一句 "Turn your head. It winks back." | 首页直接可购，缩短路径 |
| 6 | **Shop by Hole** | 三张竖卡：*First Hole*（6mm/8mm）、*Second Hole*（4mm/3mm）、*The Finish*（Huggie）；耳朵线稿标出位置 | 降低选择难度 |
| 7 | **组合推荐：The Double Take & The Encore Trio** | 两张大卡，显示组合价、原价划线、节省金额；文案 "The whole stack. One box. $40." | 拉 AOV，推向免邮门槛 |
| 8 | **畅销网格** | 4 列（移动 2 列）产品卡，悬停/滑动切换到上耳图 | 常规浏览 |
| 9 | **#WearTheWink UGC 视频墙** | 横向滚动的顾客转头视频（取得授权），每条可点开购买同款 | 社会证明 + 社媒原生感 |
| 10 | **Café Colors 限定** | Powder 底；三色彩锆并排（*Rosé*、*Champagne Toast*、*Midnight*），售罄显示 "Gone in a wink. Join the waitlist." | 新鲜感与收集欲 |
| 11 | **材质说明：No fine print** | 可可底奶油字的"小票"样式清单：316L、PVD 厚度、AAAAA-grade CZ 的解释、检测状态（报告到手后展示）；链接到 Materials 页 | 对冲"平价 = 廉价"顾虑 |
| 12 | **评论精选** | 3 条带图评论 + 总评分（Judge.me / Okendo 组件） | 社会证明 |
| 13 | **礼物模块：Send a wink** | 礼物包装加购说明（Love Note 卡 $3）、礼物指南入口、电子礼品卡 | 承接送礼人群 |
| 14 | **品牌小故事** | 鹪鹩线稿 + 三句话："Small bird. Big voice. That's the idea." + "Read our story" | 品牌记忆 |
| 15 | **邮件订阅** | Butter #F1E3B5 底条："Get the first wink." 10% off + 新品早鸟；欧盟用户双重确认 | 订阅率目标 3–5% |
| 16 | **页脚** | 帮助（运费、退换、护理、尺寸）、法律（隐私、Cookie 设置、条款、Impressum/法律声明）、GPSR 制造商与欧盟责任人信息、社媒图标、支付方式图标 | 合规 + 信任 |

## 3. 产品页（PDP）结构

以 The Wink 为模板，其他 SKU 复用：

1. **面包屑**：Home / Studs / The Wink
2. **媒体区**（左，移动端顶部）：① 白底主图 ② 上耳图（暖肤色）③ 上耳图（另一肤色）④ 转头闪光视频 ⑤ 刻面示意图 ⑥ 尺寸对比图（4/6/8mm 在同一只耳朵上）⑦ 包装开箱图
3. **购买区**（右）：标题 + 副标题 → 星级与评论数 → 价格（自动按市场显示 $ / € 含税）→ 表面选择（色块 + 文字 "Polished Steel / Gold-tone"）→ 数量 → "Add to bag" → Shop Pay / Apple Pay 快速结账 → 免邮进度提示 → 信任小字（30 天退换、发货时效）
4. **组合加购模块**："Make it a Double Take — save $4–8"（一键升级为组合）
5. **折叠面板**：Description · Details & specs · Materials & testing · Care · Shipping & returns
6. **"Why fireworks cut?" 图解区**：普通切 vs 烟花切对比
7. **Shop the stack**：模特完整耳叠图，热点标注每件产品
8. **评论区**：带图/视频评论优先，可按"耳洞位置""肤色"筛选
9. **FAQ**（5 条，见 04 号文件）
10. **你可能也喜欢**：同色系 3 件
11. **移动端吸底购买栏**：滚动后固定显示价格与 "Add to bag"

## 4. Shopify 主题推荐

| 主题 | 价格（**未核实**） | 适合理由 | 注意 |
|---|---|---|---|
| **Dawn**（官方免费） | 免费 | 速度快、结构干净，足够实现上面线框；首发推荐 | 视觉需靠字体、配色、图片撑起；部分区块需小改代码 |
| Sense / Craft（官方免费） | 免费 | 更有"品牌感"的默认排版，Craft 偏手作复古，接近咖啡馆氛围 | 同上 |
| Impulse（Archetype Themes） | 约 $350–$400（**未核实**） | 时尚品牌常用，促销、快速购买、组合展示强 | 功能多，需克制使用避免页面过杂 |
| Prestige（Maestrooo） | 约 $350–$400（**未核实**） | 高级感强、大图留白，适合精品调性 | 对图片质量要求高 |
| Be Yours（RoarTheme） | 约 $300–$400（**未核实**） | 美妆/饰品品牌常见，移动端体验好 | — |

**建议**：首发用 Dawn（省钱，预算放在摄影上）；跑通 3 个月、月销稳定后再评估换 Prestige 或 Impulse。

## 5. 必装 App 清单

| 类别 | 推荐 | 价格（**未核实**） | 用途 |
|---|---|---|---|
| 评论 | Judge.me（首选，性价比高）/ Okendo / Loox | 免费起 – 约 $15+/月 | 带图视频评论、评论邀请邮件 |
| 邮件 / SMS | Klaviyo（首选）；SMS 可用 Klaviyo SMS 或 Postscript（仅美国） | 免费起（按联系人计费） | 欢迎流、弃购流、复购流；SMS 需合规同意 |
| 组合 / Bundle | Shopify Bundles（官方免费）或 Fast Bundle | 免费 – 约 $20/月 | Double Take、Encore Trio、Build Your Own Trio |
| 加购 / Upsell | Rebuy 或 ReConvert / Shopify Search & Discovery（官方免费，含推荐） | 免费 – 视套餐 | 购物车加购 Little Wink、免邮进度条 |
| 免邮进度条 | 主题自带或 Rebuy Smart Cart | — | "You're $X away from free shipping" |
| 翻译 | Shopify Translate & Adapt（官方免费）/ Weglot | 免费 – 约 €15+/月 | 德、法、荷语；英文为主 |
| 多币种 / 多市场 | Shopify Markets（内置） | 内置 | 欧元含税定价、按国家显示价格 |
| Cookie 同意 / GDPR | Pandectes GDPR Compliance 或 Consentmo | 免费起 – 约 $10+/月 | 欧盟 Cookie 横幅、同意记录、像素按同意加载 |
| 法律页面 | Shopify 政策生成器 + 律师审阅 | — | 隐私、退换（含欧盟 14 天撤回权）、条款、Impressum |
| 达人 / 联盟 | Shopify Collabs（官方）或 UpPromote | 免费起 | 达人专属码、佣金追踪 |
| 礼物 | 主题自带礼物卡 + 加购 Love Note 卡 | — | 送礼场景 |
| 物流追踪 | AfterShip / Parcel Panel | 免费起 | 减少"我的包裹在哪"客服量 |
| 分析 | GA4 + Meta / TikTok 像素（官方渠道 App） | 免费 | 转化追踪（受 Cookie 同意控制） |

**原则**：上线时 App ≤ 8 个，每个都要能说清带来什么指标，避免拖慢速度。

## 6. 转化率检查清单

**速度与技术**
- [ ] 移动端 LCP < 2.5 秒（PageSpeed 测）；首屏视频压缩 < 3MB，提供静态封面
- [ ] 图片用 WebP、懒加载；App 数量 ≤ 8
- [ ] 结账开启 Shop Pay、Apple Pay、Google Pay、PayPal；欧盟加 iDEAL（荷兰）、Klarna 等本地支付（可用性**未核实**）

**信任**
- [ ] 每个 PDP 写清 316L stainless steel、PVD 厚度、AAAAA 的解释
- [ ] 检测报告合格后，在 Materials 页公开报告摘要
- [ ] 退换政策在 PDP、购物车、页脚三处可见
- [ ] 评论 ≥ 20 条前，先用达人内容和开箱视频补社会证明（不伪造评论）
- [ ] 页脚有真实联系方式、GPSR 信息

**说服**
- [ ] 首屏 3 秒内看到"转头闪光"
- [ ] 每个 PDP 至少 1 条上耳视频 + 尺寸对比图
- [ ] 购物车免邮进度条 + 一键加购 Little Wink
- [ ] 组合显示原价划线与节省金额（必须真实计算）
- [ ] 不用虚假倒计时、虚假"仅剩 2 件"（欧盟不公平商业行为法规风险）

**留存**
- [ ] 订阅弹窗延迟 8 秒或滚动 40% 后出现，移动端不遮挡全屏（Google 移动体验要求）
- [ ] 订单确认页邀请关注 TikTok / IG
- [ ] 欧盟订阅双重确认；Cookie 拒绝选项与接受同样醒目

**每周看板**：会话数、转化率（目标 2.0–3.0%）、AOV（目标 ≥ $38）、加购率、结账放弃率、订阅率（3–5%）、移动端跳出率。
