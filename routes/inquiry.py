"""询盘路由"""
from flask import Blueprint, request, jsonify, render_template
from models import db, Inquiry
from services.notify import send_inquiry_notification
from datetime import datetime, timezone
import logging

logger = logging.getLogger(__name__)

inquiry_bp = Blueprint('inquiry', __name__)


@inquiry_bp.route('/', methods=['POST'])
def submit_inquiry():
    """提交询盘"""
    data = request.get_json() if request.is_json else request.form

    name = (data.get('name') or '').strip()
    if not name:
        return jsonify({'error': '请填写联系人姓名'}), 400

    phone = (data.get('phone') or '').strip()
    email = (data.get('email') or '').strip()
    if not phone and not email:
        return jsonify({'error': '请填写电话或邮箱'}), 400

    inquiry = Inquiry(
        name=name,
        company=(data.get('company') or '').strip(),
        phone=phone,
        email=email,
        product_name=(data.get('product_name') or '').strip(),
        message=(data.get('message') or '').strip(),
        source_page=(data.get('source_page') or request.referrer or ''),
        utm_source=(data.get('utm_source') or ''),
        status='new',
    )

    try:
        db.session.add(inquiry)
        db.session.commit()
        logger.info(f'新询盘已保存: {name} - {inquiry.product_name}')
    except Exception as e:
        db.session.rollback()
        logger.error(f'询盘保存失败: {e}')
        return jsonify({'error': '提交失败，请稍后重试'}), 500

    # 发送通知
    try:
        notified = send_inquiry_notification(inquiry.to_dict())
        if notified:
            inquiry.is_notified = True
            db.session.commit()
    except Exception as e:
        logger.error(f'通知发送失败: {e}')

    return jsonify({
        'success': True,
        'message': '感谢您的咨询！我们的技术团队将在24小时内与您联系。',
    })


@inquiry_bp.route('/page')
def inquiry_page():
    """独立询盘页面 (备用)"""
    product_name = request.args.get('product', '')
    return render_template(
        'contact.html',
        preselected_product=product_name,
        meta_title='技术咨询 - 清徽半导体材料',
    )
