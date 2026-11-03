# Lark & Luce · 07 网站（Shopify）

> 域名 larkandluce.com（可用性未核实）。建站原则：**像一本安静的欧洲杂志，而不是一个促销货架**——但每一个安静的模块都必须有明确的转化任务。

## 1. 整体美学

| 维度 | 规范 |
|---|---|
| 背景 | Bone `#F3EFE8` 全站底色；卡片用 Mist `#E4DED4` |
| 文字 | Graphite `#2B2B2B`；辅助信息 Stone `#A39E93` |
| 强调 | Dawn `#E8C9B5`（角标、Hover），Gilt `#B89B5E`（星级、细线、光点） |
| 字体 | 标题 Cormorant Garamond Light；导航/按钮/价格 Jost 全大写；规格 IBM Plex Mono |
| 留白 | 模块间距桌面 120px / 手机 72px；首屏只放 1 张图 + 1 句话 + 1 个按钮 |
| 动效 | 仅两种：图片缓慢淡入（600ms）、Hero 视频中一束光扫过；无弹跳、无闪烁倒计时 |
| 按钮 | Graphite 实底 + Bone 字，直角或 2px 圆角；次级按钮为 1px Graphite 描边 |
| 图片比例 | 产品卡 4:5；Hero 桌面 16:9 / 手机 4:5 |

## 2. 首页线框（自上而下 13 个模块）

| # | 模块 | 内容 | 转化任务 |
|---|---|---|---|
| 1 | **公告栏** | "Free shipping over $35 · €39 in the EU · 30-day returns"（Jost 11px，Graphite 底） | 拉高 AOV、降低风险感 |
| 2 | **页头** | 居中 Logo A（LARK & LUCE + 地平线细线）；左侧 Shop / Stacks / The Cut / About；右侧 搜索 / 账户 / 购物袋；市场切换（USD/EUR） | 导航清晰 |
| 3 | **Hero 视频** | 8 秒循环：晨光扫过 Gilt Luce 耳钉；标题 "Catch the first light."；副标 "Fireworks-cut studs in 316L steel, from $18."；按钮 [Shop The Luce] | 进入主打 PDP |
| 4 | **信任条** | 4 个图标 + 短语：316L stainless steel · Fireworks-cut CZ · Free shipping $35+ · 30-day returns（检测报告到手后增加 "Nickel-release tested (EU)"） | 回答首要顾虑 |
| 5 | **Bestsellers 横滑** | 4 张产品卡：Luce / Glint / Alba Huggie / Dawn Chorus；卡片 Hover 切换为上耳图；显示星级 | 浏览 → 加购 |
| 6 | **The Cut（切工解释）** | 左：刻面示意线稿（Gilt 细线）；右：三行文字 "Dozens of facets. Finer flashes. More light in less size." + [See it up close] | 建立唯一卖点 |
| 7 | **Build your stack** | 一张耳部大图，三处热点标注 Glint / Luce / Alba；下方 Dawn Chorus $40（对比 $68+）+ [Add the stack] | 推组合、过门槛 |
| 8 | **Shop by size** | 4mm / 6mm / 8mm 三格，同一耳朵不同尺寸实拍，附 "Most loved" 标签于 6mm | 降低尺寸犹豫 |
| 9 | **The Hours（当月 drop）** | 每月替换的主题区：三色彩锆 + 一句诗意文案 "For the minutes after sunset." | 新鲜感与复访 |
| 10 | **UGC / 评价墙** | 6–9 张真实用户窗边照 + 精选评价；Judge.me/Okendo 驱动 | 社会证明 |
| 11 | **品牌故事缩略** | "Lark & Luce (LOO-chay) — Italian for light." + 两句故事 + [▶ hear it] 音频 + [Read our story] | 建立品牌、解决发音 |
| 12 | **邮件订阅** | "Join the Early Larks — 10% off your first order, and first light on every new drop." 只要邮箱一个字段 | 留资（目标 3–5% 访客） |
| 13 | **页脚** | 护理 / 运输 / 退换 / 材料与检测 / FAQ / 联系；制造商与欧盟责任人信息（GPSR）；隐私与 Cookie 设置；社媒 @larkandluce | 合规与信任 |

## 3. 产品页（PDP）结构

**首屏（桌面左右分栏 / 手机上下）**
1. 左：图片 8–10 张——①白底主图 ②微距火彩 ③上耳（6mm）④尺寸对比（硬币）⑤Steel/Gilt 对比 ⑥包装开箱 ⑦刻面示意 ⑧10 秒光线视频。
2. 右：
   - 产品名 "The Luce Stud — 6mm Fireworks-Cut" + 副标
   - 星级 + 评论数（点击跳转）
   - 价格（按市场显示 USD 或 EUR 含税）
   - 表面选择：Steel / Gilt（色块 + 文字）
   - 尺寸切换：4mm / 6mm / 8mm（链接到对应 PDP，形成阶梯）
   - 加购按钮 [Add to bag]；下方 Shop Pay / Apple Pay 快捷支付
   - 免邮进度条："Add $13 more for free shipping"
   - 升级提示："Make it a Duet — add the 4mm Glint for $14 more"（Bundles App）
   - 三行信任："Ships in 1–2 business days · 30-day returns · Arrives gift-ready"

