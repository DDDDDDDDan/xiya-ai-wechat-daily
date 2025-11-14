# 蹊涯AI：公众号日报

精选优质公众号文章，每日为您呈现。

## 📁 项目结构

```
蹊涯AI：公众号日报/
├── src/                      # HTML 文件目录
│   ├── index.html           # 首页导航（自动生成）
│   ├── 2025-10-24.html      # 日报文件（按日期命名）
│   ├── 2025-10-29.html
│   └── ...                  # 更多日报文件
├── .github/                 # GitHub 配置
│   └── ISSUE_TEMPLATE/      # Issue 模板
├── generate_index.py        # 生成首页索引的脚本
├── netlify.toml             # Netlify 部署配置
├── requirements.txt         # Python 依赖
├── DEPLOY.md                # 部署文档
├── NETLIFY_SETUP.md         # Netlify 设置指南
├── CONTRIBUTING.md          # 贡献指南
├── CHANGELOG.md             # 更新日志
└── README.md                # 本文件
```

## 🚀 快速开始

### 环境要求

- Python 3.6+
- （可选）Supabase 账户（如需集成数据库）

### 本地运行

1. **克隆项目**
   ```bash
   git clone <repository-url>
   cd <project-directory>
   ```

2. **安装依赖**（可选，如需 Supabase 集成）
   ```bash
   pip install -r requirements.txt
   ```

3. **生成首页索引**
   ```bash
   python generate_index.py
   ```

   这将扫描 `src/` 目录中的所有日报 HTML 文件，自动生成 `src/index.html` 首页。

4. **本地预览**
   ```bash
   cd src
   python -m http.server 8000
   ```

   访问 http://localhost:8000 查看效果。

## 📊 功能特性

- ✨ **响应式设计** - 完美适配桌面、平板、手机
- 🎨 **现代化 UI** - 简洁优雅的界面设计
- 📱 **卡片式布局** - 清晰展示每期日报信息
- 🔍 **按日期组织** - 时间线式浏览体验
- 📈 **统计数据** - 实时显示期数和文章数
- 🚀 **自动部署** - Netlify 一键部署
- 📑 **公众号预览** - 每期显示涉及的公众号

## 🛠️ 技术栈

- **后端脚本**: Python 3
- **前端展示**: HTML5/CSS3
- **部署平台**: Netlify
- **数据来源**: Supabase（可选）

## 📝 工作流程

1. 将日报 HTML 文件放入 `src/` 目录（格式：`YYYY-MM-DD.html`）
2. 运行 `python generate_index.py` 自动更新首页索引
3. 推送到 GitHub，Netlify 自动部署

## 🌐 部署

### Netlify 部署

详细部署步骤请参考：
- [NETLIFY_SETUP.md](NETLIFY_SETUP.md) - Netlify 完整设置指南
- [DEPLOY.md](DEPLOY.md) - 通用部署文档

**快速部署**：
1. 将项目推送到 GitHub
2. 在 Netlify 导入 GitHub 仓库
3. Netlify 会自动读取 `netlify.toml` 配置并部署

## 🤝 贡献

欢迎贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详情。

## 📋 更新日志

查看 [CHANGELOG.md](CHANGELOG.md) 了解版本更新历史。

## 📄 许可证

MIT License

© 2025 蹊涯AI - 精选优质内容，分享知识价值

## 📮 联系方式

如有问题或建议，欢迎提交 Issue。
