#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
公众号日报首页自动生成脚本
每次新增日报后运行此脚本即可自动更新 index.html
"""

import os
import re
from datetime import datetime
from collections import Counter
from pathlib import Path

def parse_html_file(filepath):
    """解析HTML文件，提取关键信息"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # 提取日期
        date_match = re.search(r'<div class="date">(\d{4})年(\d{1,2})月(\d{1,2})日\s+星期([一二三四五六日])</div>', content)
        if not date_match:
            return None

        year, month, day, weekday = date_match.groups()
        date_str = f"{year}年{month}月{day}日"

        # 统计文章数
        article_count = len(re.findall(r'<div class="article-card">', content))

        # 提取公众号名称
        sources = re.findall(r'<span>📱 ([^<]+)</span>', content)
        # 去重并保持顺序
        unique_sources = []
        seen = set()
        for source in sources:
            if source not in seen:
                seen.add(source)
                unique_sources.append(source)

        source_count = len(unique_sources)

        return {
            'filename': os.path.basename(filepath),
            'date': date_str,
            'year': year,
            'month': month,
            'day': day,
            'weekday': weekday,
            'article_count': article_count,
            'source_count': source_count,
            'sources': unique_sources  # 改为公众号列表
        }
    except Exception as e:
        print(f"解析文件 {filepath} 时出错: {e}")
        return None

