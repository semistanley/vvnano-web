"""产品中心路由"""
import json
from flask import Blueprint, render_template, request, jsonify, current_app
from models import Product, ProductCategory
from services.ai_writer import generate_comparison
from services.seo import generate_product_schema, generate_breadcrumb_schema

products_bp = Blueprint('products', __name__)


@products_bp.route('/')
def product_list():
    """产品列表页"""
    category_slug = request.args.get('category', '')
    query = Product.query.filter_by(is_active=True)

    if category_slug:
        category = ProductCategory.query.filter_by(slug=category_slug).first()
        if category:
            query = query.filter_by(category_id=category.id)

    products = query.order_by(Product.category_id, Product.sort_order).all()
    categories = ProductCategory.query.filter_by(is_active=True).order_by(ProductCategory.sort_order).all()

    current_category = None
    if category_slug:
        current_category = ProductCategory.query.filter_by(slug=category_slug).first()

    breadcrumb = [
        ('首页', '/'),
        ('产品中心', '/products/'),
    ]
    if current_category:
        breadcrumb.append((current_category.name, f'/products/?category={current_category.slug}'))

    breadcrumb_schema = generate_breadcrumb_schema(breadcrumb)

    return render_template(
        'products/list.html',
        products=products,
        categories=categories,
        current_category=current_category,
        page_schema=breadcrumb_schema,
        meta_title=f'{current_category.name} - ' if current_category else '',
        meta_title_suffix='清徽半导体材料产品中心',
        meta_description=f'浏览{current_category.name}产品' if current_category else '浏览清徽半导体材料全系列产品，包括光刻胶、电镀药水、刻蚀气体等。',
    )


@products_bp.route('/<slug>/')
def product_detail(slug):
    """产品详情页"""
    product = Product.query.filter_by(slug=slug, is_active=True).first_or_404()

    # 同类产品推荐
    related = (
        Product.query
        .filter(Product.category_id == product.category_id, Product.id != product.id, Product.is_active == True)
        .limit(4)
        .all()
    )

    breadcrumb = [
        ('首页', '/'),
        ('产品中心', '/products/'),
        (product.category.name, f'/products/?category={product.category.slug}') if product.category else ('', ''),
        (product.name, f'/products/{product.slug}'),
    ]

    product_schema = generate_product_schema(product)
    breadcrumb_schema = generate_breadcrumb_schema(breadcrumb)

    return render_template(
        'products/detail.html',
        product=product,
        related_products=related,
        page_schema=[product_schema, breadcrumb_schema],
        meta_title=f'{product.name} - {product.model}' if product.model else product.name,
        meta_title_suffix='清徽半导体材料',
        meta_description=product.summary or f'{product.name}技术参数和应用',
    )


@products_bp.route('/compare/')
def compare_tool():
    """技术对比工具页面"""
    categories = ProductCategory.query.filter_by(is_active=True).order_by(ProductCategory.sort_order).all()
    products = Product.query.filter_by(is_active=True).order_by(Product.category_id, Product.sort_order).all()

    return render_template(
        'products/compare.html',
        categories=categories,
        products=products,
        meta_title='半导体材料技术对比工具 - 清徽半导体材料',
        meta_description='在线对比不同半导体材料方案的性能参数，AI智能分析为您推荐最优选型。',
    )


@products_bp.route('/api/compare', methods=['POST'])
def compare_api():
    """对比API - AI分析两款产品的差异"""
    data = request.get_json()
    product_ids = data.get('product_ids', [])

    if len(product_ids) < 2:
        return jsonify({'error': '请至少选择两款产品进行对比'}), 400

    products = Product.query.filter(Product.id.in_(product_ids)).all()
    if len(products) < 2:
        return jsonify({'error': '未找到所选产品'}), 404

    # 准备对比数据
    comparison_table = []
    product_a_data = products[0].to_dict()
    product_b_data = products[1].to_dict()

    # 合并所有参数键
    all_keys = set()
    for p in products:
        all_keys.update(p.comparison_dict.keys())
    all_keys = sorted(all_keys)

    for key in all_keys:
        row = {'param': key}
        for p in products:
            row[f'product_{p.id}'] = p.comparison_dict.get(key, '-')
        comparison_table.append(row)

    # AI对比分析
    ai_analysis = generate_comparison(product_a_data, product_b_data)

    return jsonify({
        'products': [p.to_dict() for p in products],
        'comparison_table': comparison_table,
        'ai_analysis': ai_analysis,
    })


@products_bp.route('/api/products')
def products_api():
    """获取产品列表 (JSON API)"""
    category_slug = request.args.get('category', '')
    query = Product.query.filter_by(is_active=True)

    if category_slug:
        category = ProductCategory.query.filter_by(slug=category_slug).first()
        if category:
            query = query.filter_by(category_id=category.id)

    products = query.order_by(Product.sort_order).all()
    return jsonify([p.to_dict() for p in products])
