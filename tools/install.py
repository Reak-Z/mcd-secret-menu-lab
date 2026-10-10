#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""一键安装「麦门隐藏菜单实验室」Skill 到本机技能目录。

自动探测目标（优先级）：
1. ~/.workbuddy/skills/mcd-secret-menu-lab/   （WorkBuddy）
2. ~/.claude/skills/mcd-secret-menu-lab/      （Claude Code 等）

用法：
    python tools/install.py [自定义技能根目录]
"""
import os
import shutil
import sys


def main():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    if len(sys.argv) > 1:
        dest_root = sys.argv[1]
    else:
        home = os.path.expanduser("~")
        if os.path.isdir(os.path.join(home, ".workbuddy")):
            dest_root = os.path.join(home, ".workbuddy", "skills")
        else:
            dest_root = os.path.join(home, ".claude", "skills")

    dest = os.path.join(dest_root, "mcd-secret-menu-lab")
    os.makedirs(dest, exist_ok=True)

    shutil.copy2(os.path.join(base, "SKILL.md"), os.path.join(dest, "SKILL.md"))
    src_ref = os.path.join(base, "references")
    dst_ref = os.path.join(dest, "references")
    os.makedirs(dst_ref, exist_ok=True)
    for f in os.listdir(src_ref):
        shutil.copy2(os.path.join(src_ref, f), os.path.join(dst_ref, f))

    print("✅ 已安装到:", dest)
    print("提示：请先在客户端配置麦当劳 MCP 连接器（见 README 快速开始），再新开一个会话使用。")


if __name__ == "__main__":
    main()
