#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""应急推送工具：通过 GitHub API 通道提交文件（当 git 推送因网络抖动反复失败时使用）。

用法（在仓库根目录）：
    python _api_push.py <提交信息> <文件1> [<文件2> ...]
"""
import base64
import json
import os
import sys
import time
import urllib.error
import urllib.request

TOKEN = json.load(open(r"E:/WorkBoddy/McDonald-MCP/.workbuddy/mcp.json", encoding="utf-8"))[
    "mcpServers"]["github"]["env"]["GITHUB_TOKEN"]
REPO = "Reak-Z/mcd-secret-menu-lab"
API = "https://api.github.com"


def api(url, method="GET", data=None):
    last = ""
    for _ in range(6):
        for mode in ("direct", "env"):
            h = urllib.request.ProxyHandler({}) if mode == "direct" else urllib.request.ProxyHandler()
            req = urllib.request.Request(url, method=method)
            req.add_header("Authorization", "Bearer " + TOKEN)
            req.add_header("Accept", "application/vnd.github+json")
            req.add_header("User-Agent", "api-push")
            if data is not None:
                req.data = json.dumps(data).encode()
                req.add_header("Content-Type", "application/json")
            try:
                with urllib.request.build_opener(h).open(req, timeout=30) as r:
                    raw = r.read().decode("utf-8", "ignore")
                    return json.loads(raw) if raw.strip() else {}
            except urllib.error.HTTPError as e:
                body = e.read().decode("utf-8", "ignore")[:300]
                raise SystemExit("HTTP %s: %s" % (e.code, body))
            except Exception as e:  # noqa: BLE001
                last = "%s:%s" % (mode, type(e).__name__)
        time.sleep(3)
    raise SystemExit("API 请求失败: " + last)


def main():
    message = sys.argv[1]
    files = sys.argv[2:]

    # 1) 远端当前 head + base tree
    ref = api("%s/repos/%s/git/ref/heads/main" % (API, REPO))
    head = ref["object"]["sha"]
    commit = api("%s/repos/%s/git/commits/%s" % (API, REPO, head))
    base_tree = commit["tree"]["sha"]
    print("远端 HEAD:", head[:8])

    # 2) 为每个文件建 blob
    entries = []
    for path in files:
        with open(path, "rb") as f:
            content = f.read()
        blob = api("%s/repos/%s/git/blobs" % (API, REPO), method="POST",
                   data={"content": base64.b64encode(content).decode(), "encoding": "base64"})
        entries.append({"path": path.replace(os.sep, "/"), "mode": "100644",
                        "type": "blob", "sha": blob["sha"]})
        print("blob:", path, len(content), "bytes")

    # 3) 建 tree（基于远端 tree + 我们的变更）
    tree = api("%s/repos/%s/git/trees" % (API, REPO), method="POST",
               data={"base_tree": base_tree, "tree": entries})
    print("tree:", tree["sha"][:8])

    # 4) 建 commit
    newc = api("%s/repos/%s/git/commits" % (API, REPO), method="POST",
               data={"message": message, "tree": tree["sha"], "parents": [head]})
    print("commit:", newc["sha"][:8])

    # 5) 更新 ref
    api("%s/repos/%s/git/refs/heads/main" % (API, REPO), method="PATCH",
        data={"sha": newc["sha"], "force": False})
    print("✅ 已通过 API 推送:", newc["sha"][:8])


if __name__ == "__main__":
    main()
