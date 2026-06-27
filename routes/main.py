"""首页路由"""
from flask import Blueprint, render_template, current_app
from models import Product, Article, ProductCategory
from services.seo import generate_organization_schema

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """首页"""
    # 推荐产品
    featured_products = (
        Product.query
        .filter_by(is_active=True, is_featured=True)
        .order_by(Product.sort_order)
        .limit(4)
        .all()
    )

    # 如果推荐产品不足4个，补充普通产品
    if len(featured_products) < 4:
        existing_ids = [p.id for p in featured_products]
        extra = (
            Product.query
            .filter(Product.is_active == True, ~Product.id.in_(existing_ids))
            .order_by(Product.sort_order)
            .limit(4 - len(featured_products))
            .all()
        )
        featured_products.extend(extra)

    # 最新行业快讯 (AI生成的news类型)
    latest_news = (
        Article.query
        .filter_by(is_published=True, article_type='news')
        .order_by(Article.published_at.desc())
        .limit(3)
        .all()
    )

    # 最新技术文章
    latest_articles = (
        Article.query
        .filter_by(is_published=True, article_type='article')
        .order_by(Article.published_at.desc())
        .limit(4)
        .all()
    )

    # 产品分类
    categories = ProductCategory.query.filter_by(is_active=True).order_by(ProductCategory.sort_order).all()

    # 知识图谱统计信息 (从KG API获取)
    kg_stats = get_kg_stats()

    # Schema结构化数据
    org_schema = generate_organization_schema()

    return render_template(
        'index.html',
        featured_products=featured_products,
        latest_news=latest_news,
        latest_articles=latest_articles,
        categories=categories,
        kg_stats=kg_stats,
        page_schema=org_schema,
        meta_title='清徽半导体材料 - 专业半导体化学品供应商',
        meta_description='清徽(深圳)科技有限公司为全球半导体行业提供高性能光刻胶、电镀药水、刻蚀气体等关键材料，助力国产替代与先进制程发展。',
    )


@main_bp.route('/about/')
def about():
    """关于我们"""
    return render_template(
        'about.html',
        meta_title='关于我们 - 清徽半导体材料',
        meta_description='清徽(深圳)科技有限公司是一家致力于半导体材料解决方案国产替代的专业电子化学品材料公司。',
    )


@main_bp.route('/contact/')
def contact():
    """联系我们"""
    return render_template(
        'contact.html',
        meta_title='联系我们 - 清徽半导体材料',
        meta_description='联系清徽半导体材料，获取专业半导体材料解决方案。',
    )


def get_kg_stats():
    """从知识图谱项目获取统计数据"""
    try:
        import requests
        kg_url = current_app.config.get('KG_PUBLIC_STATS', '')
        if kg_url:
            resp = requests.get(kg_url, timeout=3)
            if resp.status_code == 200:
                return resp.json()
    except Exception:
        pass
    return {'node_count': 200, 'relation_count': 1000, 'category_count': 10}
