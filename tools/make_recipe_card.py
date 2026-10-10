#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""麦门隐藏菜单实验室 · 配方卡生成器

把配方数据渲染成 1080x1350 的可分享「配方卡」图片（适合发社交媒体 / 放 README）。

用法：
    python tools/make_recipe_card.py [输出目录，默认 assets/cards]

依赖：
    pip install pillow
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

# ---------- 品牌色 ----------
RED = (218, 41, 28)        # 麦当劳红
YELLOW = (255, 199, 44)    # 麦当劳黄
DARK = (45, 45, 45)
GRAY = (130, 130, 130)
LIGHT = (228, 228, 228)
WHITE = (255, 255, 255)
CREAM = (255, 248, 235)

W, H = 1080, 1350

FONT_CANDIDATES = [
    r"C:\Windows\Fonts\msyhbd.ttc",
    r"C:\Windows\Fonts\msyh.ttc",
    r"C:\Windows\Fonts\simhei.ttf",
    "/System/Library/Fonts/PingFang.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
]


def load_font(size):
    for p in FONT_CANDIDATES:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:  # noqa: BLE001
                continue
    return ImageFont.load_default()


# ---------- 配方数据（价格与营养均经麦当劳 MCP 实测核验，2026-10-10） ----------
RECIPES = [
    {"no": "#001", "name": "薯条蘸麦旋风", "price": "¥30.00", "diff": "★☆☆",
     "items": [("中薯条", "¥14.5"), ("经典麦旋风", "¥15.5")],
     "steps": ["薯条趁热蘸麦旋风", "趁冰火交替时入口"],
     "flavor": "咸甜交锋 · 脆软碰撞", "kcal": "约 555 kcal"},
    {"no": "#002", "name": "派上浇冰", "price": "¥20.50", "diff": "★☆☆",
     "items": [("派（香芋派）", "¥8.0"), ("新地（朱古力）", "¥12.5")],
     "steps": ["派掰成两半", "用勺把新地浇上去，挖着吃"],
     "flavor": "热派酥脆 · 冰奶滑顺", "kcal": "约 514 kcal"},
    {"no": "#003", "name": "雪顶可乐", "price": "¥14.50", "diff": "★☆☆",
     "items": [("中杯可乐", "¥9.5"), ("圆筒冰淇淋", "¥5.0")],
     "steps": ["可乐先喝掉两口", "圆筒倒扣进去，等 30 秒"],
     "flavor": "气泡冲击 · 奶香雪崩", "kcal": "约 240 kcal"},
    {"no": "#004", "name": "芝士瀑布薯条", "price": "¥17.50", "diff": "★☆☆",
     "items": [("中薯条", "¥14.5"), ("韩式烟熏芝士风味酱", "¥3.0")],
     "steps": ["薯条拆开铺平", "芝士酱整盒淋上去"],
     "flavor": "烟熏芝士 · 脆滑双杀", "kcal": "289 kcal + 酱料"},
    {"no": "#005", "name": "冰火小圆子派", "price": "¥10.00", "diff": "★☆☆",
     "items": [("黑洋酥小圆子风味派", "¥5.0"), ("圆筒冰淇淋", "¥5.0")],
     "steps": ["派掰开", "圆筒整支扣上，30 秒内吃完"],
     "flavor": "热黑洋酥 · 冰奶浆", "kcal": "约 325 kcal"},
    {"no": "#006", "name": "双酱鸡块", "price": "¥20.00", "diff": "★☆☆",
     "items": [("麦乐鸡5块", "¥14.0"), ("韩式烟熏芝士酱", "¥3.0"), ("北美招牌牧场酱", "¥3.0")],
     "steps": ["两盒酱按 1:1 搅匀", "鸡块蘸着吃"],
     "flavor": "复合咸香 · 双酱合璧", "kcal": "213 kcal + 酱料"},
    {"no": "#007", "name": "早餐王牌", "price": "¥30.50", "diff": "★☆☆",
     "items": [("枫糖厚松饼猪柳蛋堡", "¥22.0"), ("脆薯饼", "¥8.5")],
     "steps": ["脆薯饼直接塞进汉堡", "压紧，一口咬下"],
     "flavor": "枫糖咸甜 · 三层咔嚓", "kcal": "146 kcal + 汉堡"},
    {"no": "#008", "name": "酸甜脆薯", "price": "¥14.50", "diff": "★☆☆",
     "items": [("中薯条", "¥14.5"), ("番茄酱 + 白糖（自助台）", "免费")],
     "steps": ["番茄酱撒糖搅匀", "蘸着吃"],
     "flavor": "糖醋提亮 · 酸甜脆", "kcal": "289 kcal"},
    {"no": "#009", "name": "雪顶麦炫酷", "price": "¥17.50", "diff": "★☆☆",
     "items": [("阳光橙麦炫酷", "¥12.5"), ("圆筒冰淇淋", "¥5.0")],
     "steps": ["喝掉 1/3", "圆筒倒扣，融一半时喝"],
     "flavor": "橙味气泡 · 奶香收尾", "kcal": "约 321 kcal"},
    {"no": "#010", "name": "麦旋风双拼", "price": "¥20.50", "diff": "★☆☆",
     "items": [("经典麦旋风", "¥15.5"), ("黑洋酥小圆子风味派", "¥5.0")],
     "steps": ["派掰碎撒进麦旋风", "搅两下，开吃"],
     "flavor": "软脆交织 · 一口两吃", "kcal": "约 500 kcal"},
]


