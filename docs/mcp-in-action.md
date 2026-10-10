# 麦当劳 MCP 实战：从 0 到 1 做个「隐藏菜单实验室」（附 8 个踩坑记录）

> 这是一份参赛作品的技术复盘：如何用**麦当劳中国官方 MCP**（35 个工具）+ 一个**纯标准库写的迷你客户端**，把「门店 → 菜单 → 实时计价 → 营养数据」串成一条完整可用链路，并在此之上做出一个「隐藏吃法配方实验室」。
> 全部代码与实测数据已开源：<https://github.com/Reak-Z/mcd-secret-menu-lab>

---

## 0. 背景：为什么要做这个

麦当劳的菜单是「原子」的（一根薯条、一个汉堡、一支甜筒），但吃法是「无限」的。薯条蘸麦旋风、热派浇冰新地……这些在社交平台火了十几年的隐藏吃法，从来没有一个工具能回答三个最基本的问题：

1. **这家店有货吗？**（不同城市/门店菜单不同，还有季节轮换）
2. **现在要多少钱？**（价格随门店波动，网上攻略经常过期）
3. **热量多少？**（官方营养表其实有，只是没人把它和"吃法"关联）

麦当劳在 2026 年的开发者比赛中开放了官方 MCP，正好把这几个问题都解决了。下面是我们从零接通的完整过程。

## 1. 麦当劳 MCP 速览

| 项目 | 说明 |
|---|---|
| 端点 | `https://mcp.mcd.cn`（Streamable HTTP，`Authorization: Bearer <Token>`） |
| 协议 | MCP（Model Context Protocol，2025-06-18 版本） |
| 工具数 | **35 个**，覆盖：门店查询 / 菜单 / 餐品详情 / 实时计价 / 下单 / 营养数据 / 优惠券 / 积分 / 活动日历 等 |
| Token 申请 | open.mcd.cn/mcp → 手机号登录 → 控制台 → 激活 → 复制 Token |

工具命名很直白，几个核心的：

| 工具 | 作用 |
|---|---|
| `now-time-info` | 服务器时间（对时间敏感的活动判断用） |
| `query-nearby-stores` | 按城市+关键词找门店（拿 `storeCode`） |
| `query-meals` | 拉门店全量在售餐品（一次 130+ 项） |
| `query-meal-detail` | 单个餐品详情（套餐结构 / 可选口味） |
| `calculate-price` | **实时计价**（核心） |
| `list-nutrition-foods` | 官方营养表（158 项：热量/蛋白/脂肪/碳水/钠/钙） |
| `available-coupons` / `auto-bind-coupons` | 可领券 / 一键领券 |
| `query-my-coupons` / `query-store-coupons` | 卡包 / 门店可用券（券后计价的关键） |
| `create-order` | 下单（资金操作，务必用户确认） |

## 2. 一个 80 行的迷你 MCP 客户端（纯标准库）

接 MCP 不一定需要官方 SDK。为了把协议看得更清楚（也为了零依赖），我们用 Python 标准库手写了一个客户端，核心就三件事：

**MCP 握手三步**：`initialize` → 通知 `notifications/initialized` → 调用 `tools/call`。

```python
import json, urllib.request, urllib.error

MCP_URL = "https://mcp.mcd.cn"

class Mcp:
    """迷你 MCP 客户端（Streamable HTTP，仅标准库）"""

    def __init__(self, token):
        self.tok = token
        self.sid = None
        self.n = 0

    def _post(self, payload):
        body = json.dumps(payload).encode("utf-8")
        headers = {
            "Authorization": "Bearer " + self.tok,
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
        }
        if self.sid:
            headers["mcp-session-id"] = self.sid      # 会话保持
        req = urllib.request.Request(MCP_URL, data=body, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=45) as resp:
            self.sid = resp.headers.get("mcp-session-id") or self.sid
            return resp.read().decode("utf-8", "ignore")

    @staticmethod
    def _parse(text):
        """兼容 JSON 与 SSE 两种返回"""
        t = text.lstrip()
        if t.startswith(("event:", "data:", "id:", "retry:")):
            t = "\n".join(l[5:].strip() for l in text.splitlines()
                          if l.strip().startswith("data:"))
        return json.loads(t)

    def initialize(self):
        self.n += 1
        self._post({
            "jsonrpc": "2.0", "id": self.n, "method": "initialize",
            "params": {"protocolVersion": "2025-06-18", "capabilities": {},
                       "clientInfo": {"name": "mini", "version": "1.0"}},
        })
        self._post({"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}})

    def tool(self, name, args=None):
        self.n += 1
        r = self._parse(self._post({
            "jsonrpc": "2.0", "id": self.n, "method": "tools/call",
            "params": {"name": name, "arguments": args or {}},
        }))
        res = r.get("result") or {}
        return res.get("structuredContent") or res   # 部分工具结构体在 structuredContent

m = Mcp(open("token.txt").read().strip())
m.initialize()
print(m.tool("now-time-info"))
```

