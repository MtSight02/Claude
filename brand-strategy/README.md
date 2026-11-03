# DTC 珠宝品牌方案（平价时尚耳钉 · 美国 + 欧盟）

**总报告**：[`REPORT.md`](REPORT.md)（由各分文件自动合成，修改分文件后运行 `python3 scripts/build_report.py` 重新生成）
**推荐方案**：Finch & Flare → 首页样稿 [`site/index.html`](site/index.html)（纯 HTML + CSS，浏览器直接打开）

## 目录结构

```
brand-strategy/
├── 00-shared/                    共用底稿（所有方案的统一口径）
│   ├── 01-brief-and-rules.md     品牌信息、文案红线、首发 SKU 与定价基线、成本假设、合规清单
│   ├── 02-competitor-landscape.md 11 个竞品底表（不确定数据标"未核实"）
│   ├── 03-finance-model.md       三档启动预算、单件成本、单笔订单贡献利润
│   └── unit-economics-template.csv 可导入表格的财务模板（含公式）
├── finch-and-flare/              方案 A（推荐）
├── wren-and-wink/                方案 B
├── lark-and-luce/                方案 C
│   ├── 01-positioning.md         品牌定位
│   ├── 02-competitors.md         竞品分析与差异点
│   ├── 03-brand-identity.md      品牌形象（logo、配色、字体、摄影、包装）
│   ├── 04-voice.md               品牌语气、tagline、产品详情页、About 页
│   ├── 05-product-line.md        产品线与 6 个月上新节奏
│   ├── 06-marketing.md           90 天计划、内容、达人、广告、邮件、节日日历
│   ├── 07-website.md             网站审美、首页线框、产品页、Shopify 主题与 App
│   └── 08-budget-finance.md      启动预算与毛利测算
├── 09-comparison.md              三方案对比与推荐
├── 10-bold-concept.md            大胆版方向：Steel & Spark
├── site/index.html               Finch & Flare 首页样稿
├── scripts/build_report.py       合成总报告脚本
└── REPORT.md                     总报告
```

## 全局约定

- 材质统一写 **316L stainless steel**，所有对外文案不出现钛材质相关说法（见简报文案红线第 1 条，提交前已全目录检索确认）。
- 竞品价格、域名、商标可用性、供应商成本等**均标注"未核实"**，落地前需逐项复核。
