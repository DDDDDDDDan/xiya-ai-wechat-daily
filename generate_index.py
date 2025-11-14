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

        # 首先尝试从文件名中提取日期
        filename = os.path.basename(filepath)
        filename_date_match = re.match(r'(\d{4})-(\d{1,2})-(\d{1,2})\.html', filename)

        if filename_date_match:
            year, month, day = filename_date_match.groups()
            date_str = f"{year}年{month}月{day}日"
            # 计算星期几
            try:
                date_obj = datetime(int(year), int(month), int(day))
                weekday_map = {0: '一', 1: '二', 2: '三', 3: '四', 4: '五', 5: '六', 6: '日'}
                weekday = weekday_map[date_obj.weekday()]
            except:
                weekday = '一'
        else:
            # 如果文件名不匹配，尝试从内容中提取日期（兼容旧格式）
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
            background: #2c3e50;
            color: white;
            padding: 60px 0 50px;
            margin-bottom: 40px;
            position: relative;
            overflow: hidden;
        }}

        .header::before {{
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320"><path fill="rgba(52,152,219,0.1)" d="M0,96L48,112C96,128,192,160,288,160C384,160,480,128,576,122.7C672,117,768,139,864,138.7C960,139,1056,117,1152,101.3C1248,85,1344,75,1392,69.3L1440,64L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"></path></svg>') no-repeat bottom;
            background-size: cover;
            opacity: 0.3;
        }}

        .header-content {{
            max-width: 900px;
            margin: 0 auto;
            padding: 0 20px;
            text-align: center;
            position: relative;
            z-index: 1;
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
            margin-bottom: 40px;
        }}

        .header-title {{
            font-size: 28px;
            font-weight: 700;
            margin-bottom: 24px;
            margin-top: 40px;
        }}

        .header-description {{
            font-size: 16px;
            line-height: 1.8;
            margin-bottom: 30px;
            opacity: 0.95;
            max-width: 800px;
            margin-left: auto;
            margin-right: auto;
        }}

        .features-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 24px;
            margin-top: 36px;
        }}

        .feature-card {{
            background: rgba(52, 152, 219, 0.15);
            backdrop-filter: blur(10px);
            border-radius: 12px;
            padding: 24px;
            transition: all 0.3s ease;
            border: 1px solid rgba(52, 152, 219, 0.3);
        }}

        .feature-card:hover {{
            background: rgba(52, 152, 219, 0.25);
            transform: translateY(-4px);
            border-color: rgba(52, 152, 219, 0.5);
        }}

        .feature-icon {{
            font-size: 36px;
            margin-bottom: 12px;
        }}

        .feature-title {{
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 8px;
            color: white;
        }}

        .feature-desc {{
            font-size: 14px;
            opacity: 0.9;
            line-height: 1.6;
            color: rgba(255, 255, 255, 0.9);
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

        .footer {{
            background: #2c3e50;
            color: #ecf0f1;
            padding: 50px 20px 30px;
            margin-top: 60px;
        }}

        .footer-content {{
            max-width: 900px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 40px;
            align-items: center;
        }}

        .footer-left {{
            text-align: left;
        }}

        .footer-title {{
            font-size: 20px;
            font-weight: 600;
            margin-bottom: 16px;
            color: #3498db;
        }}

        .footer-description {{
            font-size: 14px;
            line-height: 1.8;
            color: #bdc3c7;
            margin-bottom: 20px;
        }}

        .creator-info {{
            display: flex;
            align-items: center;
            gap: 12px;
            margin-top: 20px;
            padding-top: 20px;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
        }}

        .creator-avatar {{
            width: 48px;
            height: 48px;
            background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            font-weight: 700;
            color: white;
        }}

        .creator-details {{
            flex: 1;
        }}

        .creator-name {{
            font-size: 16px;
            font-weight: 600;
            color: #ecf0f1;
            margin-bottom: 4px;
        }}

        .creator-role {{
            font-size: 13px;
            color: #95a5a6;
        }}

        .footer-right {{
            text-align: center;
        }}

        .qrcode-container {{
            background: white;
            padding: 0;
            border-radius: 12px;
            display: inline-block;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }}

        .qrcode-container img {{
            display: block;
            width: 160px;
            height: 160px;
        }}

        .qrcode-label {{
            margin-top: 12px;
            font-size: 14px;
            color: #bdc3c7;
            font-weight: 500;
        }}

        .copyright {{
            text-align: center;
            padding-top: 30px;
            margin-top: 30px;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            color: #95a5a6;
            font-size: 13px;
        }}

        @media (max-width: 768px) {{
            .header {{
                padding: 40px 0 40px;
            }}

            .header h1 {{
                font-size: 28px;
            }}

            .header-title {{
                font-size: 24px;
            }}

            .header-description {{
                font-size: 15px;
            }}

            .features-grid {{
                grid-template-columns: 1fr;
            }}

            .footer-content {{
                grid-template-columns: 1fr;
                gap: 30px;
            }}

            .footer-left {{
                text-align: center;
            }}

            .creator-info {{
                justify-content: center;
            }}

            .daily-card {{
                padding: 20px;
            }}

            .daily-date {{
                font-size: 20px;
            }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <div class="header-content">
            <h1>📰 蹊涯AI：公众号日报</h1>
            <div class="subtitle">专注金融投资 · AI智能总结 · 每日精选财经深度</div>

            <div class="header-title">您的金融投资智能助手</div>
            <div class="header-description">
                <strong>蹊涯AI日报</strong>专注于金融投资与产业研究领域，
                运用AI技术从顶级财经公众号中精选深度内容，涵盖产业链分析、公司研报、行业动态、投资机会等核心信息。
            </div>

            <div class="features-grid">
                <div class="feature-card">
                    <div class="feature-icon">📈</div>
                    <div class="feature-title">专业财经聚合</div>
                    <div class="feature-desc">精选市值风云、调研纪要、思想钢印等头部财经公众号，聚焦新能源、AI、半导体等热门赛道</div>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">🤖</div>
                    <div class="feature-title">AI智能总结</div>
                    <div class="feature-desc">每篇文章自动提炼核心观点和投资逻辑，附带明确的行动指引，10秒看懂一篇深度研报</div>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">⏰</div>
                    <div class="feature-title">每日定时推送</div>
                    <div class="feature-desc">工作日持续更新，不错过市场热点与投资机会，让您的投资决策始终领先一步</div>
                </div>
            </div>
        </div>
    </div>

    <div class="container">
        <div class="section-title">所有日报</div>

{cards_section}
    </div>

    <div class="footer">
        <div class="footer-content">
            <div class="footer-left">
                <div class="footer-title">蹊涯AI：公众号日报</div>
                <div class="footer-description">
                    聚焦金融投资与产业研究，每日精选顶级财经公众号深度内容。
                    覆盖AI、新能源、半导体、医药生物等核心投资领域，为投资者提供专业决策参考。
                    <br><br>
                    立即扫码关注「蹊涯学习室」公众号，第一时间获取每日投资情报，把握市场先机！
                </div>
                <div class="creator-info">
                    <div class="creator-avatar">D</div>
                    <div class="creator-details">
                        <div class="creator-name">Dan</div>
                        <div class="creator-role">产品策划与开发</div>
                    </div>
                </div>
            </div>
            <div class="footer-right">
                <div class="qrcode-container">
                    <img src="https://github.com/DDDDDDDDan/xiya-ai-wechat-daily/blob/main/%E8%B9%8A%E6%B6%AF%E5%AD%A6%E4%B9%A0%E5%AE%A4%E4%BA%8C%E7%BB%B4%E7%A0%81.jpg?raw=true" alt="蹊涯学习室公众号">
                </div>
                <div class="qrcode-label">扫码关注公众号</div>
            </div>
        </div>
        <div class="copyright">
            蹊涯AI：公众号日报 © 2025 - 精选优质内容，分享知识价值 | Made with ❤️ by Dan
        </div>
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
