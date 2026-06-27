"""技术文章模型"""
from datetime import datetime, timezone
from . import db


class Article(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False, comment='标题')
    slug = db.Column(db.String(300), unique=True, nullable=False, comment='URL标识')
    summary = db.Column(db.Text, comment='摘要')
    content = db.Column(db.Text, comment='正文 (Markdown)')
    content_html = db.Column(db.Text, comment='正文 (HTML渲染后)')

    # 分类: article=技术文章, news=行业快讯, case=应用案例
    article_type = db.Column(db.String(20), default='article', index=True)

    # 封面图
    cover_image = db.Column(db.String(300), comment='封面图')

    # 来源
    source = db.Column(db.String(200), comment='文章来源')
    source_url = db.Column(db.String(500), comment='原文链接')
    is_ai_generated = db.Column(db.Boolean, default=False, comment='AI生成')

    # SEO
    meta_title = db.Column(db.String(200))
    meta_description = db.Column(db.String(500))

    # 关联产品 (可选)
    related_product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=True)
    related_product = db.relationship('Product', backref='articles', lazy=True)

    # 状态
    is_published = db.Column(db.Boolean, default=False)
    is_featured = db.Column(db.Boolean, default=False, comment='首页推荐')
    view_count = db.Column(db.Integer, default=0)

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    published_at = db.Column(db.DateTime, nullable=True)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc),
                           onupdate=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'slug': self.slug,
            'summary': self.summary,
            'article_type': self.article_type,
            'cover_image': self.cover_image,
            'is_ai_generated': self.is_ai_generated,
            'is_featured': self.is_featured,
            'view_count': self.view_count,
            'published_at': self.published_at.isoformat() if self.published_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return f'<Article {self.title[:30]}>'
