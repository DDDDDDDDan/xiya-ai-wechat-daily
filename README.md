# 蹊涯AI：公众号日报

精选优质公众号文章，每日为您呈现。

## 📁 项目结构

```
├── posts_content/          # Markdown格式的原始文章内容
│   ├── post_6.md
│   ├── post_7.md
│   └── ...
├── src/                    # 生成的HTML文件
│   ├── index.html         # 首页导航
│   ├── 2025-10-24.html   # 各日期的日报
│   └── ...
├── generate_html.py       # 从markdown生成HTML的脚本
└── update_index.py        # 更新首页导航的脚本
```

## 🚀 使用方法

### 生成日报HTML文件

```bash
python generate_html.py
```

这将读取 `posts_content` 文件夹中的所有markdown文件，并在 `src` 文件夹中生成对应的HTML文件。

### 更新首页导航

```bash
python update_index.py
```

这将扫描所有生成的HTML文件，并更新 `src/index.html` 作为导航首页。

## 📊 功能特性

- ✨ 响应式设计，适配各种设备
- 🎨 现代化的UI界面
- 📱 文章卡片式布局
- 🔍 按日期组织的日报
- 📈 统计数据展示

## 🛠️ 技术栈

- Python 3
- HTML5/CSS3
- Markdown

## 📝 数据来源

文章内容来自Supabase数据库中的posts表。

## 📄 许可证

© 2025 蹊涯AI - 精选优质内容，分享知识价值
