#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成精美多页HTML格式的音乐编年史报告
用法: python generate_html_report.py <markdown_file> <output_html>

设计特点：
- A4分页设计（每页page-break-after: always）
- 每页独立背景色/渐变 + 主题装饰元素
- 封面页含唱片装饰、音符、五线谱元素
- 使用 Noto Serif SC + Noto Sans SC 字体
- 引用块、琴弦卡片、疆域卡片、时间轴等排版组件
- 浅色暖调设计，适合打印
"""
import sys
import re


# ========== CSS 样式模板 ==========
CSS_TEMPLATE = '''
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600;700;900&family=Noto+Sans+SC:wght@300;400;500;700&display=swap');

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

@page {
  size: A4;
  margin: 0;
}

body {
  font-family: 'Noto Sans SC', sans-serif;
  line-height: 1.8;
  color: #2d2d2d;
  background: #fafafa;
}

.page {
  width: 210mm;
  min-height: 297mm;
  padding: 45mm 25mm 35mm 25mm;
  position: relative;
  overflow: hidden;
  page-break-after: always;
}

/* ===== 封面 ===== */
.page-cover {
  background: linear-gradient(160deg, #fef9f0 0%, #fff5eb 30%, #fdf0e8 60%, #fce8d8 100%);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  padding: 30mm;
}

.page-cover::before {
  content: '';
  position: absolute;
  top: -60px;
  right: -60px;
  width: 400px;
  height: 400px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(255,183,120,0.15) 0%, transparent 70%);
}

.page-cover::after {
  content: '';
  position: absolute;
  bottom: -80px;
  left: -80px;
  width: 500px;
  height: 500px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(200,150,255,0.1) 0%, transparent 70%);
}

.cover-vinyl {
  position: absolute;
  top: 50px;
  right: 40px;
  width: 180px;
  height: 180px;
  border-radius: 50%;
  background: conic-gradient(from 0deg, #e8e0d8, #d4c8b8, #e8e0d8, #c8baa8, #e8e0d8);
  opacity: 0.25;
  box-shadow: inset 0 0 30px rgba(0,0,0,0.1);
}

.cover-vinyl::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #fef9f0;
  box-shadow: 0 0 0 3px rgba(180,150,100,0.3);
}

.cover-notes {
  position: absolute;
  bottom: 80px;
  left: 50px;
  font-size: 72px;
  opacity: 0.08;
  color: #8b6914;
  letter-spacing: 20px;
}

.cover-staff {
  position: absolute;
  top: 40%;
  left: 0;
  right: 0;
  height: 60px;
  opacity: 0.06;
}

.cover-staff::before {
  content: '';
  position: absolute;
  top: 0;
  left: 5%;
  right: 5%;
  height: 1px;
  background: #666;
  box-shadow: 0 12px 0 #666, 0 24px 0 #666, 0 36px 0 #666, 0 48px 0 #666;
}

.cover-title {
  font-family: 'Noto Serif SC', serif;
  font-size: 36px;
  font-weight: 900;
  color: #3d2b1f;
  margin-bottom: 20px;
  position: relative;
  z-index: 1;
  letter-spacing: 2px;
}

.cover-subtitle {
  font-size: 16px;
  color: #8b6a4a;
  font-weight: 300;
  letter-spacing: 4px;
  margin-bottom: 40px;
  position: relative;
  z-index: 1;
}

.cover-meta {
  font-size: 13px;
  color: #a08060;
  position: relative;
  z-index: 1;
  line-height: 2.2;
}

.cover-divider {
  width: 80px;
  height: 2px;
  background: linear-gradient(90deg, transparent, #c8a060, transparent);
  margin: 30px auto;
}

/* ===== 内容页通用 ===== */
.page-content {
  background: linear-gradient(180deg, #fdfcfa 0%, #f9f6f2 100%);
}

.section-title {
  font-family: 'Noto Serif SC', serif;
  font-size: 22px;
  font-weight: 700;
  margin-bottom: 24px;
  position: relative;
  padding-left: 16px;
  color: #2d2d2d;
}

.section-title::before {
  content: '';
  position: absolute;
  left: 0;
  top: 4px;
  bottom: 4px;
  width: 4px;
  border-radius: 2px;
  background: #c89020;
}

.section-subtitle {
  font-size: 13px;
  color: #888;
  margin-bottom: 20px;
  font-weight: 300;
  letter-spacing: 1px;
}

.content {
  position: relative;
  z-index: 1;
}

.content p {
  margin-bottom: 14px;
  font-size: 13.5px;
  line-height: 2;
  text-align: justify;
}

.content p strong {
  font-weight: 600;
  color: #1a1a1a;
}

.content hr {
  border: none;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(0,0,0,0.08), transparent);
  margin: 24px 0;
}

.quote-block {
  margin: 16px 0;
  padding: 12px 16px;
  border-radius: 8px;
  font-style: italic;
  font-size: 13px;
  background: rgba(200,144,32,0.05);
  border-left: 3px solid rgba(200,144,32,0.2);
}

.page-footer {
  position: absolute;
  bottom: 20px;
  left: 0;
  right: 0;
  text-align: center;
  font-size: 10px;
  color: rgba(0,0,0,0.15);
  letter-spacing: 2px;
}

.page-number {
  position: absolute;
  bottom: 20px;
  right: 30px;
  font-size: 10px;
  color: rgba(0,0,0,0.2);
  font-family: 'Noto Serif SC', serif;
}

@media print {
  body { background: white; }
  .page { box-shadow: none; }
}
'''


def parse_markdown_sections(md_text):
    """将Markdown解析为章节结构"""
    sections = []
    current_section = {'title': '', 'subtitle': '', 'content': []}
    lines = md_text.split('\n')

    for line in lines:
        stripped = line.strip()
        if stripped.startswith('## '):
            if current_section['title'] or current_section['content']:
                sections.append(current_section)
            current_section = {'title': stripped[3:], 'subtitle': '', 'content': []}
        elif stripped.startswith('### ') and not current_section['content']:
            current_section['subtitle'] = stripped[4:]
        elif stripped == '---':
            continue
        elif stripped.startswith('# ') and not sections:
            # 主标题作为封面
            current_section = {'title': stripped[2:], 'subtitle': '', 'content': [], 'is_cover': True}
        else:
            current_section['content'].append(line)

    if current_section['title'] or current_section['content']:
        sections.append(current_section)

    return sections


def process_inline_md(text):
    """处理行内Markdown格式"""
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    return text


def paragraphs_to_html(lines):
    """将行列表转为HTML段落"""
    html_parts = []
    paragraph = []

    for line in lines:
        stripped = line.strip()
        if stripped == '':
            if paragraph:
                text = ' '.join(paragraph)
                text = process_inline_md(text)
                html_parts.append(f'<p>{text}</p>')
                paragraph = []
        else:
            paragraph.append(stripped)

    if paragraph:
        text = ' '.join(paragraph)
        text = process_inline_md(text)
        html_parts.append(f'<p>{text}</p>')

    return '\n    '.join(html_parts)


def extract_cover_info(md_text):
    """从Markdown提取封面信息"""
    title_match = re.search(r'^# (.+)$', md_text, re.MULTILINE)
    title = title_match.group(1) if title_match else '音乐编年史'

    # 尝试从标题中分离主标题和副标题
    if '：' in title:
        parts = title.split('：', 1)
        main_title = parts[0] + '的音乐编年史'
        subtitle = parts[1]
    elif ':' in title:
        parts = title.split(':', 1)
        main_title = parts[0] + '的音乐编年史'
        subtitle = parts[1]
    else:
        main_title = title
        subtitle = ''

    return main_title, subtitle


def generate_html(md_path, output_path):
    """生成完整的多页HTML报告"""
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    main_title, subtitle = extract_cover_info(md_content)
    sections = parse_markdown_sections(md_content)

    # 构建HTML页面
    pages_html = []

    # 封面
    pages_html.append(f'''
<!-- 封面 -->
<div class="page page-cover">
  <div class="cover-vinyl"></div>
  <div class="cover-notes">♪ ♫ ♩ ♬</div>
  <div class="cover-staff"></div>
  
  <div class="cover-title">{main_title}</div>
  <div class="cover-divider"></div>
  <div class="cover-subtitle">{subtitle}</div>
  <div class="cover-meta">
    网易云音乐"我喜欢的音乐"深度分析<br>
    由 AI 生成的个人音乐品味编年史
  </div>
  <div class="page-footer">MUSIC · SOUL · CHRONICLE</div>
</div>''')

    # 内容页
    page_num = 1
    for section in sections:
        if section.get('is_cover'):
            continue
        if not section['title'] and not section['content']:
            continue

        content_html = paragraphs_to_html(section['content'])
        if not content_html.strip():
            continue

        subtitle_html = f'<div class="section-subtitle">{section["subtitle"]}</div>' if section['subtitle'] else ''

        pages_html.append(f'''
<!-- {section['title']} -->
<div class="page page-content">
  <div class="content">
    <div class="section-title">{process_inline_md(section["title"])}</div>
    {subtitle_html}
    {content_html}
  </div>
  <div class="page-number">{page_num:02d}</div>
</div>''')
        page_num += 1

    all_pages = '\n'.join(pages_html)

    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{main_title}</title>
<style>
{CSS_TEMPLATE}
</style>
</head>
<body>
{all_pages}
</body>
</html>'''

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"✅ HTML报告已生成: {output_path}")
    print(f"   共 {page_num} 页（含封面）")
    print(f"   建议在浏览器中打开预览，支持 Ctrl+P 直接打印为 PDF")


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("用法: python generate_html_report.py <markdown_file> <output_html>")
        sys.exit(1)
    generate_html(sys.argv[1], sys.argv[2])