要点：
- **`mcp-session-id` 响应头**必须回传（会话保持），否则部分调用会 400
- `Accept` 要同时接受 `application/json` 和 `text/event-stream`（服务端可能回 SSE 格式）
- 有的工具把结果放在 `structuredContent`，有的是文本（详见踩坑 5）

## 3. 真实链路演示（可复现）

以「福州五四路省农科院店」为例，一条完整的核验链路：

```text
① query-nearby-stores  → 店：1410005（麦当劳福州五四路(省农科院)餐厅）
② query-meals          → 130 项在售（code → 名称/价格 映射）
③ calculate-price      → 薯条(4810) + 经典麦旋风(9900008754) = ¥30.00
④ list-nutrition-foods → 中薯条 289 kcal / 经典麦旋风(参考) 266 kcal
```

实测输出（2026-10-10）：

```text
$ python tools/mcd_verify.py verify 4810 9900008754 --store 1410005
==============================================
配方核验报告（门店 1410005）
==============================================
配料与价格：
  · 中薯条                    ¥14.50
  · 经典麦旋风                 ¥15.50
  ------------------------
  合计（实时核价）            ¥30.00

营养汇总（官方营养表）：
  热量 555 kcal ｜ 蛋白 9 g ｜ 脂肪 21 g ｜ 碳水 78 g ｜ 钠 281 mg

健康分级：大满足（>500 kcal）
  建议：搭配无糖饮料 / 与朋友分享 / 当日其他餐次减量
==============================================
```

这个 `mcd_verify.py` 就是我们开源仓库里的**独立核验脚本**（只依赖标准库，clone 后可零安装使用）。

## 4. 八个踩坑记录（省下你踩坑的时间）

> 全部来自真实调试过程，按"血泪指数"排序。踩坑记录同步收录于仓库 `MCP_INTEGRATION.md`。

### 坑 1：`calculate-price` 的 `roundList` 必须带 `round` 字段

套餐/可选商品的子项选择要放在 `roundList` 里，而且**必须带 `round` 字段（round id 的字符串）**：

```json
{
  "productCode": "9900008752",
  "quantity": 1,
  "roundList": [
    { "round": "1", "comboItemList": [{ "code": "4106", "quantity": 1 }] }
  ]
}
```

漏了 `round` 字段 → 直接报 **「服务器发生了未知的问题」（code 500）**——注意，这不是参数校验错误，报错信息毫无指向性，我们试了 4 种字段变体才定位到。

### 坑 2：「派」「新地」是**可选口味商品**，不能直接计价

菜单里的「派」（¥8）实际是一个"容器"，要选香芋派/菠萝派；「新地」要选朱古力/草莓。**必须先 `query-meal-detail` 拿到 rounds 结构，再组装 `roundList` 去计价**，否则同样 500。

这也解释了为什么很多人疑惑"为什么我在 App 里看到香芋派，API 里搜不到"——它藏在「派」的可选项里。

### 坑 3：到店自取场景**不要传 `beCode`**

`beCode` 只在得来速/外送/团餐场景使用。到店自取（`orderType=1 && beType=1`）传了它会直接报错——文档里写了，但很容易被"参数都传上比较保险"的直觉坑掉。

### 坑 4：价格单位是**分**

`calculate-price` 返回 `"price": 3000` 表示 **¥30.00**。第一次看到 3000 会以为是哪个套餐，其实是单位问题。展示前记得 `/100`。

### 坑 5：`list-nutrition-foods` 返回的是**文本表格**，不是 JSON

这个工具返回的是一段**多行文本**：

