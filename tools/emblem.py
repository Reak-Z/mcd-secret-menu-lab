#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""麦门隐藏菜单实验室 · 原创标识绘制模块

设计说明：本标识为项目原创图形（实验室烧瓶 + 薯条 + 气泡），
不使用麦当劳官方 Logo（金色拱门/M 标等均为注册商标，未经授权不得使用）。

用法：
    from emblem import draw_emblem
    draw_emblem(img, x, y, size)
"""
import os

from PIL import Image, ImageDraw

YELLOW = (255, 199, 44)
RED = (218, 41, 28)
FRY = (255, 199, 44)
FRY2 = (250, 186, 28)


def draw_emblem(img, x, y, size, fg=(255, 255, 255), liquid=YELLOW):
    """在 img 的 (x, y) 处绘制 size 大小的原创"烧瓶薯条"标识。"""
    d = ImageDraw.Draw(img)
    s = size / 200.0

    def px(v):
        return x + v * s

    def py(v):
        return y + v * s

    # ---- 薯条（先画，插在瓶口后面）----
    d.polygon([(px(66), py(-30)), (px(86), py(-37)), (px(94), py(46)), (px(74), py(46))], fill=FRY)
    d.rounded_rectangle((px(94), py(-62), px(114), py(46)), radius=6 * s, fill=FRY2)
    d.polygon([(px(126), py(-37)), (px(146), py(-30)), (px(138), py(46)), (px(118), py(46))], fill=FRY)

    # ---- 瓶颈 ----
    d.rectangle((px(78), py(16), px(136), py(88)), fill=fg)

    # ---- 瓶身（梯形 + 圆底）----
    d.polygon([(px(50), py(80)), (px(164), py(80)), (px(196), py(174)), (px(18), py(174))], fill=fg)
    d.ellipse((px(18), py(150), px(196), py(196)), fill=fg)

    # ---- 液体（黄色）----
    d.polygon([(px(60), py(116)), (px(154), py(116)), (px(180), py(168)), (px(34), py(168))], fill=liquid)
    d.ellipse((px(34), py(146), px(180), py(190)), fill=liquid)

    # ---- 气泡 ----
    d.ellipse((px(74), py(132), px(98), py(156)), fill=fg)
    d.ellipse((px(112), py(146), px(130), py(164)), fill=fg)
    d.ellipse((px(60), py(160), px(74), py(174)), fill=fg)


def main():
    """快速预览 + 导出透明背景资产（供 README / 物料使用）。"""
    img = Image.new("RGB", (480, 320), RED)
    draw_emblem(img, 140, 70, 200)
    img.save("emblem_test.png")
    print("预览已生成: emblem_test.png")

    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    canvas = Image.new("RGBA", (420, 420), (0, 0, 0, 0))
    draw_emblem(canvas, 110, 132, 200)
    out = os.path.join(base, "assets", "emblem.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    canvas.save(out, "PNG")
    print("透明资产已导出:", out)


if __name__ == "__main__":
    main()
