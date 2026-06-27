"""技术中心路由"""
import markdown
from flask import Blueprint, render_template, request, abort, current_app
from models import Article
from services.seo import generate_article_schema, generate_breadcrumb_schema

technology_bp = Blueprint('technology', __name__)


@technology_bp.route('/')
def article_list():
    """技术文章列表"""
    page = request.args.get('page', 1, type=int)
    article_type = request.args.get('type', 'article')

    query = Article.query.filter_by(is_published=True)

    if article_type in ('article', 'news', 'case'):
        query = query.filter_by(article_type=article_type)

    pagination = query.order_by(Article.published_at.desc()).paginate(
        page=page, per_page=12, error_out=False
    )

    return render_template(
        'technology/list.html',
        articles=pagination.items,
        pagination=pagination,
        article_type=article_type,
        meta_title='技术中心 - 技术文章与行业动态 - 清徽半导体材料',
        meta_description='获取半导体材料领域最新技术文章、行业快讯和应用案例，了解国产替代最新进展。',
    )


@technology_bp.route('/<slug>/')
def article_detail(slug):
    """文章详情"""
    article = Article.query.filter_by(slug=slug, is_published=True).first_or_404()

    # 浏览次数+1
    article.view_count = (article.view_count or 0) + 1
    from models import db
    db.session.commit()

    # 渲染Markdown为HTML
    if article.content and not article.content_html:
        article.content_html = markdown.markdown(
            article.content,
            extensions=['extra', 'codehilite', 'toc']
        )

    # 相关文章
    related = (
        Article.query
        .filter(Article.id != article.id, Article.is_published == True, Article.article_type == article.article_type)
        .order_by(Article.published_at.desc())
        .limit(3)
        .all()
    )

    breadcrumb = [
        ('首页', '/'),
        ('技术中心', '/technology/'),
        (article.title, f'/technology/{article.slug}'),
    ]

    article_schema = generate_article_schema(article)
    breadcrumb_schema = generate_breadcrumb_schema(breadcrumb)

    return render_template(
        'technology/detail.html',
        article=article,
        related_articles=related,
        page_schema=[article_schema, breadcrumb_schema],
        meta_title=article.meta_title or article.title,
        meta_title_suffix='清徽半导体材料技术中心',
        meta_description=article.meta_description or article.summary or article.title,
    )
