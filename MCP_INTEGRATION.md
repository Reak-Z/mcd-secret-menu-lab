# 🔌 MCP 集成说明

> 本文件说明「麦门隐藏菜单实验室」实际使用的麦当劳 MCP Server、Tool、调用流程与业务价值。
> 状态：v2 已实测（2026-10-10 完成 10 个配方全链路核验：菜单拉取 → 食材详情 → 实时计价 → 营养；实测记录见 [examples/live-verification-2026-10-10.md](examples/live-verification-2026-10-10.md)）

---

## 一、使用的 MCP Server

| 项目 | 值 |
|---|---|
| Server 名称 | `mcd-mcp`（麦当劳中国官方 MCP） |
| 协议 | Streamable HTTP（MCP 协议版本 2025-06-18 及之前） |
| 端点 | `https://mcp.mcd.cn` |
| 认证 | `Authorization: Bearer <MCP_TOKEN>`（Token 从 open.mcd.cn/mcp 申请） |
| 限流 | 600 次/分钟/Token（超限 429） |

## 二、使用的 Tool 与用途

| Tool | 在本项目中的用途 | 调用时机 |
|---|---|---|
| `query-nearby-stores` | 定位用户附近门店，拿到 storeCode / beCode | 模式 C（下单）或用户问"哪里有" |
| `query-meals` | **配方核验核心**：确认配方所需食材当前在售 + 拿 productCode | 模式 A / B 每次生成配方后 |
| `query-meal-detail` | 查套餐组成与可替换项（为配方做"食材拆解"） | 配方涉及套餐时 |
| `calculate-price` | **真实计价核心**：算出配方的真实总价（含可用优惠） | 每个配方输出前 |
| `list-nutrition-foods` | 为配方卡补充热量/营养信息 | 输出配方卡时 |
| `query-store-coupons` | 查当前门店可用券，提示配方可叠加的优惠 | 用户关心价格时（进阶） |
| `available-coupons` / `auto-bind-coupons` | 省钱助手：列出可领券 → **用户确认后**一键领取 | 模式 E（领券） |
| `query-my-coupons` | 检查卡包：临期券（3 天内）预警 + 高价值券推荐 | 模式 E（省钱） |
| `create-order` | 用户确认后一键下单 | 模式 C，且需用户显式确认 |
| `cancel-order` | 用户反悔时取消 | 模式 C |
| `now-time-info` | 校准当前时间（判断早餐时段等） | 配方涉及时段限定餐品时 |

## 三、核心调用流程

```
【模式 A：还原】
用户提问 → references/recipes.md 匹配配方
        → query-meals（核验食材在售 + 取 productCode）
        → calculate-price（真实总价）
        → list-nutrition-foods（营养）
        → 输出配方卡

【模式 B：创造】
用户约束 → flavor-matrix.md 生成候选组合
        → query-meals（筛掉不可购元素）
        → calculate-price（验价，超预算自动降级换料）
        → 输出"最优 + 大胆"双配方卡

【模式 C：落地】
用户确认配方 → query-nearby-stores（定门店）
           → calculate-price（复核金额）
           → 展示明细 → 【用户显式确认】→ create-order
```

## 四、业务价值

1. **让"原子能力"产生新场景**：麦当劳 MCP 开放的是菜单/计价/下单等原子能力，本身不解决"怎么搭配才好吃"的问题。本项目在其上构建了**配方知识层（风味矩阵 + 配方库）**，把原子能力组合成"创意吃法发现 → 真实核验 → 落地下单"的完整闭环。
2. **真实数据的可信输出**：所有配方价格与可购性都经过 MCP 实时核验，杜绝"网上抄来的攻略在你这儿买不到/价格对不上"的痛点。
3. **可复用的知识资产**：风味矩阵是结构化、可迭代的知识内核，社区可持续贡献配方，让项目随时间变得更强。
4. **社区化运营**：DIY 投稿（Issue 模板）+ 反应数排行榜（GitHub Actions 每日自动更新），配方库由社区持续生长。
5. **省钱闭环**：`available-coupons → auto-bind-coupons` 领券链路与配方/订单结合，实现"券后最优价"。

## 五、实战踩坑记录（2026-10-10 真实链路）

| 坑 | 结论 |
|---|---|
| `roundList` 报「服务器发生了未知的问题」 | 必须带 `round` 字段（round id，字符串），格式：`[{"round":"1","comboItemList":[{"code":"4106","quantity":1}]}]` |
| 「派」「新地」计价失败 | 它们是**可选口味**商品（派：香芋/菠萝；新地：朱古力/草莓），须先 `query-meal-detail` 拿 rounds 再组装 |
| 价格数值异常大 | 单位是**分**（`price: 3000` = ¥30.00） |
| 到店自取场景传 beCode 报错 | `orderType=1 && beType=1` 时**不要传** `beCode` |
| 营养数据解析失败 | `list-nutrition-foods` 返回**文本表格**（160 行，格式 `名称,null,kJ,kcal,蛋白,脂肪,碳水,钠,钙`），需按行解析 |
| `query-nearby-stores` 报 600058 | `keyword` 不能为空串，需传真实地名关键词 |
| 季节菜单变化 | 本季派为「黑洋酥小圆子风味派」（¥5），经典香芋派藏在「派」（¥8）的可选项里 |
| 官方已有成品 | 菜单含「咖啡阿芙佳朵 ¥15」——配方库已主动规避重复路线，改创"芝士瀑布薯条"等官方未做组合 |
| 券后计价怎么写 | `items` 附 `couponId` + `couponCode`（`query-store-coupons` 获取）；实测 ¥19.00 → 券后 ¥9.90 验证通过 |

## 六、鲁棒性设计

- 401：引导用户重新申请 Token
- 429：自动降频、减少候选配方数量
- 门店菜单差异：不同城市/门店在售餐品不同 → 每个配方强制过 `query-meals` 校验
- 价格单位：MCP 返回"分"，展示统一换算为"元"
- 数据缺失：明确标注"待核验"，绝不编造

---

*本项目为 2026 麦当劳程序员创意开发大赛参赛作品，非麦当劳官方产品。*
