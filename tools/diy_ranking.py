#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""麦门隐藏菜单实验室 · DIY 吃法排行榜生成器

扫描仓库中带「DIY配方」标签的 Issue，按反应数（👍❤️🎉 等）排序，
自动生成 DIY_RANKING.md。

用法：
    python tools/diy_ranking.py [--repo owner/name] [--token GITHUB_TOKEN]
"""
import argparse
import json
import os
import urllib.parse
import urllib.request

DEFAULT_REPO = "Reak-Z/mcd-secret-menu-lab"
LABEL = "DIY配方"


def api(url, token=None):
    req = urllib.request.Request(url)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", "mcd-secret-menu-lab")
    if token:
        req.add_header("Authorization", "Bearer " + token)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8", "ignore"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=DEFAULT_REPO)
    ap.add_argument("--token", default=os.environ.get("GITHUB_TOKEN", ""))
    args = ap.parse_args()

    issues, page = [], 1
    while True:
        url = ("https://api.github.com/repos/%s/issues?state=all&labels=%s&per_page=100&page=%d"
               % (args.repo, urllib.parse.quote(LABEL), page))
        batch = api(url, args.token)
        if not batch:
            break
        issues.extend([x for x in batch if "pull_request" not in x])
        if len(batch) < 100:
            break
        page += 1

    rows = []
    for it in issues:
        title = (it.get("title") or "").replace("[DIY]", "").strip()
        rc = it.get("reactions") or {}
        votes = rc.get("total_count", 0) if isinstance(rc, dict) else 0
        rows.append({
            "title": title or ("Issue #%d" % it["number"]),
            "user": it["user"]["login"],
            "votes": votes,
            "number": it["number"],
            "url": it["html_url"],
        })
    rows.sort(key=lambda r: (-r["votes"], r["number"]))

    new_url = "https://github.com/%s/issues/new?template=diy-recipe.md" % args.repo
    out_lines = [
        "# 🧪 DIY 吃法排行榜",
        "",
        "> 社区原创吃法人气榜 · 票数 = Issue 收获的反应数（👍/❤️/🎉…） · 每日自动更新",
        "",
        "| 名次 | 配方 | 作者 | 票数 | 提交 |",
        "|---:|---|---|---:|---|",
    ]
    medals = {1: "🥇", 2: "🥈", 3: "🥉"}
    for i, r in enumerate(rows, 1):
        out_lines.append("| %s | %s | @%s | %d | [#%d](%s) |"
                         % (medals.get(i, str(i)), r["title"], r["user"], r["votes"], r["number"], r["url"]))
    if not rows:
        out_lines.append("| - | *还没有 DIY 投稿，快来抢占第一名！* | - | - | [投稿](%s) |" % new_url)
    out_lines += [
        "",
        "---",
        "",
        "**如何冲榜**：用 [DIY 投稿模板](%s) 提交你的原创吃法 → 让大家给你的 Issue 点 👍 → 票数越高名次越高！" % new_url,
        "",
        "*本榜单由 [tools/diy_ranking.py](tools/diy_ranking.py) 自动生成。*",
    ]

    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "DIY_RANKING.md")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(out_lines) + "\n")
    print("已生成:", out, "| 收录 DIY 数量:", len(rows))


if __name__ == "__main__":
    main()
