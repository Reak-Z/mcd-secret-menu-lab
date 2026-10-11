#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""麦门隐藏菜单实验室 · 社交传播物料生成器

生成：
1. cover.png      —— 小红书封面 / 项目海报（1080×1440）
2. all_cards.png  —— 14 张配方卡合集图（1080×1440 网格）

用法：
    python tools/make_social_poster.py [输出目录，默认 assets/social]

依赖：
    pip install pillow
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

from emblem import draw_emblem

try:
    import qrcode
except ImportError:  # qrcode 未安装时自动跳过二维码
    qrcode = None

QUIZ_URL = "https://reak-z.github.io/mcd-secret-menu-lab/quiz/"

RED = (218, 41, 28)
YELLOW = (255, 199, 44)
WHITE = (255, 255, 255)
CREAM = (255, 248, 235)
DARK = (45, 45, 45)
GRAY = (130, 130, 130)

W, H = 1080, 1440

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


def _rounded(d, box, radius, fill):
    try:
        d.rounded_rectangle(box, radius=radius, fill=fill)
    except AttributeError:  # noqa: BLE001
        d.rectangle(box, fill=fill)


def make_cover(out_path):
    img = Image.new("RGB", (W, H), RED)
    d = ImageDraw.Draw(img)

    # 顶部标签
    tag = "2026 麦当劳程序员创意开发大赛 · 参赛作品"
    f_tag = load_font(30)
    tw = d.textlength(tag, font=f_tag)
    _rounded(d, ((W - tw) / 2 - 30, 64, (W + tw) / 2 + 30, 64 + 64), 32, YELLOW)
    d.text(((W - tw) / 2, 74), tag, font=f_tag, fill=RED)

    # 主标题
    d.text((90, 190), "麦当劳隐藏吃法", font=load_font(108), fill=WHITE)
    d.text((90, 320), "被我做成了 AI", font=load_font(108), fill=WHITE)

    # 副标题
    d.text((92, 462), "省钱 × 健康 × 好吃 × 创意", font=load_font(46), fill=YELLOW)

    # 中间白卡
    _rounded(d, (70, 570, W - 70, 1180), 40, WHITE)
    x = 130
    y = 630
    d.text((x, y), "实测配方精选", font=load_font(40), fill=RED)
    y += 78
    rows = [
        ("薯条蘸麦旋风", "¥30.0"),
        ("冰火小圆子派", "¥10.0"),
        ("芝士瀑布薯条", "¥17.5"),
        ("红茶雪顶", "¥14.5"),
        ("焦香撞冰", "¥28.5"),
        ("还有 9 个配方等你解锁", ""),
    ]
    for name, price in rows:
        d.text((x, y), "● " + name, font=load_font(42), fill=DARK)
        if price:
            pw = d.textlength(price, font=load_font(42))
            d.text((W - 130 - pw, y), price, font=load_font(42), fill=RED)
        y += 66
    y += 10
    d.text((x, y), "全部价格经麦当劳 MCP 实时核验 · 四维评分见配方卡", font=load_font(30), fill=(150, 150, 150))

    # 底部
    d.text((90, H - 190), "说一句话，AI 帮你发明专属吃法", font=load_font(42), fill=CREAM)
    draw_emblem(img, 84, H - 132, 78)
    d.text((180, H - 122), "麦门隐藏菜单实验室", font=load_font(48), fill=YELLOW)

    img.save(out_path, "PNG")
    return out_path


def _center_text(d, y, text, font, fill):
    w = d.textlength(text, font=font)
    d.text(((W - w) / 2, y), text, font=font, fill=fill)


def make_quiz_cover_social(out_path):
    """人格测试反差型封面（社媒直发版·零外链）：大问号 + 6 人格环绕"""
    import math

    img = Image.new("RGB", (W, H), RED)
    d = ImageDraw.Draw(img)

    tag = "6 型人格 · 测完再点单"
    f_tag = load_font(32)
    tw = d.textlength(tag, font=f_tag)
    _rounded(d, ((W - tw) / 2 - 34, 70, (W + tw) / 2 + 34, 140), 35, YELLOW)
    d.text(((W - tw) / 2, 82), tag, font=f_tag, fill=RED)

    _center_text(d, 185, "你是哪种", load_font(100), WHITE)
    _center_text(d, 310, "麦门人格？", load_font(100), WHITE)
    _center_text(d, 455, "隐藏吃法 × 人格测试", load_font(42), YELLOW)

    cx, cy = W // 2, 915
    d.ellipse((cx - 185, cy - 185, cx + 185, cy + 185), fill=YELLOW)
    qf = load_font(260)
    qw = d.textlength("?", font=qf)
    d.text((cx - qw / 2, cy - 175), "?", font=qf, fill=RED)

    names = ["甜系", "咸香", "冰火", "轻享", "复古", "省钱"]
    for i, name in enumerate(names):
        ang = math.radians(90 - i * 60)
        sx = cx + int(300 * math.cos(ang))
        sy = cy - int(300 * math.sin(ang))
        r = 80
        fill = WHITE if i % 2 == 0 else YELLOW
        d.ellipse((sx - r, sy - r, sx + r, sy + r), fill=fill)
        f = load_font(40)
        nw = d.textlength(name, font=f)
        d.text((sx - nw / 2, sy - 27), name, font=f, fill=RED)

    _center_text(d, 1330, "14 种隐藏吃法等你解锁", load_font(40), CREAM)

    img.save(out_path, "PNG")
    return out_path


