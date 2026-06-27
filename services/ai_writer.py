"""DeepSeek AI 内容生成引擎"""
import json
import logging
import requests
from datetime import datetime, timezone
from flask import current_app

logger = logging.getLogger(__name__)

# 行业知识提示词模板
SYSTEM_PROMPT_NEWS = """你是一位半导体行业资深编辑，为清徽半导体材料网站撰写行业快讯。
要求：
1. 每篇快讯50-100字，中文，简洁专业
2. 涉及：光刻胶、电镀液、刻蚀气体、先进封装、CMP材料、国产替代等
3. 内容需基于真实的行业趋势，不要编造具体数据
4. 每天生成3条不同的快讯
5. 最后以JSON格式返回，格式：[{"title": "...", "summary": "...", "source": "..."}]
6. 不要包含markdown代码块标记，只返回纯JSON"""

SYSTEM_PROMPT_COMPARISON = """你是一位半导体材料应用工程师，为客户提供产品对比分析。
用户会提供两款产品的参数，请生成：
1. 客观的逐项对比分析
2. 清晰的优势/劣势判断
3. 针对不同应用场景的选型建议
语言：中文，专业但不晦涩，控制在200字以内"""

SYSTEM_PROMPT_ARTICLE = """你是一位半导体行业技术写手，为清徽半导体材料网站撰写技术文章。
要求：
1. 标题吸引人，包含关键搜索词
2. 正文800-1500字，Markdown格式
3. 专业准确，但避免过于学术化
4. 每篇文章至少包含一个实际应用场景
5. 如果文章涉及产品对比，保持客观中立
6. 文章末尾加一句"如需了解更多技术细节或获取样品，欢迎联系我们"""


def _call_deepseek(system_prompt, user_message, max_tokens=2000, temperature=0.7):
    """调用 DeepSeek API"""
    api_key = current_app.config.get('DEEPSEEK_API_KEY')
    if not api_key:
        logger.warning('DEEPSEEK_API_KEY 未配置，跳过AI调用')
        return None

    api_url = current_app.config.get(
        'DEEPSEEK_API_URL',
        'https://api.deepseek.com/v1/chat/completions'
    )
    model = current_app.config.get('DEEPSEEK_MODEL', 'deepseek-chat')

    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
    }

    payload = {
        'model': model,
        'messages': [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_message},
        ],
        'max_tokens': max_tokens,
        'temperature': temperature,
    }

    try:
        resp = requests.post(api_url, headers=headers, json=payload, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        content = data['choices'][0]['message']['content']
        return content.strip()
    except Exception as e:
        logger.error(f'DeepSeek API调用失败: {e}')
        return None


def generate_daily_news():
    """每日生成行业快讯"""
    from models import db, Article
    from datetime import datetime, timezone

    content = _call_deepseek(
        SYSTEM_PROMPT_NEWS,
        f'请生成{datetime.now(timezone.utc).strftime("%Y-%m-%d")}的半导体行业快讯3条',
        max_tokens=2000,
        temperature=0.7
    )

    if not content:
        logger.warning('AI未返回内容，使用默认快讯')
        return []

    # 清理可能的 markdown 代码块
    content = content.replace('```json', '').replace('```', '').strip()

    try:
        news_items = json.loads(content)
    except json.JSONDecodeError:
        logger.error(f'AI返回格式错误: {content[:200]}')
        return []

    articles = []
    for item in news_items:
        title = item.get('title', '').strip()
        summary = item.get('summary', '').strip()
        source = item.get('source', 'AI行业观察')

        if not title or not summary:
            continue

        slug = f"news-{datetime.now(timezone.utc).strftime('%Y%m%d')}-{hash(title) % 10000:04d}"

        article = Article(
            title=title,
            slug=slug,
            summary=summary,
            content=summary,
            content_html=summary.replace('\n', '<br>'),
            article_type='news',
            source=source,
            is_ai_generated=True,
            is_published=True,
            is_featured=True,
            published_at=datetime.now(timezone.utc),
        )
        db.session.add(article)
        articles.append(article)

    db.session.commit()
    logger.info(f'AI生成了 {len(articles)} 条行业快讯')
    return articles


def generate_comparison(product_a_data, product_b_data):
    """生成产品对比分析"""
    message = f"""请对比以下两款产品：

产品A: {json.dumps(product_a_data, ensure_ascii=False)}
产品B: {json.dumps(product_b_data, ensure_ascii=False)}

请给出客观的对比分析。"""

    content = _call_deepseek(
        SYSTEM_PROMPT_COMPARISON,
        message,
        max_tokens=1000,
        temperature=0.3
    )

    return content or '对比分析暂不可用，请直接联系我们的技术团队获取详细对比资料。'


def generate_product_description(product_name, specs_json, category_name):
    """AI辅助生成产品描述"""
    message = f"""请为以下半导体材料产品生成专业的产品描述（800-1500字），Markdown格式：

产品名称: {product_name}
产品类别: {category_name}
技术参数: {specs_json}

请包含：产品概述、关键技术参数解读、典型应用场景、优势特点。"""

    content = _call_deepseek(
        SYSTEM_PROMPT_ARTICLE,
        message,
        max_tokens=3000,
        temperature=0.5
    )

    return content or f'{product_name} - 请联系我们获取详细技术资料。'


def generate_article_from_kg(kg_data):
    """根据知识图谱数据生成技术文章（未来功能）"""
    message = f"""根据以下知识图谱数据，生成一篇半导体工艺技术文章：

{json.dumps(kg_data, ensure_ascii=False, indent=2)}

请写一篇800字左右的技术文章，Markdown格式。"""

    return _call_deepseek(SYSTEM_PROMPT_ARTICLE, message, max_tokens=3000, temperature=0.5)
