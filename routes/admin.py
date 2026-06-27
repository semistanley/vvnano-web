"""管理后台路由 - 简单后台管理"""
import json
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, current_app
from models import db, Product, ProductCategory, Article, Inquiry
from services.ai_writer import generate_daily_news, generate_product_description
from datetime import datetime, timezone

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    """简易登录 (生产环境建议增加更安全的认证)"""
    if request.method == 'POST':
        password = request.form.get('password', '')
        admin_pw = current_app.config.get('ADMIN_PASSWORD', 'vvnano2025')
        if password == admin_pw:
            from flask import session
            session['admin_logged_in'] = True
            return redirect(url_for('admin.dashboard'))
        return render_template('admin/login.html', error='密码错误')
    return render_template('admin/login.html')


@admin_bp.route('/')
def dashboard():
    """后台仪表盘"""
    from flask import session
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.login'))

    product_count = Product.query.count()
    article_count = Article.query.filter_by(is_published=True).count()
    inquiry_count = Inquiry.query.filter_by(status='new').count()

    recent_inquiries = Inquiry.query.order_by(Inquiry.created_at.desc()).limit(10).all()

    return render_template(
        'admin/dashboard.html',
        product_count=product_count,
        article_count=article_count,
        inquiry_count=inquiry_count,
        recent_inquiries=recent_inquiries,
    )


@admin_bp.route('/inquiries')
def inquiry_list():
    """询盘列表"""
    from flask import session
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.login'))

    inquiries = Inquiry.query.order_by(Inquiry.created_at.desc()).all()
    return render_template('admin/inquiries.html', inquiries=inquiries)


@admin_bp.route('/inquiry/<int:id>/status', methods=['POST'])
def update_inquiry_status(id):
    """更新询盘状态"""
    inquiry = Inquiry.query.get_or_404(id)
    inquiry.status = request.form.get('status', 'contacted')
    db.session.commit()
    return jsonify({'success': True})


@admin_bp.route('/ai/generate-news', methods=['POST'])
def trigger_ai_news():
    """手动触发AI生成行业快讯"""
    articles = generate_daily_news()
    return jsonify({'success': True, 'count': len(articles)})


@admin_bp.route('/ai/generate-description/<int:product_id>', methods=['POST'])
def trigger_ai_description(product_id):
    """AI生成产品描述"""
    product = Product.query.get_or_404(product_id)
    description = generate_product_description(
        product.name,
        json.dumps(product.specs_dict, ensure_ascii=False),
        product.category.name if product.category else ''
    )
    if description:
        product.description = description
        db.session.commit()
        return jsonify({'success': True, 'description': description[:200] + '...'})
    return jsonify({'success': False, 'error': 'AI生成失败'}), 500
