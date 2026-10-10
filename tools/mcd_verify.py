#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""麦门隐藏菜单实验室 · 独立核验脚本（无需 WorkBuddy）

在命令行直接调用麦当劳 MCP 核验任意配方：实时价格 + 官方营养 + 健康分级 + 四维预评分。

用法：
    # 1) 设置 Token（从 open.mcd.cn/mcp 申请，控制台激活后复制）
    export MCD_MCP_TOKEN=xxx         # macOS / Linux
    set MCD_MCP_TOKEN=xxx            # Windows CMD
    $env:MCD_MCP_TOKEN="xxx"         # Windows PowerShell

    # 2) 找门店（拿 storeCode）
    python tools/mcd_verify.py stores --city 福州 --keyword 五四路

    # 3) 搜索餐品（拿 productCode）
    python tools/mcd_verify.py search 薯条 --store 1410005

    # 4) 核验组合（productCode 列表，可用 code:数量 指定数量）
    python tools/mcd_verify.py verify 4810 9900008754 --store 1410005

依赖：仅标准库（无需 pip 安装）
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.request

MCP_URL = "https://mcp.mcd.cn"

# 营养表名称别名（菜单名 -> 营养表名），用于提高匹配率
NUTRITION_ALIAS = {
    "经典麦旋风": "奥利奥麦旋风",
    "泷盐星星麦旋风": "奥利奥麦旋风",
    "泷愿成真麦旋风——大米风味": "奥利奥麦旋风",
    "蓝莓爆爆珠麦旋风": "奥利奥麦旋风",
    "柠檬脆脆麦旋风": "奥利奥麦旋风",
    "黑洋酥小圆子风味派": "香芋派",
    "枫糖风味厚松饼猪柳蛋堡": "猪柳蛋麦满分",
    "阳光橙麦炫酷": "麦旋酷阳光橙",
    "月下相思扭扭薯": "脆脆薯条",
    "可乐": "可乐中杯",
    "阳光柠檬红茶": "阳光柠檬红茶小杯",
}


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
            "User-Agent": "mcd-secret-menu-lab/verify",
        }
        if self.sid:
            headers["mcp-session-id"] = self.sid
        req = urllib.request.Request(MCP_URL, data=body, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=45) as resp:
                self.sid = resp.headers.get("mcp-session-id") or self.sid
                return resp.read().decode("utf-8", "ignore")
        except urllib.error.HTTPError as e:
            msg = e.read().decode("utf-8", "ignore")
            raise SystemExit("MCP 请求失败 HTTP %s：%s" % (e.code, msg[:200]))

    @staticmethod
    def _parse(text):
        if not text or not text.strip():
            return None
        t = text.lstrip()
        if t.startswith(("event:", "data:", "id:", "retry:")):
            t = "\n".join(ln[5:].strip() for ln in text.splitlines() if ln.strip().startswith("data:"))
        try:
            return json.loads(t)
        except Exception:  # noqa: BLE001
            return {"_unparsed": t[:500]}

    def initialize(self):
        self.n += 1
        r = self._parse(self._post({
            "jsonrpc": "2.0", "id": self.n, "method": "initialize",
            "params": {"protocolVersion": "2025-06-18", "capabilities": {},
                       "clientInfo": {"name": "mcd-verify", "version": "1.0"}},
        })) or {}
        if "result" not in r:
            raise SystemExit("MCP 握手失败（可能是 Token 无效，请检查 MCD_MCP_TOKEN）")
        self._post({"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}})

    def tool(self, name, args=None):
        self.n += 1
        r = self._parse(self._post({
            "jsonrpc": "2.0", "id": self.n, "method": "tools/call",
            "params": {"name": name, "arguments": args or {}},
        })) or {}
        res = r.get("result") or {}
        sc = res.get("structuredContent")
        if sc is not None:
            return sc
        # 部分工具返回文本（markdown / 内嵌 JSON）
        txt = ""
        try:
            txt = res["content"][0]["text"]
        except Exception:  # noqa: BLE001
            pass
        j = txt.find("## Original Response")
        if j >= 0:
            body = txt[j:]
            st = body.find("{")
            try:
                return json.JSONDecoder().raw_decode(body[st:])[0]
            except Exception:  # noqa: BLE001
                pass
        return {"_text": txt}


def load_nutrition(m):
    """拉取官方营养表并解析为 {名称: {kcal, protein, ...}}"""
    sc = m.tool("list-nutrition-foods")
    text = sc.get("data") if isinstance(sc, dict) else None
    if not isinstance(text, str):
        return {}
    out = {}
    for line in text.splitlines()[1:]:
        p = line.strip().split(",")
        if len(p) >= 9:
            out[p[0]] = {"kcal": float(p[3] or 0), "protein": float(p[4] or 0),
                         "fat": float(p[5] or 0), "carb": float(p[6] or 0),
                         "sodium": float(p[7] or 0)}
    return out


def match_nutrition(name, table):
    if name in table:
        return table[name], ""
    alias = NUTRITION_ALIAS.get(name)
    if alias and alias in table:
        return table[alias], "参考：" + alias
    for k, v in table.items():
        if k and (k in name or name in k):
            return v, "参考：" + k
    return None, "未收录"


def cmd_stores(m, args):
    sc = m.tool("query-nearby-stores", {"beType": 1, "searchType": 2,
                                        "city": args.city, "keyword": args.keyword})
    data = sc.get("data") if isinstance(sc, dict) else None
    if not isinstance(data, list) or not data:
        print("未找到门店。原始返回：", str(sc)[:300])
        return
    print("附近门店（%s %s）：" % (args.city, args.keyword))
    for s in data[:8]:
        print("  %s  %s  %s" % (s.get("storeCode"), s.get("storeName"), s.get("address")))


def cmd_search(m, args):
    sc = m.tool("query-meals", {"storeCode": args.store, "orderType": 1, "beType": 1})
    meals = ((sc.get("data") or {}).get("meals") or {}) if isinstance(sc, dict) else {}
    kw = args.keyword
    hits = [(c, v) for c, v in meals.items() if kw in str(v.get("name", ""))]
    if not hits:
        print("未找到含「%s」的餐品（共 %d 项）" % (kw, len(meals)))
        return
    print("匹配「%s」的餐品：" % kw)
    for c, v in hits[:30]:
        print("  %s  %-24s ¥%s" % (c, v.get("name"), v.get("currentPrice")))


def cmd_verify(m, args):
    # 1) 菜单（拿名称）
    sc = m.tool("query-meals", {"storeCode": args.store, "orderType": 1, "beType": 1})
    meals = ((sc.get("data") or {}).get("meals") or {}) if isinstance(sc, dict) else {}

    items = []
    for spec in args.items:
        if ":" in spec:
            code, qty = spec.split(":", 1)
            qty = int(qty)
        else:
            code, qty = spec, 1
        items.append({"productCode": code, "quantity": qty})

    # 2) 实时计价
    sc = m.tool("calculate-price", {"storeCode": args.store, "orderType": 1, "beType": 1,
                                    "items": items})
    d = sc.get("data") if isinstance(sc, dict) else None
    if not d or d.get("price") is None:
        print("计价失败：", str(sc)[:300])
        return

    # 3) 营养
    table = load_nutrition(m)
    tot = {"kcal": 0.0, "protein": 0.0, "fat": 0.0, "carb": 0.0, "sodium": 0.0}
    notes = []
    print("=" * 46)
    print("配方核验报告（门店 %s）" % args.store)
    print("=" * 46)
    print("配料与价格：")
    for p in d.get("productList") or []:
        name = p.get("productName")
        print("  · %-22s ¥%.2f" % (name, (p.get("subtotal") or 0) / 100))
        n, note = match_nutrition(str(name), table)
        if n:
            for k in tot:
                tot[k] += n[k] * (p.get("quantity") or 1)
        else:
            notes.append("%s：营养%s" % (name, note))
    price = d["price"] / 100
    print("  " + "-" * 24)
    print("  合计（实时核价）           ¥%.2f" % price)
    print()
    print("营养汇总（官方营养表）：")
    print("  热量 %d kcal ｜ 蛋白 %.0f g ｜ 脂肪 %.0f g ｜ 碳水 %.0f g ｜ 钠 %.0f mg"
          % (tot["kcal"], tot["protein"], tot["fat"], tot["carb"], tot["sodium"]))
    for n in notes:
        print("  注：%s" % n)
    print()

    # 4) 健康分级与四维预评分（规则见 references/nutrition-guide.md）
    kc = tot["kcal"]
    tier = "轻享（≤300 kcal）" if kc <= 300 else ("适中（300–500 kcal）" if kc <= 500 else "大满足（>500 kcal）")
    money = "★★★" if price <= 15 else ("★★☆" if price <= 25 else "★☆☆")
    health = "★★★" if kc <= 300 else ("★★☆" if kc <= 500 else "★☆☆")
    print("健康分级：%s" % tier)
    if tot["sodium"] > 600:
        print("  提示：钠 %.0f mg 偏高，当日注意控盐" % tot["sodium"])
    if tot["protein"] >= 15:
        print("  提示：蛋白 %.0f g，优质蛋白" % tot["protein"])
    if kc > 500:
        print("  建议：搭配无糖饮料 / 与朋友分享 / 当日其他餐次减量")
    print("四维预评分（自动部分）：省钱 %s ｜ 健康 %s" % (money, health))
    print("（好吃/创意需结合风味矩阵人工评估，见 references/flavor-matrix.md）")
    print("=" * 46)


def main():
    ap = argparse.ArgumentParser(description="麦门隐藏菜单实验室 · 独立核验脚本")
    ap.add_argument("--token", default=os.environ.get("MCD_MCP_TOKEN", ""),
                    help="麦当劳 MCP Token（默认读 MCD_MCP_TOKEN 环境变量）")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p1 = sub.add_parser("stores", help="按城市+关键词找门店")
    p1.add_argument("--city", required=True)
    p1.add_argument("--keyword", required=True)

    p2 = sub.add_parser("search", help="在门店菜单中搜索餐品")
    p2.add_argument("keyword")
    p2.add_argument("--store", required=True)

    p3 = sub.add_parser("verify", help="核验配方组合（productCode 列表）")
    p3.add_argument("items", nargs="+", help="productCode，可用 code:数量 指定数量")
    p3.add_argument("--store", required=True)

    args = ap.parse_args()
    if not args.token:
        print("请先设置麦当劳 MCP Token：")
        print("  export MCD_MCP_TOKEN=<你的Token>   （从 open.mcd.cn/mcp 申请）")
        print("  或使用 --token 参数")
        sys.exit(1)

    m = Mcp(args.token)
    m.initialize()
    {"stores": cmd_stores, "search": cmd_search, "verify": cmd_verify}[args.cmd](m, args)


if __name__ == "__main__":
    main()