def _rounded(d, box, radius, fill):
    try:
        d.rounded_rectangle(box, radius=radius, fill=fill)
    except AttributeError:  # 兼容老版本 Pillow
        d.rectangle(box, fill=fill)


def make_card(r, out_path):
    img = Image.new("RGB", (W, H), RED)
    d = ImageDraw.Draw(img)

    # ===== 顶部品牌区 =====
    d.text((64, 58), "麦门隐藏菜单实验室", font=load_font(44), fill=YELLOW)
    d.text((64, 118), "用官方食材，炼出你的专属吃法", font=load_font(26), fill=CREAM)

    # ===== 白色主卡片 =====
    _rounded(d, (60, 190, W - 60, H - 60), 40, WHITE)

    x = 110
    y = 240
    # 编号 + 难度
    d.text((x, y), "配方卡 " + r["no"], font=load_font(28), fill=GRAY)
    w_diff = d.textlength("难度 " + r["diff"], font=load_font(28))
    d.text((W - 110 - w_diff, y), "难度 " + r["diff"], font=load_font(28), fill=GRAY)
    y += 52

    # 配方名
    d.text((x, y), r["name"], font=load_font(76), fill=DARK)
    y += 120

    # 价格徽章
    badge_text = "实测总价  " + r["price"]
    f_badge = load_font(42)
    tw = d.textlength(badge_text, font=f_badge)
    _rounded(d, (x, y, x + tw + 80, y + 84), 42, YELLOW)
    d.text((x + 40, y + 16), badge_text, font=f_badge, fill=RED)
    y += 84 + 44

    # 分割线
    d.line((x, y, W - 110, y), fill=LIGHT, width=2)
    y += 36

    # ===== 配料 =====
    d.text((x, y), "配料清单", font=load_font(34), fill=RED)
    y += 58
    for name, price in r["items"]:
        d.text((x, y), "· " + name, font=load_font(36), fill=DARK)
        pw = d.textlength(price, font=load_font(36))
        d.text((W - 110 - pw, y), price, font=load_font(36), fill=GRAY)
        y += 56
    y += 18
    d.line((x, y, W - 110, y), fill=LIGHT, width=2)
    y += 36

    # ===== 组装 =====
    d.text((x, y), "组装步骤", font=load_font(34), fill=RED)
    y += 58
    for i, s in enumerate(r["steps"], 1):
        d.text((x, y), f"{i}. {s}", font=load_font(36), fill=DARK)
        y += 56
    y += 18
    d.line((x, y, W - 110, y), fill=LIGHT, width=2)
    y += 36

    # ===== 风味 / 热量 =====
    d.text((x, y), "风味  " + r["flavor"], font=load_font(34), fill=DARK)
    y += 56
    d.text((x, y), "热量  " + r["kcal"], font=load_font(34), fill=DARK)
    y += 80

    # 底部注脚
    d.text((x, H - 150), "价格经麦当劳 MCP 实时核验 · 2026-10-10 · 福州", font=load_font(24), fill=GRAY)
    d.text((x, H - 112), "仅供创意参考 · 非麦当劳官方产品", font=load_font(24), fill=GRAY)

    img.save(out_path, "PNG")
    return out_path


def main():
    out_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "cards")
    os.makedirs(out_dir, exist_ok=True)
    for r in RECIPES:
        p = os.path.join(out_dir, "card_%s.png" % r["no"].lstrip("#"))
        make_card(r, p)
        print("生成:", p)
    print("完成，共 %d 张" % len(RECIPES))


if __name__ == "__main__":
    main()
