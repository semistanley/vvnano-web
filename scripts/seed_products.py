"""初始化产品数据种子脚本"""
import sys
import os

# Windows console UTF-8 support
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from models import db, Product, ProductCategory, Article
import json
from datetime import datetime, timezone

app = create_app()

with app.app_context():
    print('🌱 开始初始化产品数据...')

    # ==================== 创建产品分类 ====================
    categories = [
        {'name': '光刻胶', 'slug': 'photoresist', 'description': '高性能光刻胶系列，适用于多种工艺节点', 'icon': 'bi-droplet', 'sort_order': 1},
        {'name': '电镀药水', 'slug': 'electroplating', 'description': '电镀铜液、锡液等电镀化学品', 'icon': 'bi-water', 'sort_order': 2},
        {'name': '刻蚀气体', 'slug': 'etching-gas', 'description': '高纯刻蚀气体，适用于介质刻蚀和金属刻蚀', 'icon': 'bi-wind', 'sort_order': 3},
        {'name': '除湿材料', 'slug': 'desiccant', 'description': '光模块及精密器件除湿保护方案', 'icon': 'bi-moisture', 'sort_order': 4},
    ]

    for cat_data in categories:
        existing = ProductCategory.query.filter_by(slug=cat_data['slug']).first()
        if not existing:
            cat = ProductCategory(**cat_data)
            db.session.add(cat)
            print(f'  ✅ 创建分类: {cat_data["name"]}')
        else:
            print(f'  ⏭️  分类已存在: {cat_data["name"]}')

    db.session.commit()

    # ==================== 创建产品 ====================
    products = [
        {
            'category_slug': 'photoresist',
            'name': 'PR-2000 i-line 正性光刻胶',
            'model': 'PR-2000',
            'slug': 'pr-2000-i-line-photoresist',
            'subtitle': '适用于0.35μm及以上工艺节点的高性能i-line光刻胶',
            'summary': 'PR-2000是一款高性能i-line正性光刻胶，适用于功率器件、MEMS和化合物半导体等应用场景。具有优异的分辨率、膜厚均匀性和热稳定性。',
            'specifications': {
                '类型': 'i-line 正性光刻胶',
                '适用工艺节点': '≥0.35μm',
                '分辨率': '0.35μm',
                '感光速度': '120 mJ/cm²',
                '膜厚均匀性': '<3%',
                '热稳定性 (Tg)': '180°C',
                '金属离子含量': '<10ppb',
                '存储期限': '12个月',
                '适用设备': 'Nikon/Canon i-line步进式光刻机',
            },
            'comparison_data': {
                '分辨率': '0.35μm',
                '感光速度': '120 mJ/cm²',
                '膜厚均匀性': '优 (<3%)',
                '热稳定性': '优 (180°C)',
                '金属离子含量': '<10ppb',
                '价格竞争力': '★★★★★',
                '供货周期': '2周',
                '技术支持': '本地团队',
            },
            'applications': '功率器件制造\nMEMS传感器\n化合物半导体\nCMOS图像传感器\n',
            'is_featured': True,
            'is_new': True,
            'stock_status': 'in_stock',
            'sort_order': 1,
        },
        {
            'category_slug': 'photoresist',
            'name': 'PR-3000i KrF 光刻胶',
            'model': 'PR-3000i',
            'slug': 'pr-3000i-krf-photoresist',
            'subtitle': '适用于90nm节点的KrF深紫外光刻胶',
            'summary': 'PR-3000i是一款高性能KrF光刻胶，适用于90nm节点逻辑和存储器件制造。具有优异的线宽粗糙度(LWR)控制和刻蚀选择性。',
            'specifications': {
                '类型': 'KrF 正性光刻胶',
                '适用工艺节点': '90nm',
                '分辨率': '90nm',
                '感光速度': '35 mJ/cm²',
                '膜厚均匀性': '<2%',
                '热稳定性 (Tg)': '200°C',
                '金属离子含量': '<5ppb',
                '存储期限': '12个月',
                '适用设备': 'ASML/Nikon KrF扫描式光刻机',
            },
            'comparison_data': {
                '分辨率': '90nm',
                '感光速度': '35 mJ/cm²',
                '膜厚均匀性': '优 (<2%)',
                '热稳定性': '优 (200°C)',
                '金属离子含量': '<5ppb',
                '价格竞争力': '★★★★☆',
                '供货周期': '3周',
                '技术支持': '本地团队',
            },
            'applications': '逻辑器件制造\n存储器件\n先进封装RDL',
            'is_featured': True,
            'stock_status': 'in_stock',
            'sort_order': 2,
        },
        {
            'category_slug': 'photoresist',
            'name': 'PR-1000krf ArF 光刻胶',
            'model': 'PR-1000krf',
            'slug': 'pr-1000krf-arf-photoresist',
            'subtitle': '适用于28nm节点的ArF浸没式光刻胶',
            'summary': 'PR-1000krf是一款先进的ArF浸没式光刻胶，适用于28nm及以下关键层的光刻工艺。具有极高的分辨率和极低的缺陷率。',
            'specifications': {
                '类型': 'ArF 浸没式光刻胶',
                '适用工艺节点': '28nm',
                '分辨率': '28nm',
                '感光速度': '22 mJ/cm²',
                '膜厚均匀性': '<1.5%',
                '热稳定性 (Tg)': '220°C',
                '金属离子含量': '<1ppb',
                '存储期限': '9个月',
                '适用设备': 'ASML NXT系列浸没式光刻机',
            },
            'comparison_data': {
                '分辨率': '28nm',
                '感光速度': '22 mJ/cm²',
                '膜厚均匀性': '极优 (<1.5%)',
                '热稳定性': '极优 (220°C)',
                '金属离子含量': '<1ppb',
                '价格竞争力': '★★★☆☆',
                '供货周期': '4周',
                '技术支持': '原厂+本地',
            },
            'applications': '先进逻辑节点\nFinFET制造\n低功耗器件',
            'is_featured': True,
            'is_new': True,
            'stock_status': 'on_demand',
            'sort_order': 3,
        },
        {
            'category_slug': 'electroplating',
            'name': 'EC-100 电镀铜液',
            'model': 'EC-100',
            'slug': 'ec-100-copper-plating',
            'subtitle': '高性能TSV填充电镀铜液',
            'summary': 'EC-100是一款专门用于TSV（硅通孔）填充的电镀铜液，具有优异的深孔填充能力、均匀的沉积速率和高纯度。',
            'specifications': {
                '类型': '酸性电镀铜液',
                '适用工艺': 'TSV填充、RDL重布线层',
                '深宽比': '≥10:1',
                '沉积速率': '0.5-2 μm/min',
                '铜纯度': '≥99.99%',
                '应力': '<20 MPa',
                '有机添加剂量': '可调',
                '工作温度': '20-30°C',
            },
            'comparison_data': {
                '深孔填充能力': '≥10:1 深宽比',
                '沉积速率': '0.5-2 μm/min',
                '铜纯度': '≥99.99%',
                '膜厚均匀性': '优',
                '应力控制': '<20 MPa',
                '价格竞争力': '★★★★☆',
                '供货周期': '2周',
                '技术支持': '工艺工程师支持',
            },
            'applications': 'TSV硅通孔填充\nRDL重布线层\nBump凸点制作\n中介层(Interposer)',
            'is_featured': True,
            'stock_status': 'in_stock',
            'sort_order': 4,
        },
        {
            'category_slug': 'electroplating',
            'name': 'EC-200 电镀锡液',
            'model': 'EC-200',
            'slug': 'ec-200-tin-plating',
            'subtitle': '高可靠性凸点电镀锡液',
            'summary': 'EC-200是一款用于先进封装凸点制作的电镀锡液，适用于锡银(Sn-Ag)合金凸点的电镀沉积。',
            'specifications': {
                '类型': '锡合金电镀液',
                '适用工艺': 'Bump凸点、μBump',
                '合金成分': 'Sn-Ag (可调)',
                '沉积速率': '0.3-1.5 μm/min',
                '纯度': '≥99.99%',
                '应力': '<25 MPa',
                '工作温度': '25-35°C',
            },
            'comparison_data': {
                '合金成分': 'Sn-Ag可调',
                '沉积速率': '0.3-1.5 μm/min',
                '纯度': '≥99.99%',
                '凸点高度均匀性': '优',
                '焊接可靠性': '高',
                '价格竞争力': '★★★★☆',
                '供货周期': '2周',
            },
            'applications': 'Flip Chip凸点\nμBump微凸点\nFan-Out封装',
            'stock_status': 'in_stock',
            'sort_order': 5,
        },
        {
            'category_slug': 'etching-gas',
            'name': 'EG-200 刻蚀气体',
            'model': 'EG-200',
            'slug': 'eg-200-etching-gas',
            'subtitle': '高纯介质刻蚀气体',
            'summary': 'EG-200是一种高纯刻蚀气体，适用于介质刻蚀工艺。具有高刻蚀速率、优异的选择比和低污染特性。',
            'specifications': {
                '类型': '高纯刻蚀气体',
                '纯度': '≥99.999%',
                '适用工艺': '介质刻蚀、金属刻蚀',
                '金属杂质': '<1ppb',
                '水分含量': '<0.5ppm',
                '包装规格': '44L/47L钢瓶',
                '供应形式': '瓶装/散装',
            },
            'comparison_data': {
                '纯度': '≥99.999%',
                '金属杂质': '<1ppb',
                '水分含量': '<0.5ppm',
                '刻蚀速率': '高',
                '选择比': '优',
                '价格竞争力': '★★★★★',
                '供货周期': '现货',
            },
            'applications': '介质刻蚀\n金属刻蚀\nMEMS释放工艺',
            'is_featured': True,
            'stock_status': 'in_stock',
            'sort_order': 6,
        },
        {
            'category_slug': 'desiccant',
            'name': 'DA-1500 光模块除湿剂',
            'model': 'DA-1500 (MacDermid Alpha)',
            'slug': 'da-1500-desiccant',
            'subtitle': '光模块及精密器件内部除湿保护方案',
            'summary': 'DA-1500是一款专为光通信模块设计的高性能除湿剂，可有效吸收模块内部微量水分，保障光模块在复杂环境下的长期可靠性。MacDermid Alpha品牌，品质保证。',
            'specifications': {
                '品牌': 'MacDermid Alpha (洽谈中)',
                '类型': '化学吸附式除湿剂',
                '适用场景': '光模块内部除湿',
                '吸湿容量': '≥30% (自重的30%)',
                '工作温度范围': '-40°C 至 +85°C',
                '封装形式': '片状/颗粒状',
                'ROHS': '符合',
                'REACH': '符合',
            },
            'comparison_data': {
                '吸湿容量': '≥30%',
                '工作温度': '-40~85°C',
                'ROHS合规': '是',
                'REACH合规': '是',
                '品牌': 'MacDermid Alpha',
                '供货周期': '需确认',
            },
            'applications': '光收发模块除湿\n光器件内部保护\n光纤连接器\n精密电子封装',
            'is_featured': True,
            'is_new': True,
            'stock_status': 'on_demand',
            'sort_order': 7,
        },
    ]

    for prod_data in products:
        cat_slug = prod_data.pop('category_slug')
        category = ProductCategory.query.filter_by(slug=cat_slug).first()
        if not category:
            print(f'  ❌ 分类不存在: {cat_slug}')
            continue

        existing = Product.query.filter_by(slug=prod_data['slug']).first()
        if existing:
            print(f'  ⏭️  产品已存在: {prod_data["name"]}')
            continue

        product = Product(
            category_id=category.id,
            specifications=json.dumps(prod_data.pop('specifications', {}), ensure_ascii=False),
            comparison_data=json.dumps(prod_data.pop('comparison_data', {}), ensure_ascii=False),
            **prod_data
        )
        db.session.add(product)
        print(f'  ✅ 创建产品: {product.name}')

    db.session.commit()
    print('')
    print('✅ 产品数据初始化完成!')
    print(f'   📦 分类: {ProductCategory.query.count()} 个')
    print(f'   📦 产品: {Product.query.count()} 个')
