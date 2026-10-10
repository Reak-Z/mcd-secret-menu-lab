#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""麦门隐藏菜单实验室 · PWA 图标生成器

从项目标识（烧瓶薯条）生成 192/512 两种尺寸的 PWA 图标。

用法：
    python tools/make_icons.py
"""
import os
import sys

from PIL import Image

from emblem import draw_emblem

RED = (218, 41, 28)


def main():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out_dir = os.path.join(base, "assets", "icons")
    os.makedirs(out_dir, exist_ok=True)

    for size in (192, 512):
        img = Image.new("RGB", (size, size), RED)
        s = size / 200.0 * 0.62
        w, h = 178 * s, 258 * s          # 标识实际占用范围（px(18)~px(196) × py(-62)~py(196)）
        x = (size - w) / 2 - 18 * s
        y = (size - h) / 2 + 62 * s
        draw_emblem(img, x, y, size * 0.62)
        p = os.path.join(out_dir, "icon-%d.png" % size)
        img.save(p, "PNG")
        print("生成:", p)


if __name__ == "__main__":
    main()
