#!/bin/bash
# ============================================
# 清徽半导体材料网站 - 部署脚本
# ============================================
# 使用方法:
#   chmod +x scripts/deploy.sh
#   ./scripts/deploy.sh
# ============================================

set -e

echo "🚀 开始部署 清徽半导体材料网站..."
echo ""

# 检查 Docker
if ! command -v docker &> /dev/null; then
    echo "❌ 未安装 Docker，请先安装 Docker"
    exit 1
fi

if ! command -v docker compose &> /dev/null; then
    echo "⚠️  docker compose 不可用，尝试 docker-compose..."
    COMPOSE_CMD="docker-compose"
else
    COMPOSE_CMD="docker compose"
fi

# 检查 .env
if [ ! -f .env ]; then
    echo "📝 未发现 .env 文件，从 .env.example 创建..."
    cp .env.example .env
    echo "⚠️  请编辑 .env 填入您的 DeepSeek API Key 和数据库密码"
    exit 1
fi

# 创建必要目录
mkdir -p static/images instance uploads

echo "📦 构建并启动服务..."
$COMPOSE_CMD up -d --build

echo ""
echo "⏳ 等待服务启动..."
sleep 5

# 检查服务状态
if $COMPOSE_CMD ps web | grep -q "Up"; then
    echo "✅ Web 服务已启动"
else
    echo "❌ Web 服务启动失败，查看日志: $COMPOSE_CMD logs web"
    exit 1
fi

if $COMPOSE_CMD ps db | grep -q "Up"; then
    echo "✅ 数据库已启动"
else
    echo "❌ 数据库启动失败，查看日志: $COMPOSE_CMD logs db"
    exit 1
fi

echo ""
echo "🌐 初始化产品数据..."
$COMPOSE_CMD exec web python scripts/seed_products.py

echo ""
echo "======================================"
echo "✅ 部署完成！"
echo "🌐 网站地址: http://localhost:5000"
echo "🔧 管理后台: http://localhost:5000/admin/"
echo ""
echo "📋 常用命令:"
echo "   查看日志: $COMPOSE_CMD logs -f web"
echo "   重启服务: $COMPOSE_CMD restart web"
echo "   停止服务: $COMPOSE_CMD down"
echo "======================================"
