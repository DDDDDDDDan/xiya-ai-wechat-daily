# 部署指南

本文档介绍如何将「公众号日报」部署到不同的平台。

## 📋 目录

- [GitHub Pages（推荐）](#github-pages)
- [Vercel](#vercel)
- [Netlify](#netlify)
- [自托管服务器](#自托管服务器)

---

## Netlify ⭐

**推荐使用 Netlify 部署！** 配置简单，自动构建，全球 CDN 加速。

### 快速开始

1. **推送代码到 GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git push -u origin main
   ```

2. **导入到 Netlify**
   - 访问 [Netlify](https://app.netlify.com/)
   - 点击 "Add new site" → "Import an existing project"
   - 选择 GitHub → 选择你的仓库
   - Netlify 自动检测 `netlify.toml` 配置
   - 点击 "Deploy site"

3. **完成！**
   - 获得 URL：`https://random-name.netlify.app`
   - 可自定义站点名或绑定域名
   - 每次推送代码自动部署

### 配置说明

项目已包含 `netlify.toml` 配置文件：
```toml
[build]
  command = "python3 generate_index.py"
  publish = "scr"

[build.environment]
  PYTHON_VERSION = "3.8"
```

### 详细文档

查看完整的 Netlify 部署指南：[NETLIFY_DEPLOY.md](NETLIFY_DEPLOY.md)

包括：
- Git 自动部署
- 拖放部署
- 自定义域名配置
- HTTPS 设置
- 故障排查

---

## GitHub Pages

### 方式一：自动部署（推荐）

1. **推送代码到 GitHub**

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/你的用户名/公众号日报.git
git push -u origin main
```

2. **启用 GitHub Pages**

- 进入仓库 Settings → Pages
- Source 选择 `gh-pages` 分支
- 保存

3. **自动部署**

- 项目已配置 GitHub Actions（`.github/workflows/deploy.yml`）
- 每次推送到 `main` 分支会自动：
  - 运行 `generate_index.py` 生成索引
  - 部署 `scr/` 目录到 GitHub Pages

4. **访问网站**

几分钟后，访问：
```
https://你的用户名.github.io/公众号日报/
```

### 方式二：手动部署

1. **本地生成**

```bash
python generate_index.py
```

2. **推送到 gh-pages 分支**

```bash
cd scr
git init
git add .
git commit -m "Deploy"
git branch -M gh-pages
git remote add origin https://github.com/你的用户名/公众号日报.git
git push -f origin gh-pages
```

3. **在 GitHub Settings → Pages 中选择 `gh-pages` 分支**

---

## Vercel

### 部署步骤

1. **安装 Vercel CLI（可选）**

```bash
npm i -g vercel
```

2. **配置 vercel.json**

项目根目录创建 `vercel.json`：

```json
{
  "buildCommand": "python generate_index.py",
  "outputDirectory": "scr",
  "cleanUrls": true
}
```

3. **部署**

方式 A - 使用 CLI：
```bash
vercel
```

方式 B - 从 GitHub 导入：
- 访问 [Vercel Dashboard](https://vercel.com/dashboard)
- Import Git Repository
- 选择你的仓库
- 自动部署

4. **访问**

Vercel 会提供一个域名，如：
```
https://公众号日报.vercel.app
```

---

## 自托管服务器

### Nginx 配置

1. **生成静态文件**

```bash
python generate_index.py
```

2. **上传到服务器**

```bash
scp -r scr/* user@your-server:/var/www/daily/
```

3. **Nginx 配置**

```nginx
server {
    listen 80;
    server_name your-domain.com;
    root /var/www/daily;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    # 启用 gzip 压缩
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml;
}
```

4. **重启 Nginx**

```bash
sudo nginx -t
sudo systemctl reload nginx
```

### Apache 配置

```apache
<VirtualHost *:80>
    ServerName your-domain.com
    DocumentRoot /var/www/daily

    <Directory /var/www/daily>
        Options -Indexes +FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>

    # 启用压缩
    <IfModule mod_deflate.c>
        AddOutputFilterByType DEFLATE text/html text/css application/javascript
    </IfModule>
</VirtualHost>
```

---

## 使用自定义域名

### GitHub Pages

1. 在仓库 Settings → Pages → Custom domain 输入域名
2. 在 DNS 提供商添加 CNAME 记录：

```
CNAME  www  你的用户名.github.io
```

或 A 记录（顶级域名）：
```
A  @  185.199.108.153
A  @  185.199.109.153
A  @  185.199.110.153
A  @  185.199.111.153
```

### Vercel / Netlify

在平台的 Domain Settings 中添加自定义域名，然后按提示配置 DNS。

---

## 持续部署工作流

### 推荐流程

```bash
# 1. 添加新日报到 scr/ 目录
# 2. 运行脚本生成索引
python generate_index.py

# 3. 提交并推送
git add .
git commit -m "Add daily report for 2025-11-13"
git push

# 4. 自动部署（如已配置 CI/CD）
# 等待几分钟，网站自动更新
```

---

## 故障排查

### GitHub Actions 失败

1. 检查 Actions 日志
2. 确保 `generate_index.py` 能正常运行
3. 验证 Python 版本兼容性

### 页面 404

1. 确认 GitHub Pages 已启用
2. 检查分支设置（main 或 gh-pages）
3. 确保 `index.html` 存在于根目录或 `scr/` 目录

### 样式不显示

1. 检查 CSS 路径是否正确
2. 清除浏览器缓存
3. 检查控制台错误信息

---

## 性能优化

### 启用 CDN

对于静态资源，可以使用 CDN 加速：

- Cloudflare（免费）
- jsDelivr（GitHub 文件）
- 国内可用七牛云、又拍云等

### 压缩优化

```bash
# 压缩 HTML
npm install -g html-minifier
html-minifier --collapse-whitespace --remove-comments scr/*.html

# 压缩图片（如果有）
npm install -g imagemin-cli
imagemin images/* --out-dir=images-optimized
```

---

需要帮助？查看 [README.md](README.md) 或提交 [Issue](https://github.com/你的用户名/公众号日报/issues)。