```text
[160]{productName,nutritionDescription,energyKj,energyKcal,protein,fat,carbohydrate,sodium,calcium}:
  猪柳麦满分,null,1288,308,16,16,24,781,213
  中薯条,null,1210,289,4,12,38,165,18
  ...
```

按行解析（`名称,null,kJ,kcal,蛋白,脂肪,碳水,钠,钙`），不要试图 `json.loads`。另外注意名称匹配：菜单名「经典麦旋风」在营养表里叫「奥利奥麦旋风」，需要做一层别名映射。

### 坑 6：`query-nearby-stores` 的 `keyword` 不能为空串

只传 `city` 不传 `keyword` → 报 **600058「城市名或者关键词不能为空」**。至少要给一个真实地名关键词（我们用的"五四路"）。

### 坑 7：菜单是"活"的，陷阱是**季节轮换**

我们实测当天（10 月上旬），菜单上的派是「黑洋酥小圆子风味派」（¥5），而经典「香芋派」（¥8）藏在「派」的可选口味里；同时发现官方已经上架了「咖啡阿芙佳朵 ¥15」——**如果我们闭门造车，就会做出和官方重复、或者已经下架的配方**。

结论：**任何输出配方的产品，都必须实时核验，不能相信任何缓存数据**。这也是我们"先核验、后出卡"原则的来源。

### 坑 8：券后计价——`couponId` + `couponCode` 附在 `items` 上

想算"券后价"，先 `query-store-coupons` 拿三件套（`couponId` + `couponCode` + 券绑定的**凭证商品码**），然后把前两者附到 `items` 里：

```json
{
  "items": [{
    "productCode": "507411",
    "quantity": 1,
    "couponId": "264B97DBE02BE6CF996AA6914151C4A9",
    "couponCode": "MCD64719501XW09108B00"
  }]
}
```

实测：冰美式 原价 ¥19.00 → 券后 **¥9.90**（`discount` 字段会返回优惠额 910 分）。
另外注意：`available-coupons` 返回的是**活动券展示列表**（不代表每张都能入卡），实际入卡以 `query-my-coupons` 为准；「买一送一」类券不在门店券列表里，适用范围以实际下单为准。

### 附赠坑：环境变量里的代理会"偷袭"你的请求

如果你的机器上设置了 `HTTP_PROXY/HTTPS_PROXY`（很多代理软件会写），Python `urllib` 会默认走代理——请求 `mcp.mcd.cn`（国内域名）时应该绕过：

```python
opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))  # 直连
```

我们排查过一次"莫名其妙的超时"，最后发现是环境代理在作怪。

## 5. 我们最终做出来的东西

把上面的链路 + 一层产品设计，做成了「**麦门隐藏菜单实验室**」：

- 🔁 **还原**：一句话调出网红隐藏吃法的配方卡（买什么/怎么组装/什么味/多少钱）
- 🧪 **创造**：报口味和预算，按"风味矩阵"现场发明新吃法（全部实时计价）
- 🥗 **四维核验**：省钱 × 健康（热量分级）× 好吃 × 创意
- 🧑🍳 **DIY**：用户投稿吃法 → 反应数排行榜（GitHub Issue + Actions 自动更新）
- 🎫 **省钱助手**：一键领券 + 临期券预警 + 券后最优价
- 🌐 在线配方画廊（手机友好）+ 命令行核验脚本 + 14 个实测配方

- 仓库：<https://github.com/Reak-Z/mcd-secret-menu-lab>
- 画廊：<https://reak-z.github.io/mcd-secret-menu-lab/>
- 人格测试：<https://reak-z.github.io/mcd-secret-menu-lab/quiz/>

## 6. 写在最后

麦当劳 MCP 是目前国内少有的"真的能跑通一整套生活服务链路"的官方 MCP——菜单、计价、下单、营养、优惠券全部可用，且数据实时。踩坑主要集中在文档细节（round 结构、场景参数、返回格式），本文的 8 条记录希望能帮你把调试时间从几天压缩到几小时。

如果这个项目对你有帮助，欢迎 Star 支持我们参赛 ⭐（2026 麦当劳程序员创意开发大赛，排名按公开 Star 数，我们承诺只做真实分享、不刷星）。也欢迎提 Issue 交流 MCP 接入问题——能复现的我们都会回。

> 本文数据核验于 2026-10-10，来源：麦当劳 MCP 实时调用。价格随城市/门店/活动变化，请以你自己的实时核验为准。
