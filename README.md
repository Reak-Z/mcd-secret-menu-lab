# 🔮 麦门隐藏菜单实验室

<img src="assets/emblem.png" width="110" align="right" alt="项目标识：烧瓶薯条">

> **14 个实测配方 · 最低 ¥10 · 全部真实核价** —— 说一句话，AI 帮你还原全网隐藏吃法、发明专属配方。
> 省钱 × 健康 × 好吃 × 创意，一个四维配方实验室。
>
> **⭐ 本项目正在参加 [2026 麦当劳程序员创意开发大赛](https://github.com/M-China/mcd-developer-innovation-challenge) —— 喜欢的话，[点一颗 Star 支持我们](https://github.com/Reak-Z/mcd-secret-menu-lab) ⭐**

[![Stars](https://img.shields.io/github/stars/Reak-Z/mcd-secret-menu-lab?style=social)](https://github.com/Reak-Z/mcd-secret-menu-lab)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![MCP](https://img.shields.io/badge/MCP-McDonald's%20China-DA291C)](https://github.com/M-China/mcd-mcp-server)
[![Powered by WorkBuddy](https://img.shields.io/badge/Powered%20by-WorkBuddy-2F6BFF)](https://www.workbuddy.cn/)

**基于 [麦当劳中国官方 MCP](https://github.com/M-China/mcd-mcp-server) 开发 · 使用 [WorkBuddy](https://www.workbuddy.cn/) 构建**

> 🍟 **只想看配方？** → 🌐 [在线配方画廊](https://reak-z.github.io/mcd-secret-menu-lab/)（手机友好）｜ 🎯 [测测隐藏吃法人格](https://reak-z.github.io/mcd-secret-menu-lab/quiz/) ｜ [14 个实测配方文档](references/recipes.md) ｜ 🎬 见下方[在线演示](#-在线演示) ｜ 🧪 [投稿你的 DIY](DIY_RANKING.md)
>
> 📝 **开发者**：想接入麦当劳 MCP？看我们的实战复盘 → [《MCP 集成实战 + 8 个踩坑记录》](docs/mcp-in-action.md)（附 80 行迷你客户端代码）

<!-- DAILY-RECIPE:START -->
🍟 **今日隐藏吃法（10-13）**：#006 双酱鸡块 ¥20.00（213 kcal + 酱料 · 轻享）—— 点 5 块麦乐鸡 + 烟熏芝士酱 + 招牌牧场酱，两盒酱 1:1 搅匀蘸
<!-- DAILY-RECIPE:END -->

---

## 🍟 这是什么？

麦当劳的菜单是「原子」的，但吃法是「无限」的。

薯条蘸麦旋风、香芋派浇新地、甜筒坠入可乐…… 这些在社交平台被千万人点赞的**隐藏吃法**，从来没有人帮你系统地整理、验证和再创造。

**麦门隐藏菜单实验室** 是一个 AI Skill，做六件事：

| 模式 | 你说 | 它做 |
|---|---|---|
| 🔁 **还原** | “薯条蘸麦旋风怎么做？” | 调出网红隐藏吃法：买什么、怎么组装、什么味、几块钱 |
| 🧪 **创造** | “20 元以内、甜咸双杀的隐藏吃法” | 配方引擎现场发明新吃法，风味矩阵保证好吃逻辑 |
| 💰 **验价** | （自动） | 真实调用麦当劳 MCP 计价，写清楚花多少钱，不是瞎估 |
| 🛒 **落地** | “就按这个下单” | 生成到店组装指引，或经你确认后一键下单 |
| 🧑🍳 **DIY 核验** | “我有个吃法：薯条+新地+奥利奥碎” | 核验食材可购 + 实时计价 + 风味评估，生成你的专属配方卡 |
| 🎫 **省钱助手** | “帮我领券 / 有什么券能用” | 一键领券（需你确认）+ 临期券预警 + 券后最优价（实测：¥19 冰美式 → 券后 ¥9.90） |

每个配方都会生成一张可分享的 **「配方卡」** 📸 —— 并且都经过**四维核验**：💰省钱（实时计价）· 🥗健康（热量分级 + 钠提示）· 😋好吃（风味矩阵）· 🎨创意（原创度）。评分规则见 [nutrition-guide.md](references/nutrition-guide.md)。

---

## 🎬 在线演示

![演示动画](assets/demo.gif)

---

## 🧪 配方卡长什么样

对话里实时输出的 Markdown 版：

```
╭─ 配方卡 #003 ──────────────────╮
│ 🥤🍦 雪顶可乐（McFloat）        │
│ 难度 ★☆☆   实测总价 ¥14.50     │
├────────────────────────────────┤
│ 配料清单                        │
│ · 中杯可乐           ¥9.5       │
│ · 圆筒冰淇淋         ¥5.0       │
├────────────────────────────────┤
│ 组装                            │
│ 1. 可乐先喝掉两口               │
│ 2. 圆筒倒扣进去，等 30 秒       │
├────────────────────────────────┤
│ 风味：气泡冲击 · 奶香雪崩        │
│ 热量：约 240 kcal（官方营养表）  │
╰────────────────────────────────╯
```

还能一键生成**图片版配方卡**（1080×1350，可直接发社交媒体；右下角二维码扫码直达在线画廊）：

🌐 **在线配方画廊（手机友好）**：https://reak-z.github.io/mcd-secret-menu-lab/

<p>
<img src="assets/cards/card_001.png" width="46%">
&nbsp;
<img src="assets/cards/card_005.png" width="46%">
</p>

## 📊 真实实测（2026-10-10）

> 不是纸上谈兵：以下价格全部由麦当劳 MCP `calculate-price` **实时核验**（门店：福州五四路省农科院店）

| 配方 | 配料 | 实测总价 |
|---|---|---|
| #001 薯条蘸麦旋风 | 中薯条 + 经典麦旋风 | **¥30.00** |
| #002 派上浇冰 | 派（香芋派）+ 新地 | **¥20.50** |
| #003 雪顶可乐 | 可乐 + 圆筒冰淇淋 | **¥14.50** |
| #004 芝士瀑布薯条 | 中薯条 + 韩式烟熏芝士酱 | **¥17.50** |
| #005 冰火小圆子派 | 黑洋酥小圆子派 + 圆筒 | **¥10.00** |
| #006 双酱鸡块 | 麦乐鸡5块 + 双酱 | **¥20.00** |
| #007 早餐王牌 | 枫糖厚松饼猪柳蛋堡 + 脆薯饼 | **¥30.50** |
| #008 酸甜脆薯 | 中薯条（含免费番茄酱&糖） | **¥14.50** |
| #009 雪顶麦炫酷 | 阳光橙麦炫酷 + 圆筒 | **¥17.50** |
| #010 麦旋风双拼 | 经典麦旋风 + 小圆子派 | **¥20.50** |
| #011 星星撞薯 | 泷盐星星麦旋风 + 中薯条 | **¥31.00** |
| #012 扭扭芝士塔 | 扭扭薯 + 烟熏芝士酱 | **¥19.00** |
| #013 红茶雪顶 | 柠檬红茶 + 圆筒冰淇淋 | **¥14.50** |
| #014 焦香撞冰 | 薄皮焦香V翅 + 新地 | **¥28.50** |

**💳 省钱助手实测**：一键领取 5 张券入卡包；券后计价对比——冰美式 ¥19.00 → **券后 ¥9.90**（省 ¥9.10）

完整核验记录（含调用链与原始数据）：[examples/live-verification-2026-10-10.md](examples/live-verification-2026-10-10.md)

---

## 🧪 社区 DIY：你的吃法也能上榜

本实验室不只收录"网红吃法"——**你的自创吃法也能加入**：

1. 用 [DIY 投稿模板](.github/ISSUE_TEMPLATE/diy-recipe.md) 提交原创吃法（GitHub Issue）
2. 让朋友们给你的 Issue 点 👍
3. 票数越高，[DIY 吃法排行榜](DIY_RANKING.md) 名次越高（GitHub Actions **每日自动更新**）
4. 🥇 榜首配方将收录进配方库（`references/recipes.md`），**永久署名你的 ID**

---

## 🚀 快速开始

### 1. 申请麦当劳 MCP Token

前往 [open.mcd.cn/mcp](https://open.mcd.cn/mcp) → 手机号登录 → 右上角「控制台」→「激活」→ 复制 Token。

### 2. 配置 MCP 连接器（以 WorkBuddy 为例）

左侧边栏【专家·技能·连接器】→【连接器】→ 右上角【自定义连接器】→【配置 MCP】，填入 `mcp-config.example.json` 的内容并替换 `YOUR_MCP_TOKEN`。

> 其他客户端（Cursor / Cherry Studio / Trae / VSCode 等）配置方式相同，见[官方接入指南](https://github.com/M-China/mcd-mcp-server)。

### 3. 安装本 Skill

**一键安装**（自动探测 WorkBuddy / Claude Code 技能目录）：

```bash
python tools/install.py
```

或手动复制 `SKILL.md` 与 `references/` 到你的技能目录：

- **WorkBuddy**：`~/.workbuddy/skills/mcd-secret-menu-lab/`
- **Claude Code / 其他 Agent**：放入对应 skills 目录即可（SKILL.md 为通用格式）

### 4. 开聊

```
你：20 块以内，要又脆又甜的，帮我发明一个

🔮 实验室：
  ① 扫描门店菜单（130 项真实在售）
  ② 风味矩阵匹配 → 生成候选组合
  ③ calculate-price 实时计价复核 ✓

  ╭─ 配方卡 #004 芝士瀑布薯条 · 实测 ¥17.50 ╮
  ╰─ 配方卡 #008 酸甜脆薯   · 实测 ¥14.50 ╯

你：就按芝士瀑布那个下单

🔮 实验室：门店确认 → 金额复核 → 明细确认 →【等你确认】→ 下单成功
```

---

## 📁 仓库结构

```
├── SKILL.md                    # 技能主体（六大模式 + 风味矩阵 + 配方卡模板）
├── references/
│   ├── recipes.md              # 配方库 v2（实测版：真实价格 + 营养）
│   └── flavor-matrix.md        # 风味兼容性矩阵（配方引擎的知识内核）
├── tools/
│   ├── install.py              # 一键安装脚本（WorkBuddy / Claude Code）
│   ├── diy_ranking.py          # DIY 排行榜生成器（按 Issue 反应数统计）
│   ├── emblem.py               # 原创项目标识（烧瓶薯条图形，非官方 Logo）
│   ├── make_recipe_card.py     # 配方卡图片生成器（1080×1350 可分享版式）
│   ├── make_demo_gif.py        # 对话演示 GIF 生成器
│   └── make_social_poster.py   # 社交物料生成器（封面海报 + 合集图）
├── .github/
│   ├── ISSUE_TEMPLATE/diy-recipe.md   # DIY 吃法投稿模板
│   └── workflows/diy-ranking.yml      # 排行榜每日自动更新
├── DIY_RANKING.md              # 社区 DIY 吃法排行榜（自动生成）
├── assets/
│   ├── emblem.png              # 项目标识（原创图形）
│   ├── cards/                  # 生成的配方卡图片（14 张）
│   ├── social/                 # 传播物料（封面海报 + 配方合集图）
│   └── demo.gif                # 对话演示动画
├── examples/
│   └── live-verification-2026-10-10.md  # 真实链路核验记录
├── docs/
│   └── mcp-in-action.md        # MCP 集成实战指南（8 个踩坑记录 + 迷你客户端）
├── MCP_INTEGRATION.md          # MCP 工具调用流程、业务价值与踩坑记录
├── mcp-config.example.json     # 脱敏后的 MCP 配置示例（仅环境变量占位符）
├── workbuddy.md                # WorkBuddy 开发对话上下文（联动活动核验用）
├── CONTEST_DECLARATION.md      # 参赛声明（官方原文，不可修改）
└── README.md
```

---

## 🗺️ Roadmap

- [x] 配方库 v1（10 个经典隐藏吃法）
- [x] 风味兼容性矩阵 v1
- [x] **MCP 真实链路核验**（2026-10-10 完成：14 个配方全部实测计价 + 158 项营养数据）
- [x] **配方卡图片生成器**（2026-10-10：1080×1350 可分享版式，一键出图）
- [x] **对话演示 GIF**（2026-10-10：11 帧动画，183KB，见上方演示）
- [x] **社区 DIY 功能**（2026-10-10：Issue 投稿模板 + 反应数排行榜 + Actions 每日自动更新）
- [x] **省钱助手**（2026-10-10：一键领券 + 临期券预警 + 券后最优价）
- [x] **隐藏吃法人格测试**（2026-10-10：6 型人格 × 配方匹配，零门槛传播入口）
- [ ] 配方库持续扩容（欢迎投稿你的独门吃法！）

---

## 🏆 参赛信息

- 赛事：[2026 麦当劳程序员创意开发大赛](https://github.com/M-China/mcd-developer-innovation-challenge)
- 开发工具：[WorkBuddy](https://www.workbuddy.cn/)
- 参赛状态：✅ **已通过官方核验，成功参赛**（[Issue #272](https://github.com/M-China/mcd-developer-innovation-challenge/issues/272)，2026-10-10 官方确认）

---

## ❓ FAQ

**Q：没有 WorkBuddy 也能用吗？**
可以"半手动"用：14 个配方、实测价格、热量数据都写在仓库里，照着点单即可。完整体验（实时核价、现场发明新配方、DIY 核验）需要一个支持 MCP 的客户端（WorkBuddy / Claude Code / Cursor 等）。

**Q：为什么价格和我这里的不一样？**
麦当劳价格随城市/门店/时段波动。仓库里的价格是实测样本，同时提供实时核验方法——以你所在门店的 MCP 核价为准。

**Q：热量数据从哪来？**
麦当劳官方营养表（通过 MCP `list-nutrition-foods` 实时获取，158 项）。未收录的新品会标注「参考」。

**Q：这些吃法从哪来？**
经典款来自网络流传（已注明）；原创款由「风味矩阵」配方引擎发明（标注原创）。欢迎投稿你的 DIY。

**Q：为什么只做麦当劳？**
这是麦当劳官方大赛的参赛作品，规则要求只使用麦当劳品牌内容（也绝不与其他品牌对比）。

**Q：会胖吗？😅**
每个配方都有热量分级：「轻享」≤300 kcal 放心吃；「大满足」>500 kcal 建议分享或当日平衡。数据仅供参考，不构成营养建议。

## ⚠️ 声明

- 本项目为麦当劳程序员创意开发大赛参赛作品，由参赛者独立开发，**非麦当劳官方产品**
- 项目输出仅供参考，不构成医疗、营养或其他专业建议；餐品信息、价格及供应状态以麦当劳官方渠道的实时结果为准
- 下单、积分兑换等资金/权益操作均需用户显式确认后执行
- 本仓库不包含任何真实 Token，请通过官方渠道申请并妥善保管
- 项目标识为**原创图形**（烧瓶+薯条），未使用任何麦当劳注册商标；文中「麦当劳」「麦门」等字样仅作说明性引用

## 📜 License

MIT
