#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成HTML格式的音乐编年史报告
用法: python generate_html_report.py <markdown_file> <output_html>
将markdown报告转换为精美的可打印HTML页面
"""
import sys
import re


def md_to_html_content(md_text):
    """简单的markdown到HTML转换"""
    lines = md_text.split('\n')
    html_parts = []
    in_paragraph = False

    for line in lines:
        stripped = line.strip()

        if stripped.startswith('# '):
            if in_paragraph:
                html_parts.append('</p>')
                in_paragraph = False
            html_parts.append(f'<h1>{process_inline(stripped[2:])}</h1>')
        elif stripped.startswith('## '):
            if in_paragraph:
                html_parts.append('</p>')
                in_paragraph = False
            html_parts.append(f'<h2>{process_inline(stripped[3:])}</h2>')
        elif stripped.startswith('### '):
            if in_paragraph:
                html_parts.append('</p>')
                in_paragraph = False
            html_parts.append(f'<h3>{process_inline(stripped[4:])}</h3>')
        elif stripped == '---':
            if in_paragraph:
                html_parts.append('</p>')
                in_paragraph = False
            html_parts.append('<hr>')
        elif stripped == '':
            if in_paragraph:
                html_parts.append('</p>')
                in_paragraph = False
        else:
            if not in_paragraph:
                html_parts.append('<p>')
                in_paragraph = True
            html_parts.append(process_inline(stripped) + '<br>')

    if in_paragraph:
        html_parts.append('</p>')

    return '\n'.join(html_parts)


def process_inline(text):
    """处理行内markdown格式"""
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    return text


def generate_html(md_path, output_path):
    """生成完整的HTML报告"""
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    content_html = md_to_html_content(md_content)

    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>音乐编年史</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600;700;900&family=Noto+Sans+SC:wght@300;400;500;700&display=swap');

* {{
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}}

@page {{
  size: A4;
  margin: 0;
}}

body {{
  font-family: 'Noto Sans SC', -apple-system, sans-serif;
  line-height: 1.9;
  color: #2d2d2d;
  background: #fafafa;
  padding: 40px 60px;
  max-width: 900px;
  margin: 0 auto;
}}

h1 {{
  font-family: 'Noto Serif SC', serif;
  font-size: 2.2em;
  color: #1a1a1a;
  margin: 50px 0 20px;
  padding-bottom: 12px;
  border-bottom: 2px solid #e8e0d6;
}}

h2 {{
  font-family: 'Noto Serif SC', serif;
  font-size: 1.6em;
  color: #333;
  margin: 40px 0 16px;
  padding-left: 12px;
  border-left: 4px solid #c4956a;
}}

h3 {{
  font-size: 1.2em;
  color: #555;
  margin: 25px 0 10px;
}}

p {{
  margin: 12px 0;
  text-align: justify;
}}

strong {{
  color: #1a1a1a;
  font-weight: 700;
}}

em {{
  font-style: italic;
  color: #666;
}}

hr {{
  border: none;
  height: 1px;
  background: linear-gradient(to right, transparent, #ccc, transparent);
  margin: 50px 0;
}}

@media print {{
  body {{
    padding: 30mm 25mm;
    max-width: none;
  }}
  h2 {{
    page-break-before: auto;
  }}
}}
</style>
</head>
<body>
{content_html}
</body>
</html>'''

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"✅ HTML报告已生成: {output_path}")


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("用法: python generate_html_report.py <markdown_file> <output_html>")
        sys.exit(1)
    generate_html(sys.argv[1], sys.argv[2])
