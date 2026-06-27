"""客户询盘模型"""
from datetime import datetime, timezone
from . import db


class Inquiry(db.Model):
    __tablename__ = 'inquiries'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, comment='联系人')
    company = db.Column(db.String(200), comment='公司名称')
    phone = db.Column(db.String(50), comment='电话')
    email = db.Column(db.String(200), comment='邮箱')
    product_name = db.Column(db.String(200), comment='咨询产品')
    message = db.Column(db.Text, comment='需求描述')

    # 来源追踪
    source_page = db.Column(db.String(300), comment='来源页面')
    utm_source = db.Column(db.String(100), comment='UTM标记')

    # 状态
    status = db.Column(db.String(20), default='new',
                       comment='状态: new/contacted/closed')
    is_notified = db.Column(db.Boolean, default=False, comment='是否已通知')
    notes = db.Column(db.Text, comment='跟进备注')

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'company': self.company,
            'phone': self.phone,
            'email': self.email,
            'product_name': self.product_name,
            'message': self.message,
            'source_page': self.source_page,
            'status': self.status,
            'is_notified': self.is_notified,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return f'<Inquiry {self.name} - {self.product_name}>'