**下方折叠区**
3. Description（短描述）→ Why you'll love it（5 条）→ Details & specs（表格）→ Care → Shipping & returns。
4. "The Cut" 刻面示意模块（与首页共用组件）。
5. "Complete the stack" 推荐（Rebuy / Shopify Search & Discovery）。
6. 评论区（带照片筛选）。
7. FAQ（5 条，见 04 文件）。
8. 粘性加购栏（手机端下滑后出现）。

## 4. Shopify 主题推荐

| 主题 | 价格 | 适合原因 | 注意 |
|---|---|---|---|
| **Dawn**（官方免费） | 免费 | 速度快、结构干净，改字体与配色即可接近我们的美学；**标准版推荐** | 需要少量自定义 CSS（细线、Plex Mono 规格表） |
| Prestige | 约 $350–$400（未核实） | 奢华品牌常用，大图与编辑感排版出色 | 价格高，加载需优化 |
| Be Yours | 约 $300–$380（未核实） | 极简柔和，适合首饰/美妆 | 第三方主题，检查更新频率 |
| Impulse | 约 $300–$380（未核实） | 促销与集合页功能强 | 风格偏商业，需要去"热闹感" |
| Sense / Craft（官方免费） | 免费 | Craft 偏手工质感、Sense 偏美妆，可作 Dawn 的备选 | 模块灵活度略低 |

## 5. 必装 App

| 用途 | 推荐 | 备选 | 费用 |
|---|---|---|---|
| 评价（带图/视频） | Judge.me | Okendo、Loox | 有免费档，进阶付费（未核实） |
| 邮件 + SMS | Klaviyo | Omnisend；SMS 可用 Postscript（美国） | 按联系人计费（未核实） |
| 组合 / Bundles | Shopify Bundles（官方） | Fast Bundle | 官方免费（未核实） |
| 加购 / 追加销售 | Rebuy（预算够时） | ReConvert（感谢页追加）、Shopify Search & Discovery（免费推荐） | 未核实 |
| 多语言 | Shopify Translate & Adapt | Weglot | 官方免费档（未核实） |
| 多币种 / 多市场 | Shopify Markets（内置）+ 欧元含税定价 | — | 内置 |
| Cookie 同意 / GDPR | Consentmo | Pandectes、Shopify Customer Privacy Banner | 未核实 |
| 订阅弹窗 | Klaviyo 表单 | Privy | 随 Klaviyo |
| 缺货提醒 | Klaviyo Back in Stock | Notify Me! | 未核实 |
| 客服 | Shopify Inbox | Gorgias（订单量大后） | 免费 / 付费 |
| 物流追踪与退换 | AfterShip / Shopify 原生退货 | Loop Returns | 未核实 |
| 欧盟税务 | Shopify Tax + IOSS 设置 | — | 内置 |

> 原则：前 90 天 App 总月费控制在 $100 以内（估算），每装一个 App 测一次手机端 LCP。

## 6. 转化率检查清单

**信任**
- [ ] 每个 PDP 写明 316L stainless steel、PVD 镀层厚度、CZ 等级解释
- [ ] 检测报告到手后在"Materials & Testing"页公开摘要
- [ ] 退换政策 30 天，在 PDP、购物袋、页脚三处可见
- [ ] 至少 20 条真实评价后再开大额广告；评论不可编造
- [ ] 页脚有公司信息、欧盟责任人（GPSR）、联系邮箱

**清晰**
- [ ] 每个 PDP 有尺寸对比图与上耳图
- [ ] 价格按访客市场显示（USD / EUR 含 VAT），不在结账时"多出"税费
- [ ] 运输时间按地区写清；欧盟写明是否含关税（DDP）
- [ ] 发音行 "LOO-chay" 出现在首页与 About

**速度与手机**
- [ ] 手机 LCP < 2.5 秒；图片 WebP、懒加载
- [ ] 主要按钮在拇指区；粘性加购栏
- [ ] 结账开启 Shop Pay、Apple Pay、Google Pay、PayPal；欧盟加 iDEAL（荷兰）、Klarna/SOFORT 类本地支付（可用性未核实）

**AOV**
- [ ] 免邮进度条
- [ ] PDP 内"升级为 Duet"提示
- [ ] 购物袋内"Add a Seed / Glint"一键加购
- [ ] 感谢页追加推荐（限时 10 分钟内同单发货）

**留存与追踪**
- [ ] Meta Pixel + Conversions API、TikTok Pixel + Events API 已配置并测试
- [ ] GA4 + 每周看板：会话、CVR（目标 2.0–3.0%）、AOV、订阅率、退货率
- [ ] 欢迎流、弃购流、浏览弃置流、首购后 7 天评价请求、45 天复购提醒全部上线
- [ ] Cookie 横幅在欧盟默认拒绝非必要追踪，符合 GDPR
