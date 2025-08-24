#!/bin/bash

# Celery RabbitMQ Demo 启动脚本

echo "🚀 启动 Celery RabbitMQ Demo..."

# 检查 Docker 是否运行
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker 未运行，请先启动 Docker"
    exit 1
fi

# 构建并启动所有服务
echo "📦 构建和启动服务..."
docker-compose up --build -d

# 等待服务启动
echo "⏳ 等待服务启动..."
sleep 10

# 检查服务状态
echo "🔍 检查服务状态..."
docker-compose ps

echo ""
echo "✅ 服务启动完成!"
echo ""
echo "🌐 访问地址:"
echo "   FastAPI 应用: http://localhost:8000"
echo "   FastAPI 文档: http://localhost:8000/docs"
echo "   Flower 监控: http://localhost:5555"
echo "   RabbitMQ 管理: http://localhost:15672 (admin/admin123)"
echo ""
echo "📊 运行演示:"
echo "   curl -X POST http://localhost:8000/demo/run-concurrent-tasks"
echo ""
echo "🛑 停止服务:"
echo "   docker-compose down"
echo ""
