"""SEO 工具服务"""
import json
from datetime import datetime, timezone
from flask import current_app, url_for


def generate_product_schema(product):
    """生成产品的 Schema.org (Product) 结构化数据"""
    site_url = current_app.config['SITE_URL']

    schema = {
        '@context': 'https://schema.org',
        '@type': 'Product',
        'name': product.name,
        'description': product.summary or product.name,
        'sku': product.model or str(product.id),
        'category': product.category.name if product.category else '半导体材料',
        'url': f'{site_url}/products/{product.slug}',
        'offers': {
            '@type': 'Offer',
            'availability': 'https://schema.org/InStock' if product.stock_status == 'in_stock'
                           else 'https://schema.org/OutOfStock',
            'price': '0',
            'priceCurrency': 'CNY',
        },
    }

    if product.image:
        schema['image'] = f'{site_url}/static/images/{product.image}'

    return schema


def generate_article_schema(article):
    """生成文章的 Schema.org (Article) 结构化数据"""
    site_url = current_app.config['SITE_URL']

    return {
        '@context': 'https://schema.org',
        '@type': 'Article',
        'headline': article.title,
        'description': article.summary or article.title,
        'url': f'{site_url}/technology/{article.slug}',
        'datePublished': article.published_at.isoformat() if article.published_at else None,
        'dateModified': article.updated_at.isoformat() if article.updated_at else None,
        'author': {
            '@type': 'Organization',
            'name': current_app.config['COMPANY_NAME'],
        },
    }


def generate_organization_schema():
    """生成企业信息 Schema.org"""
    return {
        '@context': 'https://schema.org',
        '@type': 'Organization',
        'name': current_app.config['COMPANY_NAME'],
        'url': current_app.config['SITE_URL'],
        'telephone': current_app.config['COMPANY_PHONE'],
        'email': current_app.config['COMPANY_EMAIL'],
        'address': {
            '@type': 'PostalAddress',
            'addressLocality': '深圳',
            'addressRegion': '广东',
            'addressCountry': 'CN',
        },
    }


def generate_breadcrumb_schema(items):
    """生成面包屑导航 Schema.org"""
    site_url = current_app.config['SITE_URL']

    item_list = []
    for i, (name, url_path) in enumerate(items):
        item_list.append({
            '@type': 'ListItem',
            'position': i + 1,
            'name': name,
            'item': f'{site_url}{url_path}',
        })

    return {
        '@context': 'https://schema.org',
        '@type': 'BreadcrumbList',
        'itemListElement': item_list,
    }


def generate_sitemap(app):
    """生成 sitemap.xml 内容"""
    from models import Product, Article

    pages = []

    # 静态页面
    static_urls = ['/', '/products/', '/technology/', '/solutions/', '/about/', '/contact/', '/kg/']
    for url in static_urls:
        pages.append({
            'loc': app.config['SITE_URL'] + url,
            'changefreq': 'weekly',
            'priority': '0.9' if url == '/' else '0.7',
        })

    # 产品页
    with app.app_context():
        products = Product.query.filter_by(is_active=True).all()
        for p in products:
            pages.append({
                'loc': f'{app.config["SITE_URL"]}/products/{p.slug}',
                'changefreq': 'monthly',
                'priority': '0.8',
                'lastmod': p.updated_at.strftime('%Y-%m-%d') if p.updated_at else None,
            })

        # 文章页
        articles = Article.query.filter_by(is_published=True).all()
        for a in articles:
            pages.append({
                'loc': f'{app.config["SITE_URL"]}/technology/{a.slug}',
                'changefreq': 'monthly',
                'priority': '0.6',
                'lastmod': a.published_at.strftime('%Y-%m-%d') if a.published_at else None,
            })

    # 生成 XML
    xml_parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]

    for page in pages:
        xml_parts.append('  <url>')
        xml_parts.append(f'    <loc>{page["loc"]}</loc>')
        xml_parts.append(f'    <changefreq>{page["changefreq"]}</changefreq>')
        xml_parts.append(f'    <priority>{page["priority"]}</priority>')
        if page.get('lastmod'):
            xml_parts.append(f'    <lastmod>{page["lastmod"]}</lastmod>')
        xml_parts.append('  </url>')

    xml_parts.append('</urlset>')
    return '\n'.join(xml_parts)
