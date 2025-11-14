#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
from datetime import datetime

posts_dir = r"C:\Users\A\Downloads\1\posts_content"
src_dir = r"C:\Users\A\Downloads\1\src"
index_path = os.path.join(src_dir, "index.html")

def extract_info_from_md(content):
    """从markdown内容中提取信息"""
    info = {
        'date': None,
        'article_count': 0,
        'account_count': 0,
        'accounts': []
    }

    # 提取日期
    date_match = re.search(r'📅 \*\*日期\*\*:(\d{4})年(\d{1,2})月(\d{1,2})日', content)
    if date_match:
        year, month, day = date_match.groups()
        info['date'] = f"{year}-{int(month):02d}-{int(day):02d}"

    # 提取来源信息
    source_match = re.search(r'📰 \*\*来源\*\*:(\d+)个公众号,共(\d+)篇文章', content)
    if source_match:
        info['account_count'] = int(source_match.group(1))
        info['article_count'] = int(source_match.group(2))

    # 提取公众号名称 - 从**公众号:文章标题**格式中提取
    account_matches = re.findall(r'\*\*([^:*]+):[^*]+?\*\*', content)
    # 清理并去重
    accounts = []
    for acc in account_matches:
        acc = acc.strip()
        if acc and acc not in accounts and len(acc) < 30:  # 过滤太长的内容
            accounts.append(acc)
    info['accounts'] = accounts[:6]  # 最多显示6个

    return info

def get_weekday(date_str):
    """获取星期几"""
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        weekdays = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
        return weekdays[date_obj.weekday()]
    except:
        return ""

def format_date_chinese(date_str):
    """格式化日期为中文"""
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        return f"{date_obj.year}年{date_obj.month}月{date_obj.day}日"
    except:
        return date_str

def main():
    # 获取所有markdown文件并提取信息
    daily_reports = []

    md_files = [f for f in os.listdir(posts_dir) if f.endswith('.md')]

    for md_file in md_files:
        file_path = os.path.join(posts_dir, md_file)

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        info = extract_info_from_md(content)

        if info['date']:
            html_file = f"{info['date']}.html"
            html_path = os.path.join(src_dir, html_file)

            # 只添加已经生成的HTML文件
            if os.path.exists(html_path):
                info['html_file'] = html_file
                daily_reports.append(info)

    # 按日期排序（最新的在前）
    daily_reports.sort(key=lambda x: x['date'], reverse=True)

    # 计算总统计
    total_reports = len(daily_reports)
    total_articles = sum(r['article_count'] for r in daily_reports)

    # 生成HTML
    html_content = f'''<!DOCTYPE html>
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
                <div class="stat-number">{total_reports}</div>
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

        <div class="section-title">所有日报</div>

'''

    # 生成每个日报的卡片
    for report in daily_reports:
        date_chinese = format_date_chinese(report['date'])
        weekday = get_weekday(report['date'])

        accounts_html = ''.join([f'<span class="preview-tag">📱 {acc}</span>' for acc in report['accounts']])

        html_content += f'''        <a href="{report['html_file']}" class="daily-card">
            <div class="daily-header">
                <div class="daily-date">
                    <span class="icon">📅</span>
                    <span>{date_chinese}</span>
                </div>
                <div class="daily-weekday">{weekday}</div>
            </div>
            <div class="daily-meta">
                <div class="meta-item">
                    <span class="emoji">📝</span>
                    <span>共 <span class="number">{report['article_count']}</span> 篇文章</span>
                </div>
                <div class="meta-item">
                    <span class="emoji">🏢</span>
                    <span>{report['account_count']} 个公众号</span>
                </div>
            </div>
            <div class="daily-preview">
                {accounts_html}
            </div>
            <div class="daily-footer">
                <span class="read-btn">查看本期日报</span>
            </div>
        </a>

'''

    html_content += '''    </div>

    <div class="footer">
        <p>蹊涯AI：公众号日报 © 2025 - 精选优质内容，分享知识价值</p>
    </div>
</body>
</html>
'''

    # 写入文件
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"✅ index.html 已更新！")
    print(f"📊 总共 {total_reports} 期日报，{total_articles} 篇文章")

if __name__ == "__main__":
    main()
