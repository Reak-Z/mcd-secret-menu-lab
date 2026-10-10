#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""麦门隐藏菜单实验室 · 今日隐藏吃法（每日确定性轮换）

按日期把 14 个配方做确定性轮换（本地与 CI 一致），
更新 README.md 中 <!-- DAILY-RECIPE --> 标记区块，并输出当日配方。

用法：
    python tools/daily_recipe.py           # 更新 README
    python tools/daily_recipe.py --print   # 仅打印今日配方（不写文件）
"""
import argparse
import os
import re
from datetime import date

EPOCH = date(1970, 1, 1)  # 与浏览器端 (days since epoch) 对齐

# (编号, 名称, 价格, 健康分级, 点单话术)
RECIPES = [
    ("#001", "薯条蘸麦旋风", "¥30.00", "约 555 kcal · 大满足", "点一份中薯条 + 一份经典麦旋风，趁热蘸着吃"),
    ("#002", "派上浇冰", "¥20.50", "约 514 kcal · 大满足", "点一个派（要香芋派）+ 一份新地，掰开派浇上新地挖着吃"),
    ("#003", "雪顶可乐", "¥14.50", "约 240 kcal · 轻享", "点中杯可乐 + 一个圆筒冰淇淋，喝两口后把圆筒倒扣进去"),
    ("#004", "芝士瀑布薯条", "¥17.50", "289 kcal + 酱料 · 适中", "点中薯条 + 一盒韩式烟熏芝士风味酱，把酱淋在薯条上"),
    ("#005", "冰火小圆子派", "¥10.00", "约 325 kcal · 适中", "点一个黑洋酥小圆子风味派 + 一个圆筒，掰开派扣上圆筒"),
    ("#006", "双酱鸡块", "¥20.00", "213 kcal + 酱料 · 轻享", "点 5 块麦乐鸡 + 烟熏芝士酱 + 招牌牧场酱，两盒酱 1:1 搅匀蘸"),
    ("#007", "早餐王牌", "¥30.50", "约 533 kcal · 大满足", "点一个枫糖风味厚松饼猪柳蛋堡 + 一块脆薯饼，薯饼塞进汉堡"),
    ("#008", "酸甜脆薯", "¥14.50", "289 kcal · 轻享", "点中薯条，自助台拿番茄酱×2 + 糖包×1，搅匀蘸食"),
    ("#009", "雪顶麦炫酷", "¥17.50", "约 321 kcal · 适中", "点一杯阳光橙麦炫酷 + 一个圆筒，喝掉 1/3 后倒扣圆筒"),
    ("#010", "麦旋风双拼", "¥20.50", "约 498 kcal · 适中", "点一份经典麦旋风 + 一个黑洋酥小圆子派，派掰碎拌进去"),
    ("#011", "星星撞薯", "¥31.00", "约 555 kcal · 大满足", "点一份泷盐星星麦旋风 + 一份中薯条，薯条裹满星星粒"),
    ("#012", "扭扭芝士塔", "¥19.00", "约 280 kcal · 适中", "点一份月下相思扭扭薯 + 一盒烟熏芝士酱，酱淋满拉着丝吃"),
    ("#013", "红茶雪顶", "¥14.50", "约 178 kcal · 轻享", "点一杯阳光柠檬红茶 + 一个圆筒，喝两口后倒扣进去"),
    ("#014", "焦香撞冰", "¥28.50", "约 474 kcal · 适中", "点一份薄皮焦香V翅 + 一份新地，辣翅与冰新地交替吃"),
]

START = "<!-- DAILY-RECIPE:START -->"
END = "<!-- DAILY-RECIPE:END -->"


def today_recipe():
    """按日期确定性选择今日配方（与网页端算法一致：days-since-epoch % 14）。"""
    idx = (date.today() - EPOCH).days % len(RECIPES)
    return idx, RECIPES[idx]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--print", action="store_true", dest="print_only", help="仅打印今日配方")
    args = ap.parse_args()

    idx, (no, name, price, tier, order) = today_recipe()
    text = "%s %s %s（%s）—— %s" % (no, name, price, tier, order)
    print("今日配方[%d/%d]: %s" % (idx + 1, len(RECIPES), text))
    if args.print_only:
        return

    readme = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "README.md")
    with open(readme, encoding="utf-8") as f:
        t = f.read()
    if START not in t or END not in t:
        print("README 缺少标记区块，跳过更新")
        return

    day = date.today().strftime("%m-%d")
    block = ("%s\n🍟 **今日隐藏吃法（%s）**：%s %s %s（%s）—— %s\n%s"
             % (START, day, no, name, price, tier, order, END))
    t2 = re.sub(re.escape(START) + r".*?" + re.escape(END), block, t, flags=re.S)
    if t2 == t:
        print("内容无变化")
        return
    with open(readme, "w", encoding="utf-8") as f:
        f.write(t2)
    print("README 已更新")


if __name__ == "__main__":
    main()
