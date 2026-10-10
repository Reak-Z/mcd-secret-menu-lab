# 🛠 tools/ 脚本说明

本目录包含项目的全部可运行脚本。依赖：`pip install -r requirements.txt`（Pillow + qrcode；`mcd_verify.py` 与 `diy_ranking.py` 仅用标准库，无需安装任何依赖）。

| 脚本 | 用途 | 用法 |
|---|---|---|
| `mcd_verify.py` | **独立核验脚本**：命令行直接核验配方（实时价格 + 官方营养 + 健康分级 + 四维预评分），**无需 WorkBuddy** | `python tools/mcd_verify.py verify 4810 9900008754 --store 1410005` |
| `install.py` | 一键安装 Skill 到本机（自动探测 WorkBuddy / Claude Code 技能目录） | `python tools/install.py` |
| `diy_ranking.py` | 扫描「DIY配方」标签的 Issue，按反应数生成 `DIY_RANKING.md`（由 GitHub Actions 每日自动调用） | `python tools/diy_ranking.py --token <GITHUB_TOKEN>` |
| `daily_recipe.py` | 「今日隐藏吃法」每日确定性轮换（更新 README 标记区块） | `python tools/daily_recipe.py` |
| `emblem.py` | 绘制项目原创标识（烧瓶+薯条），导出 `assets/emblem.png` | `python tools/emblem.py` |
| `make_recipe_card.py` | 批量生成 14 张配方卡 + 1 张隐藏彩蛋卡（1080×1350，含四维评分） | `python tools/make_recipe_card.py` |
| `make_demo_gif.py` | 生成对话演示动画 `assets/demo.gif` | `python tools/make_demo_gif.py` |
| `make_social_poster.py` | 生成社交物料（封面海报 + 配方合集图，自动排除彩蛋卡） | `python tools/make_social_poster.py` |
| `make_icons.py` | 生成 PWA 图标（192/512，源自项目标识） | `python tools/make_icons.py` |
| `test_gallery.js` | 画廊页运行时测试：Node 桩化 DOM，验证图鉴全流程（17 项断言，需 Node） | `node tools/test_gallery.js` |

## 说明

- 字体依赖：脚本会自动探测系统 CJK 字体（Windows 微软雅黑 / macOS PingFang / Linux Noto），无需手动配置
- 所有图片产物输出到 `assets/` 对应子目录
- 生成的 `assets/demo_preview.png` 为检查用中间产物，已被 .gitignore 忽略
