#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""麦门隐藏菜单实验室 · 对话演示 GIF 生成器

把一次典型的 Skill 对话渲染成逐条浮现的动画 GIF（用于 README 演示）。

用法：
    python tools/make_demo_gif.py [输出路径，默认 assets/demo.gif]

依赖：
    pip install pillow
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

from emblem import draw_emblem

RED = (218, 41, 28)
YELLOW = (255, 199, 44)
DARK = (45, 45, 45)
GRAY = (140, 140, 140)
WHITE = (255, 255, 255)
BG = (247, 245, 242)
BORDER = (226, 222, 216)

W, H = 720, 900

FONT_CANDIDATES = [
    r"C:\Windows\Fonts\msyhbd.ttc",
    r"C:\Windows\Fonts\msyh.ttc",
    r"C:\Windows\Fonts\simhei.ttf",
    "/System/Library/Fonts/PingFang.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
]


def load_font(size, bold=True):
    for p in FONT_CANDIDATES:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:  # noqa: BLE001
                continue
    return ImageFont.load_default()


# ---------- 对话脚本（每条 = 一帧增量） ----------
FLOW = [
    ("u", "20 块以内，要又脆又甜的"),
    ("u", "帮我发明一个隐藏吃法"),
    ("a", "◆ 配方引擎启动……"),
    ("a", "① 扫描门店菜单（130 项真实在售）"),
    ("a", "② 风味矩阵匹配候选组合"),
    ("a", "③ 实时计价复核  [OK]"),
    ("a", "● 芝士瀑布薯条 · 实测 ¥17.50"),
    ("a", "● 酸甜脆薯 · 实测 ¥14.50"),
    ("u", "就按芝士瀑布那个下单"),
    ("a", "门店确认 → 金额复核 → 明细确认"),
    ("a", "【等你确认】→ 下单成功  [OK]"),
]


def _rounded(d, box, radius, fill, outline=None):
    try:
        d.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=2)
    except AttributeError:  # 兼容老版本 Pillow
        d.rectangle(box, fill=fill)


def render_frame(n, font_title, font_msg):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # 标题栏
    d.rectangle((0, 0, W, 66), fill=RED)
    draw_emblem(img, 18, 16, 40)
    d.text((72, 16), "麦门隐藏菜单实验室 · 在线演示", font=font_title, fill=WHITE)

    y = 100
    for role, text in FLOW[:n]:
        f = font_msg
        tw = d.textlength(text, font=f)
        bw = tw + 40
        bh = 52
        if role == "u":
            x2 = W - 26
            x1 = max(26, x2 - bw)
            _rounded(d, (x1, y, x2, y + bh), 16, RED)
            d.text((x1 + 20, y + 12), text, font=f, fill=WHITE)
        else:
            x1 = 26
            x2 = min(W - 26, x1 + bw)
            _rounded(d, (x1, y, x2, y + bh), 16, WHITE, outline=BORDER)
            d.text((x1 + 20, y + 12), text, font=f, fill=DARK)
        y += bh + 18

    # 底部注脚
    d.text((26, H - 46), "真实数据 · 麦当劳 MCP 实时核验（福州 · 2026-10-10）", font=load_font(20), fill=GRAY)
    return img


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "demo.gif")
    os.makedirs(os.path.dirname(out), exist_ok=True)

    font_title = load_font(26)
    font_msg = load_font(24)

    frames = []
    durations = []
    for i in range(1, len(FLOW) + 1):
        frames.append(render_frame(i, font_title, font_msg).convert(
            "P", palette=Image.ADAPTIVE, colors=128))
        durations.append(650 if i < len(FLOW) else 3000)

    frames[0].save(out, save_all=True, append_images=frames[1:],
                   duration=durations, loop=0, optimize=True)
    print("生成:", out, "| 帧数:", len(frames), "| 大小: %.0f KB" % (os.path.getsize(out) / 1024))

    # 同时导出末帧预览（供人工检查字型）
    frames[-1].convert("RGB").save(out.replace(".gif", "_preview.png"), "PNG")
    print("预览:", out.replace(".gif", "_preview.png"))


if __name__ == "__main__":
    main()
