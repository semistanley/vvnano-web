"""清徽半导体材料网站 - 配置文件"""
import os
import re
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))


def fix_mysql_url(url):
    """修复 Railway MySQL 连接字符串格式"""
    if not url:
        return url
    # Railway 提供 mysql://user:pass@host/db 格式
    # SQLAlchemy 需要 mysql+pymysql://user:pass@host:port/db
    if url.startswith('mysql://'):
        url = url.replace('mysql://', 'mysql+pymysql://', 1)
        # 检查是否有端口号，Railway 可能不包含端口
        # mysql+pymysql://user:pass@host/db -> 需要加端口 3306
        match = re.match(r'mysql\+pymysql://([^@]+@[^/]+)(/.*)', url)
        if match:
            host_part = match.group(1)
            if ':' not in host_part.split('@')[1]:  # 没有端口
                url = f'mysql+pymysql://{host_part}:3306{match.group(2)}'
    return url


class Config:
    # Flask
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'

    # 数据库 - 自动适配 Railway MySQL
    raw_db_url = os.environ.get('DATABASE_URL', '')
    SQLALCHEMY_DATABASE_URI = fix_mysql_url(raw_db_url) or \
        'sqlite:///' + os.path.join(basedir, 'instance', 'vvnano.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 5,
        'pool_recycle': 300,
        'pool_pre_ping': True,
    }

    # DeepSeek AI
    DEEPSEEK_API_KEY = os.environ.get('DEEPSEEK_API_KEY', '')
    DEEPSEEK_API_URL = os.environ.get(
        'DEEPSEEK_API_URL',
        'https://api.deepseek.com/v1/chat/completions'
    )
    DEEPSEEK_MODEL = os.environ.get('DEEPSEEK_MODEL', 'deepseek-chat')

    # 知识图谱 (KG Project API)
    KG_API_BASE = os.environ.get('KG_API_BASE', 'http://localhost:5001/api')
    KG_PUBLIC_STATS = os.environ.get('KG_PUBLIC_STATS', 'http://localhost:5001/api/public/stats')

    # 通知服务
    TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '')
    TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID', '')
    WECHAT_WEBHOOK_URL = os.environ.get('WECHAT_WEBHOOK_URL', '')

    # 网站基本信息
    SITE_NAME = '清徽半导体材料'
    SITE_URL = os.environ.get('SITE_URL', 'https://www.vvnano.com')
    COMPANY_NAME = '清徽（深圳）科技有限公司'
    COMPANY_ADDRESS = '深圳宝安新桥街道万科星城上郡1B栋'
    COMPANY_PHONE = '+86 13189105886'
    COMPANY_PHONE_HK = '+852 57166955'
    COMPANY_EMAIL = 'service@vvnano.com'

    # 管理后台密码
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'vvnano2025')

    # Session
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

    # 每日更新 (Railway 用自带 Cron Job)
    DAILY_UPDATE_HOUR = int(os.environ.get('DAILY_UPDATE_HOUR', '22'))
    DAILY_UPDATE_MINUTE = int(os.environ.get('DAILY_UPDATE_MINUTE', '0'))

    # 上传 - Railway 用 Volume 持久化
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', os.path.join(basedir, 'uploads'))


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig,
}
