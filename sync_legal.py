"""将 App 现有协议转换为可直接打开的静态 HTML 页面。"""
import html
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT.parent / "ecce-app/assets/legal"
FIELDS = {"operator": "LAPO_LEGAL_OPERATOR", "contact": "LAPO_PRIVACY_CONTACT",
          "region": "LAPO_DATA_REGION", "provider": "LAPO_CLOUD_PROVIDER"}
TITLES = {"privacy": "隐私政策", "terms": "用户协议", "minors": "未成年人个人信息保护规则"}


def paragraph(text):
    escaped = html.escape(text)
    escaped = re.sub(r"https://[^\s<]+", lambda m: f'<a href="{m[0]}">{m[0]}</a>', escaped)
    return f"<p>{escaped}</p>"


def render_document(name, title):
    text = (SOURCE / f"{name}.txt").read_text(encoding="utf-8")
    for field, variable in FIELDS.items():
        default = "小海懒科技(深圳)有限公司" if field == "operator" else "尚未公布"
        text = text.replace("{{" + field + "}}", os.environ.get(variable, "").strip() or default)
    lines = text.splitlines()
    body = []
    for block in "\n".join(lines[1:]).strip().split("\n\n"):
        first, _, rest = block.partition("\n")
        if re.match(r"^[一二三四五六七八九十]+、|^附录：|^（[一二三四五六七八九十]+）", first):
            tag = "h3" if first.startswith("（") else "h2"
            body.append(f"<{tag}>{html.escape(first)}</{tag}>")
            if rest:
                body.append(paragraph(rest))
        else:
            body.append(paragraph(block))
    content = "\n".join(body)
    links = " ".join(f'<a href="{key}.html"' + (' aria-current="page"' if key == name else '') + f'>{value}</a>' for key, value in TITLES.items())
    page = f'''<!doctype html>
<html lang="zh-CN">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="lapo {title}全文。"><title>lapo {title}</title>
<link rel="icon" href="assets/icon.png"><link rel="stylesheet" href="style.css"></head>
<body><a class="skip-link" href="#main">跳转到正文</a>
<header class="site-header"><a href="index.html" aria-label="lapo 首页"><img class="logo" src="assets/logo.png" alt="lapo" width="132" height="66"></a></header>
<main id="main" class="legal"><a class="back" href="index.html#agreements">返回官网</a>
<article><h1>{html.escape(lines[0])}</h1>{content}</article></main>
<footer class="site-footer"><span>lapo · 协议与保护规则</span>{links}</footer></body></html>
'''
    (ROOT / f"{name}.html").write_text(page, encoding="utf-8")


for name, title in TITLES.items():
    render_document(name, title)
