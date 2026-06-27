"""解决方案路由"""
from flask import Blueprint, render_template
from services.seo import generate_breadcrumb_schema

solutions_bp = Blueprint('solutions', __name__)

SOLUTIONS = {
    'frontend': {
        'title': '前道制程解决方案',
        'description': '为晶圆制造提供光刻胶、湿电子化学品等关键材料，适用于功率器件、MEMS、化合物半导体等前道工艺。',
        'products': ['光刻胶系列', '刻蚀气体', '湿电子化学品'],
        'applications': ['功率器件制造', 'MEMS传感器', '化合物半导体', 'CMOS图像传感器'],
    },
    'advanced-packaging': {
        'title': '先进封装解决方案',
        'description': '为2.5D/3D封装、Fan-Out封装等先进封装工艺提供电镀药水、临时键合胶等全套材料方案。',
        'products': ['电镀铜液', '电镀锡液', '先进封装材料'],
        'applications': ['TSV制造', 'RDL重布线层', 'Bump凸点制作', 'Fan-Out封装'],
    },
    'optical-module': {
        'title': '光模块封装解决方案',
        'description': '为光通信模块提供高可靠性除湿保护方案，保障光模块在复杂环境下的长期稳定性。',
        'products': ['除湿剂 (MacDermid Alpha)'],
        'applications': ['光模块内部除湿', '光器件保护', '光纤连接器'],
    },
    'research': {
        'title': '科研院所解决方案',
        'description': '为高校和科研机构提供小批量、多品种的半导体材料，支持前沿课题研发需求。',
        'products': ['光刻胶', '电镀药水', '特种气体', '高纯试剂'],
        'applications': ['新材料研究', '器件原型验证', '工艺开发', '教学实验'],
    },
}


@solutions_bp.route('/')
def solution_list():
    """解决方案列表"""
    return render_template(
        'solutions/list.html',
        solutions=SOLUTIONS,
        meta_title='解决方案 - 清徽半导体材料',
        meta_description='为前道制程、先进封装、光模块封装和科研院所提供定制化半导体材料解决方案。',
    )


@solutions_bp.route('/<slug>/')
def solution_detail(slug):
    """解决方案详情"""
    solution = SOLUTIONS.get(slug)
    if not solution:
        from flask import abort
        abort(404)

    breadcrumb = [
        ('首页', '/'),
        ('解决方案', '/solutions/'),
        (solution['title'], f'/solutions/{slug}'),
    ]

    return render_template(
        'solutions/detail.html',
        solution=solution,
        slug=slug,
        page_schema=generate_breadcrumb_schema(breadcrumb),
        meta_title=f'{solution["title"]} - 清徽半导体材料',
        meta_description=solution['description'],
    )
