# 贡献指南

感谢你考虑为「公众号日报」项目做出贡献！

## 如何贡献

### 报告 Bug

如果你发现了 Bug，请：

1. 检查 [Issues](https://github.com/你的用户名/公众号日报/issues) 确保该问题尚未被报告
2. 创建新的 Issue，包含：
   - 清晰的标题
   - 详细的问题描述
   - 复现步骤
   - 期望的行为
   - 实际的行为
   - 截图（如果适用）
   - 环境信息（操作系统、Python 版本等）

### 提出新功能

如果你有功能建议：

1. 先在 Issues 中搜索，确保没有重复
2. 创建 Feature Request Issue
3. 详细描述你的想法和使用场景
4. 如果可能，提供实现思路

### 提交代码

1. **Fork 项目**
   ```bash
   # 点击 GitHub 页面上的 Fork 按钮
   ```

2. **克隆到本地**
   ```bash
   git clone https://github.com/你的用户名/公众号日报.git
   cd 公众号日报
   ```

3. **创建特性分支**
   ```bash
   git checkout -b feature/amazing-feature
   ```

4. **进行修改**
   - 保持代码风格一致
   - 添加必要的注释
   - 测试你的修改

5. **提交改动**
   ```bash
   git add .
   git commit -m "feat: 添加某个新功能"
   ```

   提交信息格式：
   - `feat:` 新功能
   - `fix:` 修复 Bug
   - `docs:` 文档更新
   - `style:` 代码格式调整
   - `refactor:` 代码重构
   - `test:` 测试相关
   - `chore:` 构建/工具相关

6. **推送到 GitHub**
   ```bash
   git push origin feature/amazing-feature
   ```

7. **创建 Pull Request**
   - 在 GitHub 上打开你的 Fork
   - 点击 "New Pull Request"
   - 填写 PR 描述，说明你的改动
   - 等待审核

## 代码规范

### Python 代码

- 遵循 [PEP 8](https://pep8.org/) 风格指南
- 使用 4 空格缩进
- 函数和变量使用小写加下划线命名
- 类名使用大驼峰命名
- 添加适当的文档字符串

示例：
```python
def parse_html_file(filepath):
    """解析HTML文件，提取关键信息

    Args:
        filepath: HTML文件路径

    Returns:
        包含解析结果的字典，失败返回 None
    """
    # 代码实现
    pass
```

### HTML/CSS

- 使用 2 空格缩进
- 类名使用小写加连字符
- 保持语义化的 HTML 结构
- CSS 按功能分组，添加注释

## 测试

在提交 PR 前，请确保：

- [ ] 代码可以正常运行
- [ ] `generate_index.py` 能正确生成 index.html
- [ ] 生成的页面在主流浏览器中显示正常
- [ ] 移动端响应式布局正常
- [ ] 没有引入新的错误或警告

## 文档

如果你的改动涉及：

- 新功能：更新 README.md
- API 变更：更新相关文档
- 配置项：更新配置说明

## 问题和讨论

有任何疑问？可以：

- 在 Issues 中提问
- 发送邮件至 your.email@example.com
- 参与项目讨论

## 行为准则

- 尊重他人，保持友善
- 接受建设性的批评
- 专注于对项目最有利的事情
- 对其他社区成员表示同理心

再次感谢你的贡献！ 🎉
