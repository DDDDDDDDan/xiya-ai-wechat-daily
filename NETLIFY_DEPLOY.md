# 📘 Netlify 部署指南

本文档介绍如何将「公众号日报」项目部署到 Netlify。

## 🚀 方式一：通过 Git 自动部署（推荐）

### 步骤 1: 推送代码到 GitHub

```bash
# 如果还没有推送到 GitHub
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/你的用户名/公众号日报.git
git push -u origin main
```

### 步骤 2: 连接到 Netlify

1. 访问 [Netlify](https://app.netlify.com/)
2. 点击 **"Add new site"** → **"Import an existing project"**
3. 选择 **GitHub**（首次需要授权）
4. 选择你的仓库 **"公众号日报"**

### 步骤 3: 配置构建设置

Netlify 会自动检测到 `netlify.toml` 配置文件，无需手动配置。

**确认以下设置**：
- **Branch to deploy**: `main`
- **Build command**: `python3 generate_index.py`
- **Publish directory**: `scr`

点击 **"Deploy site"**

### 步骤 4: 等待部署完成

- 首次部署约需 1-2 分钟
- 部署成功后，Netlify 会提供一个 URL：
  ```
  https://random-name-123456.netlify.app
  ```

### 步骤 5: 自定义域名（可选）

1. 进入 **Site settings** → **Domain management**
2. 点击 **"Add custom domain"**
3. 输入你的域名（如 `daily.yourdomain.com`）
4. 按照提示配置 DNS 记录

---

## 🎯 方式二：拖放部署（快速测试）

### 快速部署

1. 本地生成网站：
   ```bash
   python generate_index.py
   ```

2. 访问 [Netlify Drop](https://app.netlify.com/drop)

3. 直接拖拽 `scr/` 文件夹到页面

4. 立即获得部署链接！

**注意**：拖放部署不支持自动更新，每次需要手动重新上传。

---

## 🔄 自动部署工作流

配置完成后，工作流程如下：

```
1. 添加新日报到 scr/ 目录
   ↓
2. 提交并推送到 GitHub
   git add .
   git commit -m "Add new daily report"
   git push
   ↓
3. Netlify 自动检测到更改
   ↓
4. 运行构建命令
   python3 generate_index.py
   ↓
5. 部署到 CDN
   ↓
6. 网站自动更新！✅
```

---

## ⚙️ 配置说明

### netlify.toml 配置文件

项目已包含 `netlify.toml` 配置文件，主要设置：

```toml
[build]
  command = "python3 generate_index.py"  # 构建命令
  publish = "scr"                        # 发布目录

[build.environment]
  PYTHON_VERSION = "3.8"                 # Python 版本
```

### 环境变量（如需要）

在 Netlify 后台设置环境变量：

1. **Site settings** → **Build & deploy** → **Environment**
2. 点击 **"Edit variables"**
3. 添加变量（例如 API keys）

---

## 🌐 自定义域名配置

### 使用 Netlify 子域名

1. **Site settings** → **Domain management** → **Custom domains**
2. 点击 **"Options"** → **"Edit site name"**
3. 修改为自定义名称：
   ```
   公众号日报.netlify.app → my-daily.netlify.app
   ```

### 使用自己的域名

#### DNS 配置（推荐）

在你的 DNS 提供商添加记录：

**方式 A - CNAME（子域名）**
```
类型: CNAME
名称: daily (或 www)
值: your-site.netlify.app
```

**方式 B - A 记录（顶级域名）**
```
类型: A
名称: @
值: 75.2.60.5
```

#### Netlify DNS（可选）

1. 将域名的 nameservers 指向 Netlify
2. 在 Netlify 管理 DNS 记录
3. 好处：自动 SSL、更快的部署

---

## 🔒 启用 HTTPS

Netlify 自动为所有站点启用 HTTPS（Let's Encrypt）

**自定义域名 HTTPS**：
1. 添加域名后，等待 DNS 验证
2. 自动签发 SSL 证书（约 10 分钟）
3. 启用 **"Force HTTPS"** 选项

---

## 📊 监控和分析

### 部署日志

查看构建日志：
1. **Deploys** 标签
2. 点击任意部署记录
3. 查看详细日志

### 分析统计

1. **Analytics** 标签（需订阅）
2. 查看访问量、带宽使用等

### 表单处理（可选）

Netlify 支持表单提交（无需后端）：

```html
<form name="contact" method="POST" data-netlify="true">
  <input type="text" name="name" />
  <input type="email" name="email" />
  <button type="submit">提交</button>
</form>
```

---

## 🐛 故障排查

### 构建失败

**错误**: `python3: command not found`

**解决**:
- 检查 `netlify.toml` 中的 Python 版本设置
- 确认使用 `python3` 而非 `python`

**错误**: `No such file or directory: scr`

**解决**:
- 确认 `publish = "scr"` 路径正确
- 检查脚本是否成功生成了文件

### 部署成功但页面空白

**原因**:
- 检查浏览器控制台错误
- 确认 `index.html` 存在于 `scr/` 目录
- 检查文件路径是否正确

### 更新不生效

**解决**:
1. 清除浏览器缓存
2. 在 Netlify 后台手动触发重新部署
3. 检查 Git 是否正确推送

---

## 💡 高级配置

### 预览部署

每个 Pull Request 自动创建预览部署：
- 独立的 URL
- 不影响主站
- 方便测试更改

### 分支部署

部署多个分支：
```toml
[context.production]
  command = "python3 generate_index.py"

[context.deploy-preview]
  command = "python3 generate_index.py"

[context.branch-deploy]
  command = "python3 generate_index.py"
```

### 重定向规则

在 `netlify.toml` 中配置：
```toml
[[redirects]]
  from = "/old-path"
  to = "/new-path"
  status = 301

[[redirects]]
  from = "/blog/*"
  to = "/news/:splat"
  status = 302
```

---

## 🆓 免费额度

Netlify 免费计划包括：
- ✅ 100 GB 带宽/月
- ✅ 300 分钟构建时间/月
- ✅ 无限站点数量
- ✅ 自动 HTTPS
- ✅ 持续部署
- ✅ 表单处理（100 次/月）

对于个人博客/日报完全够用！

---

## 📞 获取帮助

- 📖 [Netlify 官方文档](https://docs.netlify.com/)
- 💬 [Netlify 社区论坛](https://answers.netlify.com/)
- 🐛 [提交 Issue](https://github.com/你的用户名/公众号日报/issues)

---

## ✅ 部署检查清单

部署前确认：

- [ ] 代码已推送到 GitHub
- [ ] `netlify.toml` 配置正确
- [ ] 本地测试 `python generate_index.py` 成功
- [ ] `scr/index.html` 已生成
- [ ] Git 仓库设为 public（或 Netlify 已授权访问 private）

部署后验证：

- [ ] 网站可以正常访问
- [ ] 所有页面链接正常
- [ ] 移动端显示正常
- [ ] HTTPS 已启用
- [ ] 自定义域名配置成功（如有）

---

**🎉 现在你的网站已部署到 Netlify！每次推送代码都会自动更新！**

访问你的网站: `https://your-site.netlify.app`