def make_quiz_cover(out_path, social=False):
    """人格测试主视觉（小红书封面用）：6 型人格 + 扫码即玩"""
    img = Image.new("RGB", (W, H), RED)
    d = ImageDraw.Draw(img)

    tag = "6 道题 · 30 秒 · 零门槛"
    f_tag = load_font(30)
    tw = d.textlength(tag, font=f_tag)
    _rounded(d, ((W - tw) / 2 - 30, 64, (W + tw) / 2 + 30, 64 + 64), 32, YELLOW)
    d.text(((W - tw) / 2, 74), tag, font=f_tag, fill=RED)

    d.text((90, 178), "麦当劳隐藏吃法", font=load_font(92), fill=WHITE)
    d.text((90, 292), "人格测试", font=load_font(92), fill=WHITE)
    d.text((92, 428), "测出你是哪种隐藏吃法玩家", font=load_font(44), fill=YELLOW)

    _rounded(d, (70, 530, W - 70, 1140), 40, WHITE)
    x, y = 130, 592
    d.text((x, y), "6 种人格，你是哪一种？", font=load_font(36), fill=RED)
    y += 70
    rows = [
        ("甜系炼金师", "万物皆可蘸冰淇淋"),
        ("咸香掌门", "芝士就是力量"),
        ("冰火玩家", "一半冰一半热才叫爽"),
        ("轻享派", "好吃也要无负担"),
        ("复古考古家", "经典流传二十年"),
        ("省钱战术家", "十块钱吃到仪式感"),
    ]
    for name, tagline in rows:
        d.text((x, y), "◆ " + name, font=load_font(38), fill=DARK)
        tw2 = d.textlength(tagline, font=load_font(28))
        d.text((W - 130 - tw2, y + 6), tagline, font=load_font(28), fill=GRAY)
        y += 66

    if not social and qrcode is not None:
        qr = qrcode.make(QUIZ_URL).convert("RGB").resize((170, 170))
        img.paste(qr, (90, H - 246))
    if social:
        # 社媒清洁版：无二维码、无外链文字（防站外导流判定）
        _center_text(d, H - 232, "6 型人格 · 你是哪一种？", load_font(46), WHITE)
        _center_text(d, H - 168, "测完匹配你的专属配方卡", load_font(28), CREAM)
    else:
        d.text((292, H - 238), "扫码开始测试", font=load_font(46), fill=WHITE)
        d.text((294, H - 176), "测完匹配你的专属配方卡", font=load_font(28), fill=CREAM)
        draw_emblem(img, W - 240, H - 216, 108)

    img.save(out_path, "PNG")
    return out_path


def make_cards_grid(cards_dir, out_path):
    files = sorted(f for f in os.listdir(cards_dir)
                   if f.startswith("card_") and f.endswith(".png") and "015" not in f)  # 排除隐藏彩蛋卡
    gap = 22
    cols = 4
    thumb_w = (W - gap * (cols + 1)) // cols
    thumb_h = int(thumb_w * 1350 / 1080)
    rows = (len(files) + cols - 1) // cols
    header = 130
    canvas_h = header + rows * (thumb_h + gap) + gap

    img = Image.new("RGB", (W, canvas_h), (250, 248, 245))
    d = ImageDraw.Draw(img)
    d.text((44, 36), "◆ 麦门隐藏菜单实验室 · 配方全家福", font=load_font(42), fill=RED)
    d.text((44, 92), "全部实测核价 · 2026-10-10", font=load_font(28), fill=(150, 150, 150))

    for i, f in enumerate(files):
        r, c = divmod(i, cols)
        x = gap + c * (thumb_w + gap)
        y = header + gap + r * (thumb_h + gap)
        thumb = Image.open(os.path.join(cards_dir, f)).resize((thumb_w, thumb_h), Image.LANCZOS)
        img.paste(thumb, (x, y))

    img.save(out_path, "PNG")
    return out_path


def main():
    import argparse

    ap = argparse.ArgumentParser(description="社交物料生成器")
    ap.add_argument("outdir", nargs="?", default=None, help="输出目录（默认 assets/social）")
    ap.add_argument("--social", action="store_true", help="同时生成社媒清洁版（反差封面/人格总览/合集，全部无码）")
    ap.add_argument("--noscan-cards", default=None, help="无码配方卡目录（用于社媒合集图）")
    args = ap.parse_args()

    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out_dir = args.outdir or os.path.join(base, "assets", "social")
    os.makedirs(out_dir, exist_ok=True)

    p1 = make_cover(os.path.join(out_dir, "cover.png"))
    print("生成:", p1)
    p1b = make_quiz_cover(os.path.join(out_dir, "cover_quiz.png"))
    print("生成:", p1b)
    p2 = make_cards_grid(os.path.join(base, "assets", "cards"), os.path.join(out_dir, "all_cards.png"))
    print("生成:", p2)

    if args.social:
        ps1 = make_quiz_cover_social(os.path.join(out_dir, "cover_persona.png"))
        print("生成(社媒):", ps1)
        ps2 = make_quiz_cover(os.path.join(out_dir, "cover_quiz_noscan.png"), social=True)
        print("生成(社媒):", ps2)
        if args.noscan_cards:
            ps3 = make_cards_grid(args.noscan_cards, os.path.join(out_dir, "all_cards_noscan.png"))
            print("生成(社媒):", ps3)


if __name__ == "__main__":
    main()
