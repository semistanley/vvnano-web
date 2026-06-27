"""清徽半导体材料网站 - Flask 应用入口"""
import os
from dotenv import load_dotenv

load_dotenv()

from flask import Flask
from config import config
from models import db


def create_app(config_name=None):
    """应用工厂"""
    if config_name is None:
        config_name = os.environ.get('FLASK_CONFIG', 'default')

    app = Flask(__name__)
    app.config.from_object(config.get(config_name, config['default']))

    # 确保必要目录存在
    os.makedirs(app.instance_path, exist_ok=True)
    os.makedirs(app.config.get('UPLOAD_FOLDER', 'uploads'), exist_ok=True)

    # 初始化扩展
    db.init_app(app)

    # 注册路由蓝图
    from routes.main import main_bp
    from routes.products import products_bp
    from routes.technology import technology_bp
    from routes.solutions import solutions_bp
    from routes.inquiry import inquiry_bp
    from routes.kg_bridge import kg_bridge_bp
    from routes.admin import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(products_bp, url_prefix='/products')
    app.register_blueprint(technology_bp, url_prefix='/technology')
    app.register_blueprint(solutions_bp, url_prefix='/solutions')
    app.register_blueprint(inquiry_bp, url_prefix='/inquiry')
    app.register_blueprint(kg_bridge_bp, url_prefix='/kg')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    # 注册错误处理器
    register_error_handlers(app)

    # 注册模板全局变量
    @app.context_processor
    def inject_globals():
        return {
            'site_name': app.config['SITE_NAME'],
            'company_name': app.config['COMPANY_NAME'],
            'company_phone': app.config['COMPANY_PHONE'],
            'company_phone_hk': app.config.get('COMPANY_PHONE_HK', ''),
            'company_email': app.config['COMPANY_EMAIL'],
            'company_address': app.config['COMPANY_ADDRESS'],
            'site_url': app.config['SITE_URL'],
            'current_year': __import__('datetime').datetime.now().year,
        }

    # 注册过滤器
    @app.template_filter('datetime')
    def format_datetime(dt, fmt='%Y-%m-%d'):
        if dt is None:
            return ''
        if dt.tzinfo is not None:
            dt = dt.replace(tzinfo=None)
        return dt.strftime(fmt)

    # 创建数据库表 (幂等操作，多次执行安全)
    with app.app_context():
        db.create_all()

    return app


def register_error_handlers(app):
    """错误页面"""

    @app.errorhandler(404)
    def not_found(e):
        from flask import render_template
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def server_error(e):
        from flask import render_template
        return render_template('errors/500.html'), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app = create_app()
    app.run(host='0.0.0.0', port=port, debug=True)