def generate_index_html(dailies):
    """生成index.html内容"""

    # 计算总统计数据
    total_issues = len(dailies)
    total_articles = sum(d['article_count'] for d in dailies)

    # 生成日报卡片HTML
    cards_html = []
    for daily in dailies:
        sources_html = ''.join([f'<span class="preview-tag">📱 {source}</span>' for source in daily['sources']])

        card = f'''        <a href="{daily['filename']}" class="daily-card">
            <div class="daily-header">
                <div class="daily-date">
                    <span class="icon">📅</span>
                    <span>{daily['date']}</span>
                </div>
                <div class="daily-weekday">星期{daily['weekday']}</div>
            </div>
            <div class="daily-meta">
                <div class="meta-item">
                    <span class="emoji">📝</span>
                    <span>共 <span class="number">{daily['article_count']}</span> 篇文章</span>
                </div>
                <div class="meta-item">
                    <span class="emoji">🏢</span>
                    <span>{daily['source_count']} 个公众号</span>
                </div>
            </div>
            <div class="daily-preview">
                {sources_html}
            </div>
            <div class="daily-footer">
                <span class="read-btn">查看本期日报</span>
            </div>
        </a>'''
        cards_html.append(card)

    cards_section = '\n\n'.join(cards_html)

    # 完整的HTML模板
    html_template = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>蹊涯AI：公众号日报 - 首页</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background-color: #f5f5f5;
            color: #333;
            line-height: 1.6;
            min-height: 100vh;
        }}

        .header {{
            background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
            color: white;
            padding: 60px 0 40px;
            margin-bottom: 40px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }}

        .header-content {{
            max-width: 900px;
            margin: 0 auto;
            padding: 0 20px;
            text-align: center;
        }}

        .header h1 {{
            font-size: 36px;
            margin-bottom: 12px;
            font-weight: 700;
            letter-spacing: -0.5px;
        }}

        .header .subtitle {{
            font-size: 16px;
            opacity: 0.9;
            font-weight: 300;
        }}

        .container {{
            max-width: 900px;
            margin: 0 auto;
            padding: 0 20px 60px;
        }}

        .section-title {{
            font-size: 20px;
            color: #2c3e50;
            margin-bottom: 24px;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .section-title::before {{
            content: "";
            width: 4px;
            height: 24px;
            background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
            border-radius: 2px;
        }}

        .daily-card {{
            background: white;
            border: 1px solid #e0e0e0;
            border-radius: 12px;
            padding: 28px;
            margin-bottom: 24px;
            transition: all 0.3s ease;
            cursor: pointer;
            text-decoration: none;
            display: block;
            color: inherit;
            position: relative;
            overflow: hidden;
        }}

        .daily-card::before {{
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #3498db 0%, #2980b9 100%);
            transform: scaleX(0);
            transform-origin: left;
            transition: transform 0.3s ease;
        }}

        .daily-card:hover::before {{
            transform: scaleX(1);
        }}

        .daily-card:hover {{
            box-shadow: 0 8px 24px rgba(0,0,0,0.12);
            transform: translateY(-4px);
            border-color: #3498db;
        }}

        .daily-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 16px;
        }}

        .daily-date {{
            font-size: 24px;
            font-weight: 700;
            color: #2c3e50;
            display: flex;
            align-items: center;
            gap: 12px;
        }}

        .daily-date .icon {{
            font-size: 28px;
        }}

        .daily-weekday {{
            background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
            color: white;
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 13px;
            font-weight: 600;
        }}

        .daily-meta {{
            display: flex;
            gap: 20px;
            margin-bottom: 16px;
            flex-wrap: wrap;
        }}

        .meta-item {{
            display: flex;
            align-items: center;
            gap: 8px;
            color: #7f8c8d;
            font-size: 14px;
        }}

        .meta-item .emoji {{
            font-size: 18px;
        }}

        .meta-item .number {{
            font-weight: 600;
            color: #3498db;
            font-size: 16px;
        }}

        .daily-preview {{
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
            margin-bottom: 20px;
        }}

        .preview-tag {{
            background: #e8f4f8;
            color: #3498db;
            padding: 6px 14px;
            border-radius: 16px;
            font-size: 13px;
            font-weight: 500;
            transition: all 0.2s;
        }}

        .daily-card:hover .preview-tag {{
            background: #3498db;
            color: white;
        }}

        .daily-footer {{
            display: flex;
            justify-content: flex-end;
            align-items: center;
            padding-top: 16px;
            border-top: 1px solid #f0f0f0;
        }}

        .read-btn {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            color: #3498db;
            font-size: 14px;
            font-weight: 600;
            transition: all 0.2s;
        }}

        .daily-card:hover .read-btn {{
            color: #2980b9;
            transform: translateX(4px);
        }}

        .read-btn::after {{
            content: "→";
            font-size: 18px;
        }}

        .stats-bar {{
            background: white;
            border: 1px solid #e0e0e0;
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 40px;
            display: flex;
            justify-content: space-around;
            gap: 20px;
            flex-wrap: wrap;
        }}

        .stat-item {{
            text-align: center;
            flex: 1;
            min-width: 120px;
        }}

        .stat-number {{
            font-size: 32px;
            font-weight: 700;
            background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 8px;
        }}

        .stat-label {{
            color: #7f8c8d;
            font-size: 14px;
        }}

        .footer {{
            text-align: center;
            padding: 40px 20px;
            color: #95a5a6;
            font-size: 14px;
        }}

        @media (max-width: 768px) {{
            .header {{
                padding: 40px 0 30px;
            }}

            .header h1 {{
                font-size: 28px;
            }}

            .daily-card {{
                padding: 20px;
            }}

            .daily-date {{
                font-size: 20px;
            }}

            .stats-bar {{
                padding: 20px;
            }}

            .stat-number {{
                font-size: 24px;
            }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <div class="header-content">
            <h1>📰 蹊涯AI：公众号日报</h1>
            <div class="subtitle">精选优质公众号文章，每日为您呈现</div>
        </div>
    </div>

    <div class="container">
        <div class="stats-bar">
            <div class="stat-item">
                <div class="stat-number">{total_issues}</div>
                <div class="stat-label">已发布期数</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">{total_articles}</div>
                <div class="stat-label">精选文章</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">持续更新</div>
                <div class="stat-label">更新状态</div>
            </div>
        </div>

        <div class="section-title">最新日报</div>

{cards_section}
    </div>

    <div class="footer">
        <p>蹊涯AI：公众号日报 © 2025 - 精选优质内容，分享知识价值</p>
    </div>
</body>
</html>'''

    return html_template

def main():
    """主函数"""
    # 设置目录
    script_dir = Path(__file__).parent
    src_dir = script_dir / 'src'

    if not src_dir.exists():
        print(f"错误: src 目录不存在: {src_dir}")
        return

    # 查找所有日报HTML文件（排除index.html）
    html_files = []
    for file in src_dir.glob('*.html'):
        if file.name.lower() != 'index.html':
            html_files.append(file)

    if not html_files:
        print("未找到任何日报文件")
        return

    print(f"找到 {len(html_files)} 个日报文件，开始解析...")

    # 解析所有文件
    dailies = []
    for filepath in html_files:
        print(f"  解析: {filepath.name}")
        info = parse_html_file(filepath)
        if info:
            dailies.append(info)

    if not dailies:
        print("没有成功解析任何文件")
        return

    # 按日期排序（最新的在前面）
    dailies.sort(key=lambda x: (x['year'], x['month'].zfill(2), x['day'].zfill(2)), reverse=True)

    print(f"\n成功解析 {len(dailies)} 个日报")
    print(f"总文章数: {sum(d['article_count'] for d in dailies)}")

    # 生成index.html
    html_content = generate_index_html(dailies)

    # 写入文件
    index_path = src_dir / 'index.html'
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"\n✅ 成功生成 index.html")
    print(f"   路径: {index_path}")
    print(f"\n各期日报:")
    for d in dailies:
        print(f"  - {d['date']} ({d['article_count']} 篇文章)")

if __name__ == '__main__':
    # Windows下设置UTF-8输出
    import sys
    if sys.platform == 'win32':
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    main()
