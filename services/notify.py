"""客户询盘通知服务 - Telegram + 企业微信"""
import logging
import requests
from flask import current_app
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

TELEGRAM_API = 'https://api.telegram.org/bot{token}/sendMessage'
WECHAT_API = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={key}'


def send_inquiry_notification(inquiry_data):
    """发送询盘通知到所有已配置的渠道"""
    sent = False

    # Telegram
    token = current_app.config.get('TELEGRAM_BOT_TOKEN')
    chat_id = current_app.config.get('TELEGRAM_CHAT_ID')
    if token and chat_id:
        try:
            send_telegram(token, chat_id, inquiry_data)
            sent = True
            logger.info(f'Telegram通知已发送: {inquiry_data.get("name")}')
        except Exception as e:
            logger.error(f'Telegram通知失败: {e}')

    # 企业微信
    webhook = current_app.config.get('WECHAT_WEBHOOK_URL')
    if webhook:
        try:
            send_wechat(webhook, inquiry_data)
            sent = True
            logger.info(f'企业微信通知已发送: {inquiry_data.get("name")}')
        except Exception as e:
            logger.error(f'企业微信通知失败: {e}')

    return sent


def _format_inquiry_message(data):
    """格式化询盘消息"""
    now = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
    return (
        f'🔔 新客户询盘\n'
        f'━━━━━━━━━━━━━━\n'
        f'📅 时间: {now}\n'
        f'👤 姓名: {data.get("name", "未填写")}\n'
        f'🏢 公司: {data.get("company", "未填写")}\n'
        f'📞 电话: {data.get("phone", "未填写")}\n'
        f'📧 邮箱: {data.get("email", "未填写")}\n'
        f'📦 产品: {data.get("product_name", "未指定")}\n'
        f'📝 需求: {data.get("message", "未填写")}\n'
        f'━━━━━━━━━━━━━━\n'
        f'来源页面: {data.get("source_page", "直接访问")}'
    )


def send_telegram(token, chat_id, data):
    """发送Telegram消息"""
    text = _format_inquiry_message(data)
    url = TELEGRAM_API.format(token=token)

    resp = requests.post(
        url,
        json={
            'chat_id': chat_id,
            'text': text,
            'parse_mode': 'HTML',
            'disable_web_page_preview': True,
        },
        timeout=15,
    )
    resp.raise_for_status()
    return resp.json()


def send_wechat(webhook_url, data):
    """发送企业微信消息"""
    text = _format_inquiry_message(data)

    resp = requests.post(
        webhook_url,
        json={
            'msgtype': 'text',
            'text': {
                'content': text,
            },
        },
        timeout=15,
    )
    resp.raise_for_status()
    return resp.json()
