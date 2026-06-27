# ============================================
# 清徽半导体材料网站 - 部署脚本 (Windows)
# ============================================
# 使用方法:
#   .\scripts\deploy.ps1
# ============================================

Write-Host "🚀 开始部署 清徽半导体材料网站..." -ForegroundColor Green
Write-Host ""

# 检查 Docker
try {
    docker --version | Out-Null
} catch {
    Write-Host "❌ 未安装 Docker，请先安装 Docker Desktop" -ForegroundColor Red
    exit 1
}

# 检查 .env
if (-not (Test-Path ".env")) {
    Write-Host "📝 未发现 .env 文件，从 .env.example 创建..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "⚠️  请编辑 .env 填入您的 DeepSeek API Key 和数据库密码" -ForegroundColor Yellow
    exit 1
}

# 创建必要目录
New-Item -ItemType Directory -Force -Path "static\images" | Out-Null
New-Item -ItemType Directory -Force -Path "instance" | Out-Null
New-Item -ItemType Directory -Force -Path "uploads" | Out-Null

Write-Host "📦 构建并启动服务..." -ForegroundColor Cyan
docker compose up -d --build

Write-Host ""
Write-Host "⏳ 等待服务启动..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# 检查服务状态
$webStatus = docker compose ps web --format json | ConvertFrom-Json
if ($webStatus.State -eq "running") {
    Write-Host "✅ Web 服务已启动" -ForegroundColor Green
} else {
    Write-Host "❌ Web 服务启动失败，查看日志: docker compose logs web" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "🌐 初始化产品数据..." -ForegroundColor Cyan
docker compose exec web python scripts/seed_products.py

Write-Host ""
Write-Host "======================================" -ForegroundColor Green
Write-Host "✅ 部署完成！" -ForegroundColor Green
Write-Host "🌐 网站地址: http://localhost:5000" -ForegroundColor Cyan
Write-Host "🔧 管理后台: http://localhost:5000/admin/" -ForegroundColor Cyan
Write-Host ""
Write-Host "📋 常用命令:" -ForegroundColor Yellow
Write-Host "   查看日志: docker compose logs -f web" -ForegroundColor White
Write-Host "   重启服务: docker compose restart web" -ForegroundColor White
Write-Host "   停止服务: docker compose down" -ForegroundColor White
Write-Host "======================================" -ForegroundColor Green
