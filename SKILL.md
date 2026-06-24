---
name: netease-music-chronicle
description: |
  网易云音乐编年史——基于用户"我喜欢的音乐"歌单数据，生成深度个性化的音乐品味分析报告。
  输出包含精美的 Markdown 长文报告、多页分页 HTML（每页独立设计背景+装饰）和可打印的 PDF。
  报告风格为故事化叙述，以第二人称（"你"）视角深入解读用户音乐收藏背后的灵魂画像。
  当用户提到"音乐分析"、"歌单分析"、"网易云分析"、"音乐编年史"、"分析我的歌单"、
  "我的音乐品味"、"音乐报告"时使用此skill。
  也适用于用户发来网易云音乐歌单链接并希望获得深度解读的场景。
---

# 网易云音乐编年史 Skill

## 概述

将用户的网易云"我喜欢的音乐"歌单，转化为一份深度个性化的音乐品味编年史报告（Markdown + 精美多页 HTML + PDF）。

## 工作流程

### Phase 1: 收集用户信息

向用户询问以下信息：

1. **必需**：网易云"我喜欢的音乐"歌单链接（形如 `https://music.163.com/playlist?id=XXXXXXX`）
2. **必需**：用户当前年龄（用于推算每年对应的人生阶段）
3. **可选**：任何补充信息（职业、所在城市、音乐相关经历、希望报告的称呼等）

示例询问：
```
为了生成你的音乐编年史，我需要以下信息：
1. 你的网易云"我喜欢的音乐"歌单链接
2. 你现在的年龄（我会用它推算每年你的人生阶段）
3. 其他你想让我知道的信息（可选，比如昵称、职业、城市等）
```

### Phase 2: 获取歌单数据

运行数据获取脚本：

```bash
python3 {SKILL_DIR}/scripts/fetch_playlist.py "<歌单链接或ID>" "<工作目录>/playlist_data.json"
```

脚本会：
- 从链接中自动提取歌单ID
- 分批获取所有歌曲详情（每批200首，间隔0.8秒）
- 输出包含歌名、歌手、专辑、时长、添加时间、发布时间的JSON

### Phase 3: 数据分析

运行分析脚本：

```bash
python3 {SKILL_DIR}/scripts/analyze_playlist.py "<工作目录>/playlist_data.json" "<工作目录>/analysis_data.json"
```

分析维度包括：
- 年度收藏量趋势
- Top 100 歌手排名
- 各年份最爱歌手变化
- 语言/地区分布及年度变化
- 时长分布与偏好
- 音乐发行年代分布
- 高频收藏月份和日期
- 深夜收藏(0-4点)统计
- 首尾歌曲对比
- 高频收藏日（单日>10首的日子）

### Phase 4: 撰写报告

读取 `analysis_data.json`，结合用户年龄和补充信息，撰写音乐编年史 Markdown 报告。

**写作指南详见**: `references/report_writing_guide.md`

核心原则：
- 第二人称叙述，像懂音乐的老朋友在深谈
- 数据精确但为故事服务
- 将音乐选择与人生阶段深度结合
- 故事化关键时刻（跨年夜、高频日、深夜收藏）
- 提炼贯穿始终的灵魂线索
- 报告长度4000-8000字

报告结构（共8个章节）：
1. **音乐内核总述** — 用比喻概括灵魂底色
2. **编年史纪元**（按年份分3-6个纪元）— 故事化叙述每段人生
3. **音乐琴弦** — 将品味抽象为5-6根"弦"，每根对应一类音乐和情感需求
4. **灵魂疆域** — 精神地图：北方/日本/深夜/长歌等坐标
5. **峥嵘岁月** — 按年龄段总结人生弧线
6. **下一纪元：音乐预言** — 推荐8-12首歌 + 场景化描写 + 哲学释义
7. **尾声** — 从第一首歌到最后一首歌的呼应，温暖收尾

将报告保存为 `<工作目录>/music_report.md`。

### Phase 5: 生成HTML和PDF

#### 方案A：精美多页HTML + Playwright PDF（推荐）

1. 生成多页精美HTML报告：

```bash
python3 {SKILL_DIR}/scripts/generate_html_report.py "<工作目录>/music_report.md" "<工作目录>/music_report.html"
```

HTML报告特点：
- A4分页设计（`page-break-after: always`）
- 每页独立背景色/渐变 + 主题装饰元素（声波、唱片、琴弦、指南针等）
- 封面页含唱片装饰、音符、五线谱元素
- 使用 Noto Serif SC + Noto Sans SC 字体
- 引用块、琴弦卡片、疆域卡片、时间轴等多种排版组件
- 每页底部页码
- 浅色暖调设计

2. 通过Playwright转PDF：

```bash
pip install playwright 2>/dev/null; playwright install chromium 2>/dev/null
python3 {SKILL_DIR}/scripts/html_to_pdf.py "<工作目录>/music_report.html" "<工作目录>/music_report.pdf"
```

#### 方案B：ReportLab 暗色主题PDF（备选，无需浏览器）

```bash
pip install reportlab 2>/dev/null
python3 {SKILL_DIR}/scripts/generate_pdf_reportlab.py "<工作目录>/analysis_data.json" "<工作目录>/music_report.md" "<工作目录>/music_report.pdf"
```

暗色PDF特点：
- 深色背景 (#0D1117) + 青/紫/金/粉多色点缀
- 数据柱状图可视化
- 引用块高亮样式
- 不依赖浏览器，适合服务器环境

如果两个方案都不可用，告知用户可以直接用浏览器打开HTML文件并打印为PDF。

### Phase 6: 交付

向用户展示：
1. 完整的 Markdown 报告内容
2. 告知 HTML 和 PDF 文件位置
3. 简要总结关键发现

## 注意事项

- 歌单必须是**公开**或**链接可见**状态才能获取数据
- 如果歌单歌曲数>5000首，获取时间可能较长（约3-5分钟）
- 网易云API有频率限制，脚本已内置0.8秒间隔
- 报告中引用的所有数据必须来自实际分析结果，不可编造
- 工作目录默认为当前项目目录，所有中间文件和最终报告都保存在此
- HTML报告设计为A4打印优化，浏览器中直接Ctrl+P即可获得精美打印效果
