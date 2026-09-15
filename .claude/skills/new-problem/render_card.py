# -*- coding: utf-8 -*-
"""render_card.py —— 把 leetcode.cn 题目 JSON 渲染成题目卡 image.png

用法:
    PYTHONIOENCODING=utf-8 python render_card.py <题目JSON> <输出目录> "<副标题行>"

题目JSON = graphql question(titleSlug) 的完整返回;
副标题行例: LeetCode 热题 100 · 哈希 ｜ 难度：中等 ｜ leetcode.cn/problems/group-anagrams/
"""
import json, os, re, sys
from html.parser import HTMLParser
from PIL import Image, ImageDraw, ImageFont

W, PAD = 1080, 48
MAXW = W - 2 * PAD

F_TITLE = ImageFont.truetype(r"C:\Windows\Fonts\msyhbd.ttc", 30)
F_SUB   = ImageFont.truetype(r"C:\Windows\Fonts\msyh.ttc", 19)
F_BODY  = ImageFont.truetype(r"C:\Windows\Fonts\msyh.ttc", 22)
F_BOLD  = ImageFont.truetype(r"C:\Windows\Fonts\msyhbd.ttc", 22)
F_CODE  = ImageFont.truetype(r"C:\Windows\Fonts\msyh.ttc", 21)

LH_BODY, LH_CODE, LH_EX = 37, 33, 37
DIFF = {"Easy": "简单", "Medium": "中等", "Hard": "困难"}

TEXT, SUBTLE, CODEBG, ACCENT, LINE = "#1f2328", "#8b949e", "#f6f8fa", "#0969da", "#d0d7de"


class T(HTMLParser):
    """题目 HTML → (文本, 类型) 列表。新版题面示例的输入/输出不在 <pre> 里，
    故按行首关键词分类: 输入/输出→code，示例/解释→example，其余→desc。"""
    def __init__(self):
        super().__init__()
        self.items, self.buf, self.pre = [], "", None

    def flush(self):
        t = self.buf.replace("\xa0", " ").strip()
        if t:
            for l in t.split("\n"):
                l = re.sub(r"\s*([，。；、：！？）])\s*", r"\1", l.strip())
                if l:
                    if l.startswith(("输入", "输出")):
                        kind = "code"
                    elif l.startswith(("示例", "解释")):
                        kind = "example"
                    else:
                        kind = "desc"
                    self.items.append((l, kind))
        self.buf = ""

    def handle_starttag(self, tag, attrs):
        if tag == "pre":
            self.flush(); self.pre = ""
        elif tag in ("p", "ul", "ol"):
            self.flush()
        elif tag == "li":
            self.flush(); self.buf = "• "
        elif tag == "sup":
            self.buf += "^"

    def handle_endtag(self, tag):
        if tag == "pre" and self.pre is not None:
            for l in self.pre.split("\n"):
                l = re.sub(r"\s*([，。；、：！？）])\s*", r"\1", l.replace("\xa0", " ").rstrip())
                if l.strip():
                    self.items.append((l, "code"))
            self.pre = None
        elif tag in ("p", "li"):
            self.flush()

    def handle_data(self, d):
        if self.pre is not None:
            self.pre += d
        else:
            self.buf += d


def wrap(draw, text, font, maxw):
    lines, cur = [], ""
    for ch in text:
        t = cur + ch
        if draw.textlength(t, font=font) > maxw and cur:
            lines.append(cur); cur = ch
        else:
            cur = t
    if cur:
        lines.append(cur)
    return lines


def main():
    json_path, out_dir, meta_line = sys.argv[1], sys.argv[2], sys.argv[3]
    q = json.load(open(json_path, encoding="utf-8"))["data"]["question"]
    pid = q["questionFrontendId"]
    title = q["translatedTitle"]
    diff = DIFF.get(q.get("difficulty", ""), "?")

    p = T(); p.feed(q["translatedContent"])
    merged = []  # 相邻的 输入/输出 行合并进同一个代码块
    for s, k in p.items:
        if k == "code" and merged and merged[-1][1] == "code":
            merged[-1] = (merged[-1][0] + "\n" + s, "code")
        else:
            merged.append((s, k))
    p.items = merged

    dummy = ImageDraw.Draw(Image.new("RGB", (8, 8)))
    ops, y = [], 0

    def text(x, ty, s, font, fill):
        ops.append(("text", x, ty, s, font, fill))

    # —— 标题区 ——
    y = PAD
    text(PAD, y, f"{pid}. {title}", F_TITLE, TEXT)
    y += 44
    text(PAD, y, meta_line, F_SUB, SUBTLE)
    y += 34
    ops.append(("line", PAD, y, W - PAD, y, LINE)); y += 20

    # —— 正文 ——
    prev = None
    for s, kind in p.items:
        if kind == "code":
            lines = []
            for src in s.split("\n"):
                lines.extend(wrap(dummy, src, F_CODE, MAXW - 36))
            h = LH_CODE * len(lines) + 28
            ops.append(("rect", PAD, y, W - PAD, y + h, CODEBG))
            for i, l in enumerate(lines):
                text(PAD + 18, y + 14 + i * LH_CODE, l, F_CODE, TEXT)
            y += h + 8
        else:
            font = F_BOLD if kind == "example" else F_BODY
            if kind == "example" and prev != "example":
                y += 10
                ops.append(("bar", PAD, y + 6, PAD + 4, y + 30, ACCENT))
            for l in wrap(dummy, s, font, MAXW - (14 if kind == "example" else 0)):
                text(PAD + (14 if kind == "example" else 0), y, l, font, TEXT)
                y += LH_EX if kind == "example" else LH_BODY
            y += 10
        prev = kind

    H = y + PAD
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    for op in ops:
        if op[0] == "text":
            _, x, ty, s, font, fill = op; d.text((x, ty), s, font=font, fill=fill)
        elif op[0] == "line":
            _, x1, y1, x2, y2, fill = op; d.line((x1, y1, x2, y2), fill=fill, width=1)
        elif op[0] == "rect":
            _, x1, y1, x2, y2, fill = op; d.rounded_rectangle((x1, y1, x2, y2), 8, fill=fill)
        elif op[0] == "bar":
            _, x1, y1, x2, y2, fill = op; d.rectangle((x1, y1, x2, y2), fill=fill)

    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, "image.png")
    img.save(out)
    print("saved:", out.replace("\\", "/"), "| size:", img.size, "| bytes:", os.path.getsize(out))


if __name__ == "__main__":
    main()
