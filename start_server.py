#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
本地开发服务器启动脚本
在浏览器中预览生成的网站
"""

import http.server
import socketserver
import webbrowser
import os
from pathlib import Path

# 配置
PORT = 8000
DIRECTORY = "scr"

def main():
    """启动本地服务器"""

    # 切换到 scr 目录
    script_dir = Path(__file__).parent
    web_dir = script_dir / DIRECTORY

    if not web_dir.exists():
        print(f"错误: {DIRECTORY} 目录不存在")
        return

    os.chdir(web_dir)

    # 创建服务器
    Handler = http.server.SimpleHTTPRequestHandler

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        url = f"http://localhost:{PORT}"
        print(f"🚀 服务器启动成功！")
        print(f"📡 访问地址: {url}")
        print(f"📁 服务目录: {web_dir}")
        print(f"\n按 Ctrl+C 停止服务器")
        print("-" * 50)

        # 自动打开浏览器
        webbrowser.open(url)

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n👋 服务器已停止")

if __name__ == "__main__":
    main()
