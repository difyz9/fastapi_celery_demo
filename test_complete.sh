#!/bin/bash

# 完整功能测试脚本

BASE_URL="http://localhost:8000"

echo "🎉 Celery RabbitMQ Demo - 完整功能测试"
echo "======================================="

# 1. 健康检查
echo "1️⃣ 健康检查..."
health_check=$(curl -s "$BASE_URL/health")
echo "✅ 健康状态: $health_check"
echo ""

# 2. 提交各种类型的任务
echo "2️⃣ 提交各种类型的任务..."

# 快速计算任务
echo "📊 快速计算任务..."
quick_response=$(curl -s -X POST "$BASE_URL/tasks/quick" \
  -H "Content-Type: application/json" \
  -d '{"numbers": [10, 20, 30, 40, 50]}')
quick_task_id=$(echo $quick_response | python3 -c "import sys, json; print(json.load(sys.stdin)['task_id'])")
echo "   任务ID: $quick_task_id"

# 邮件任务
echo "📧 邮件发送任务..."
email_response=$(curl -s -X POST "$BASE_URL/tasks/email" \
  -H "Content-Type: application/json" \
  -d '{"recipient": "test@example.com", "subject": "测试邮件", "message": "这是一封功能测试邮件"}')
email_task_id=$(echo $email_response | python3 -c "import sys, json; print(json.load(sys.stdin)['task_id'])")
echo "   任务ID: $email_task_id"

# 批量处理任务
echo "👥 批量用户处理任务..."
batch_response=$(curl -s -X POST "$BASE_URL/tasks/batch" \
  -H "Content-Type: application/json" \
  -d '{"user_ids": [1, 2, 3]}')
batch_task_id=$(echo $batch_response | python3 -c "import sys, json; print(json.load(sys.stdin)['task_id'])")
echo "   任务ID: $batch_task_id"

# API获取任务
echo "🌐 API数据获取任务..."
api_response=$(curl -s -X POST "$BASE_URL/tasks/api-fetch" \
  -H "Content-Type: application/json" \
  -d '{"urls": ["https://httpbin.org/delay/1", "https://httpbin.org/delay/2"]}')
api_task_id=$(echo $api_response | python3 -c "import sys, json; print(json.load(sys.stdin)['task_id'])")
echo "   任务ID: $api_task_id"

# 长时间任务
echo "⏱️  长时间运行任务..."
long_response=$(curl -s -X POST "$BASE_URL/tasks/long" \
  -H "Content-Type: application/json" \
  -d '{"duration": 15, "task_name": "功能测试长任务"}')
long_task_id=$(echo $long_response | python3 -c "import sys, json; print(json.load(sys.stdin)['task_id'])")
echo "   任务ID: $long_task_id"
echo ""

# 3. 等待任务执行
echo "3️⃣ 等待任务执行..."
sleep 8

# 4. 检查任务结果
echo "4️⃣ 检查任务结果..."

echo "📊 快速计算结果:"
curl -s "$BASE_URL/tasks/$quick_task_id/result" | python3 -m json.tool | head -10

echo ""
echo "📧 邮件任务结果:"
curl -s "$BASE_URL/tasks/$email_task_id/result" | python3 -m json.tool | head -10

echo ""
echo "👥 批量处理结果:"
curl -s "$BASE_URL/tasks/$batch_task_id/result" | python3 -m json.tool | head -10

echo ""
echo "🌐 API获取结果:"
curl -s "$BASE_URL/tasks/$api_task_id/result" | python3 -m json.tool | head -10

echo ""
echo "⏱️  长任务状态:"
curl -s "$BASE_URL/tasks/$long_task_id/status" | python3 -m json.tool

echo ""
echo ""

# 5. 系统统计
echo "5️⃣ 系统统计..."
echo "活跃任务:"
curl -s "$BASE_URL/tasks/active" | python3 -m json.tool

echo ""
echo "任务历史 (最近10个):"
curl -s "$BASE_URL/tasks/" | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(f'总任务数: {data[\"total\"]}')
for task in data['tasks'][:10]:
    print(f'  - {task[\"task_name\"]}: {task[\"status\"]} ({task[\"created_at\"]})')
"

echo ""
echo ""

# 6. 并发演示
echo "6️⃣ 并发任务演示..."
demo_response=$(curl -s -X POST "$BASE_URL/demo/run-concurrent-tasks")
echo "并发演示启动:"
echo $demo_response | python3 -m json.tool

echo ""
echo ""

# 7. 监控链接
echo "7️⃣ 监控和管理界面:"
echo "   🌸 Flower 监控: http://localhost:5555"
echo "   🐰 RabbitMQ 管理: http://localhost:15672 (admin/admin123)"
echo "   📚 FastAPI 文档: http://localhost:8000/docs"
echo "   🎯 FastAPI 应用: http://localhost:8000"

echo ""
echo "✅ 功能测试完成!"
echo ""
echo "💡 提示:"
echo "   - 访问 Flower 界面查看实时任务监控"
echo "   - 查看 RabbitMQ 管理界面了解消息队列状态"
echo "   - 使用 FastAPI 文档页面交互式测试 API"
echo ""
