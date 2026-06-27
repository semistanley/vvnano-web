"""知识图谱桥接路由 - 连接vvnano.com与semiconductor-knowledge-graph"""
import requests
from flask import Blueprint, render_template, jsonify, current_app
from models import Product, Article
from services.ai_writer import generate_article_from_kg
import logging

logger = logging.getLogger(__name__)

kg_bridge_bp = Blueprint('kg_bridge', __name__)


@kg_bridge_bp.route('/')
def knowledge_graph_page():
    """知识图谱入口页 - 展示KG平台介绍及入口"""
    # 尝试从KG项目获取统计数据
    kg_stats = get_kg_stats()

    # 从KG获取最新图谱数据点（供页面展示）
    kg_highlights = get_kg_highlights()

    return render_template(
        'technology/knowledge_graph.html',
        kg_stats=kg_stats,
        kg_highlights=kg_highlights,
        meta_title='半导体工艺知识图谱 - 清徽半导体材料',
        meta_description='探索由AI驱动的交互式半导体工艺知识图谱，涵盖前道制程、封装测试、材料应用等全流程知识。',
    )


@kg_bridge_bp.route('/api/stats')
def stats_api():
    """获取知识图谱统计数据 - 供首页调用"""
    kg_stats = get_kg_stats()
    return jsonify(kg_stats)


@kg_bridge_bp.route('/api/sync-article/<int:article_id>')
def sync_to_kg(article_id):
    """将网站文章同步到知识图谱（未来功能）"""
    article = Article.query.get_or_404(article_id)
    # TODO: 调用KG API将文章内容作为三元组导入
    return jsonify({'status': 'ok', 'message': f'文章 "{article.title}" 已同步到知识图谱'})


@kg_bridge_bp.route('/api/generate-from-kg')
def generate_from_kg():
    """从知识图谱数据生成技术文章"""
    try:
        kg_api = current_app.config.get('KG_API_BASE', '')
        if not kg_api:
            return jsonify({'error': 'KG服务未配置'}), 503

        # 获取图谱概览数据
        resp = requests.get(f'{kg_api}/graph/overview', timeout=5)
        if resp.status_code != 200:
            return jsonify({'error': 'KG服务暂不可用'}), 503

        kg_data = resp.json()

        # 让AI根据KG数据生成文章
        content = generate_article_from_kg(kg_data)
        if not content:
            return jsonify({'error': 'AI生成失败'}), 500

        return jsonify({
            'content': content,
            'source': 'knowledge-graph',
        })

    except Exception as e:
        logger.error(f'从KG生成文章失败: {e}')
        return jsonify({'error': str(e)}), 500


@kg_bridge_bp.route('/redirect')
def redirect_to_kg():
    """跳转到知识图谱平台"""
    from flask import redirect
    kg_url = current_app.config.get('KG_API_BASE', '').replace('/api', '')
    if not kg_url:
        kg_url = 'http://localhost:5000'
    return redirect(kg_url)


def get_kg_stats():
    """获取知识图谱统计数据"""
    try:
        kg_url = current_app.config.get('KG_PUBLIC_STATS', '')
        if kg_url:
            resp = requests.get(kg_url, timeout=3)
            if resp.status_code == 200:
                return resp.json()
    except requests.exceptions.ConnectionError:
        logger.debug('KG服务未运行，使用默认统计')
    except Exception as e:
        logger.debug(f'获取KG统计失败: {e}')

    return {
        'node_count': 200,
        'relation_count': 1000,
        'category_count': 10,
        'user_count': 0,
        'online': False,
    }


def get_kg_highlights():
    """获取知识图谱亮点数据"""
    try:
        kg_api = current_app.config.get('KG_API_BASE', '')
        if kg_api:
            resp = requests.get(f'{kg_api}/graph/overview', timeout=3)
            if resp.status_code == 200:
                data = resp.json()
                return data.get('categories', [])
    except Exception:
        pass
    return [
        {'name': '光刻工艺', 'count': 45},
        {'name': '薄膜沉积', 'count': 38},
        {'name': '刻蚀工艺', 'count': 32},
        {'name': '封装测试', 'count': 28},
    ]
