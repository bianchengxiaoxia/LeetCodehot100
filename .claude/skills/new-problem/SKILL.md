---
name: new-problem
description: 为 LeetCode Hot 100 仓库创建新题目脚手架（文件夹 + LeetCode 官方 Python3 代码模板 + 题目卡 image.png + 空笔记）。当用户说"准备下一题""创建 XX 题的文件夹"或给出题号时使用。
---

# new-problem — Hot 100 新题目脚手架

在仓库根目录创建 `<中文题名>/` 文件夹，结构与 `两数之和/` 一致：代码文件、`image.png` 题目卡、空《解题思路与收获.md》。

## 输入

题号（优先）或中文题名。都没有时，读 `README.md` 的「题单明细」，取第一个未勾选题作为建议并向用户确认。

## 流程

### 1. 查静态映射

读本 skill 目录下的 `hot100.json`（100 题静态表：`id / category / slug / title / difficulty`），按题号取条目。

> ⚠️ 不要用 GraphQL 搜索类接口做题号→slug 反查（schema 频繁变动，已踩坑多次），静态表是唯一可靠来源。

### 2. 拉取题目详情

在仓库根目录执行（替换 `<slug>`）：

```bash
curl -sS -m 20 -X POST https://leetcode.cn/graphql \
  -H "Content-Type: application/json" -H "Referer: https://leetcode.cn" \
  -d '{"query":"query q($s: String!){ question(titleSlug: $s){ questionFrontendId translatedTitle translatedContent difficulty codeSnippets{ langSlug code } } }","variables":{"s":"<slug>"}}' \
  -o _q.json
```

用到 `data.question` 里的：`translatedContent`（HTML 题面）、`codeSnippets` 中 `langSlug=="python3"` 的 `code`（官方模板）。

### 3. 创建文件

文件夹名 = 中文题名（`translatedTitle`，应与 hot100.json 的 `title` 一致；不一致以 API 为准并提醒用户）：

| 文件 | 内容 |
|------|------|
| `<slug驼峰>.py` | LeetCode 官方 python3 模板原文；若方法体为空，补一个 docstring 作为方法体（内容见下）。文件名转换：slug 按 `-` 分段，首段原样、其余段首字母大写（`group-anagrams` → `groupAnagrams.py`） |
| `解题思路与收获.md` | 空文件 |
| `image.png` | 第 4 步生成 |

方法体 docstring 格式：

```python
        """<题号>. <题名>（<难度>）· <专题>
        题目链接: https://leetcode.cn/problems/<slug>/
        """
```

### 4. 渲染题目卡

```bash
PYTHONIOENCODING=utf-8 python .claude/skills/new-problem/render_card.py _q.json <输出文件夹> "LeetCode 热题 100 · <专题> ｜ 难度：<难度> ｜ leetcode.cn/problems/<slug>/"
```

### 5. 收尾

- 删除临时文件 `_q.json` 和 `__pycache__/`
- 建议用视觉模型抽查 `image.png`（乱码 / 重叠 / 截断）
- 提醒用户：做完题后更新 `README.md`（勾 checkbox、进度数字、「已完成」表加行），再 `git add -A && git commit && git push`

## 本机环境注意（2026-09 实测）

- leetcode.cn 的 API 从命令行直连可达（GraphQL 和 `api/problems/all/` 都可用）
- 控制台是 GBK：python 打印不要用 emoji，统一加 `PYTHONIOENCODING=utf-8`
- 依赖：Pillow 已装；字体用 `C:\Windows\Fonts\msyh.ttc`（常规）和 `msyhbd.ttc`（加粗）
- 新版题目页 HTML：示例的「输入/输出」不在 `<pre>` 里，而是普通段落 + `<ul>` 列表；`render_card.py` 按行首关键词分类渲染（输入/输出→灰色代码块，示例/解释→加粗+蓝色竖条），这段逻辑是踩坑修正后的结果，不要改动
- hot100.json 的数据来源：`https://leetcode.cn/api/problems/all/`（slug/难度）+ 官方学习计划清单（中文名/专题），若未来题目信息变化可重新生成
