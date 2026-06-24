# 🎵 网易云歌单分析 Skill

> 基于你的「我喜欢的音乐」歌单，生成一份深度个性化的音乐品味编年史报告。

![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

## ✨ 这是什么

这是一个能够自动抓取你的网易云音乐歌单数据，进行多维度分析，并生成一份故事化的音乐编年史报告的 skill。

**输出效果**：一份 3000-6000 字的深度分析报告（Markdown + PDF），以第二人称「你」的视角，像一位懂音乐的老朋友，深入解读你多年音乐收藏背后的灵魂画像。

## 📊 分析维度

| 维度 | 说明 |
|------|------|
| 🕰️ 时间线 | 年度收藏量趋势，你在哪些年份疯狂收歌 |
| 🎤 歌手图谱 | Top 100 歌手排名，各年份最爱歌手变迁 |
| 🌍 语言版图 | 华语/欧美/日语/韩语等分布及年度变化 |
| ⏱️ 时长偏好 | 长歌 vs 短歌，你的注意力曲线 |
| 📅 收藏节奏 | 高频月份和日期，哪些日子你在疯狂收歌 |
| 🌙 深夜灵魂 | 凌晨 0-4 点的收藏记录，夜晚的你在听什么 |
| 🎼 年代考古 | 你收藏的歌跨越了哪些音乐时代 |

## 🚀 使用方法

### 在 AI coding 产品中使用（如 codex、claude code、codebuddy）

1. 安装此 Skill（导入 `.skill` 文件或从 Skill 市场安装）
2. 对 AI 说：**「分析我的网易云歌单」**
3. 提供以下信息：
   - ✅ 你的「我喜欢的音乐」歌单链接
   - ✅ 你的年龄
   - 💡 可选：昵称、职业、城市等补充信息
4. 等待几分钟，获得完整报告 🎉

### 触发关键词

以下关键词会自动激活此 Skill：
- "音乐分析"、"歌单分析"、"网易云分析"
- "音乐编年史"、"分析我的歌单"
- "我的音乐品味"、"音乐报告"
- 直接发送网易云歌单链接

## 📁 项目结构

```
netease-playlist-analyzer/
├── README.md                              # 本文件
├── SKILL.md                               # Skill 定义（工作流 + 触发条件）
├── scripts/
│   ├── fetch_playlist.py                  # 歌单数据获取（支持链接/ID 自动识别）
│   ├── analyze_playlist.py                # 多维度数据分析
│   ├── generate_html_report.py            # Markdown → 精美 HTML
│   └── html_to_pdf.py                     # HTML → PDF（基于 Playwright）
└── references/
    └── report_writing_guide.md            # 报告写作风格指南
```

## ⚙️ 依赖

- **Python 3.8+**
- **requests**：用于调用网易云 API
- **playwright**（可选）：用于生成 PDF

```bash
pip install requests playwright
playwright install chromium
```

> 💡 如果不安装 playwright，报告仍会正常生成 HTML 和 Markdown 格式，你可以用浏览器手动打印为 PDF。

## 📝 注意事项

- 歌单需要设置为 **公开** 或 **链接可见** 状态
- 歌曲数 > 5000 首时获取时间约 3-5 分钟
- 已内置请求频率控制（0.8s 间隔），无需担心被封
- 报告中所有数据均来自实际分析，不编造任何内容

## 📄 输出示例

报告会包含以下章节：

1. **音乐内核总述** — 用一段话概括你的音乐灵魂
2. **编年史纪元** — 按年份划分 3-6 个时期，讲述音乐与人生的交织
3. **深层解读** — 3-5 条贯穿始终的音乐线索
4. **灵魂画像** — 一句话定义你的音乐人格
5. **🔮 下一纪元：音乐预言** — 根据你的年龄与品味演进，为即将到来的人生阶段推荐 8-12 首歌，附哲学释义
6. **尾声** — 从过去到未来的呼应

## 🤝 Contributing

欢迎提 Issue 和 PR！如果你有好的分析维度建议或报告优化想法，非常期待你的贡献。

## 📜 License

MIT License
