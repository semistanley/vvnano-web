"""每日AI内容更新脚本
============================================
Railway 使用方式:
  Railway Dashboard → Cron Jobs → 添加:
  - Schedule: 0 6 * * *  (每天北京时间6:00)
  - Command:  python scripts/daily_update.py

本地测试:
  python scripts/daily_update.py
============================================
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app

app = create_app()

with app.app_context():
    print('[Daily Update] 开始每日AI内容更新...')

    from services.ai_writer import generate_daily_news

    articles = generate_daily_news()

    if articles:
        print(f'[Daily Update] 完成! 生成了 {len(articles)} 篇内容')
        for article in articles:
            print(f'  📰 {article.title}')
    else:
        print('[Daily Update] 本次未生成新内容')

print('[Daily Update] 结束')
