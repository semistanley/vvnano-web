"""产品与分类模型"""
from datetime import datetime, timezone
from . import db


class ProductCategory(db.Model):
    __tablename__ = 'product_categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, comment='分类名称')
    slug = db.Column(db.String(100), unique=True, nullable=False, comment='URL标识')
    description = db.Column(db.Text, comment='分类描述')
    icon = db.Column(db.String(200), comment='分类图标CSS类或图片路径')
    sort_order = db.Column(db.Integer, default=0, comment='排序')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    products = db.relationship('Product', backref='category', lazy='dynamic',
                               order_by='Product.sort_order')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'description': self.description,
            'icon': self.icon,
            'product_count': self.products.filter_by(is_active=True).count(),
        }

    def __repr__(self):
        return f'<ProductCategory {self.name}>'


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('product_categories.id'), nullable=False)

    name = db.Column(db.String(200), nullable=False, comment='产品名称')
    model = db.Column(db.String(100), comment='产品型号')
    slug = db.Column(db.String(200), unique=True, nullable=False, comment='URL标识')
    subtitle = db.Column(db.String(300), comment='简短副标题')
    summary = db.Column(db.Text, comment='产品简介（列表页显示）')

    # 详细描述 (Markdown格式，支持富文本)
    description = db.Column(db.Text, comment='产品描述')
    specifications = db.Column(db.Text, comment='技术参数 (JSON格式)')
    applications = db.Column(db.Text, comment='应用场景')

    # 对比数据 (JSON: {"分辨率": "0.35μm", "感光速度": "120 mJ/cm²", ...})
    comparison_data = db.Column(db.Text, comment='对比参数 (JSON)')

    # 产品图片
    image = db.Column(db.String(300), comment='主图路径')
    gallery = db.Column(db.Text, comment='产品图集 (JSON数组)')

    # SEO
    meta_title = db.Column(db.String(200))
    meta_description = db.Column(db.String(500))
    meta_keywords = db.Column(db.String(300))

    # 状态
    is_active = db.Column(db.Boolean, default=True, comment='上架')
    is_featured = db.Column(db.Boolean, default=False, comment='首页推荐')
    is_new = db.Column(db.Boolean, default=False, comment='新品标记')
    stock_status = db.Column(db.String(20), default='in_stock',
                             comment='库存: in_stock/out_of_stock/on_demand')
    sort_order = db.Column(db.Integer, default=0)

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc),
                           onupdate=lambda: datetime.now(timezone.utc))

    @property
    def specs_dict(self):
        """解析技术参数JSON"""
        if not self.specifications:
            return {}
        import json
        try:
            return json.loads(self.specifications)
        except (json.JSONDecodeError, TypeError):
            return {}

    @property
    def comparison_dict(self):
        """解析对比数据JSON"""
        if not self.comparison_data:
            return {}
        import json
        try:
            return json.loads(self.comparison_data)
        except (json.JSONDecodeError, TypeError):
            return {}

    @property
    def gallery_list(self):
        """解析图集JSON"""
        if not self.gallery:
            return []
        import json
        try:
            return json.loads(self.gallery)
        except (json.JSONDecodeError, TypeError):
            return []

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'model': self.model,
            'slug': self.slug,
            'subtitle': self.subtitle,
            'summary': self.summary,
            'category': self.category.name if self.category else None,
            'category_slug': self.category.slug if self.category else None,
            'specifications': self.specs_dict,
            'comparison_data': self.comparison_dict,
            'applications': self.applications,
            'image': self.image,
            'is_featured': self.is_featured,
            'is_new': self.is_new,
            'stock_status': self.stock_status,
        }

    def __repr__(self):
        return f'<Product {self.name}>'
