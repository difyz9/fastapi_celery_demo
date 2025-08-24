#!/bin/bash

# 测试脚本 - 验证 Celery RabbitMQ Demo 功能

BASE_URL="http://localhost:8000"

echo "🧪 开始测试 Celery RabbitMQ Demo..."

# 检查服务是否运行
echo "1️⃣ 检查服务健康状态..."
health_response=$(curl -s "$BASE_URL/health")
echo "健康检查响应: $health_response"
echo ""

# 测试快速任务
echo "2️⃣ 测试快速计算任务..."
quick_task_response=$(curl -s -X POST "$BASE_URL/tasks/quick" \
  -H "Content-Type: application/json" \
  -d '{"numbers": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}')
echo "快速任务响应: $quick_task_response"

# 提取任务ID
quick_task_id=$(echo $quick_task_response | python3 -c "import sys, json; print(json.load(sys.stdin)['task_id'])")
echo "快速任务ID: $quick_task_id"
echo ""

# 测试邮件任务
echo "3️⃣ 测试邮件发送任务..."
email_task_response=$(curl -s -X POST "$BASE_URL/tasks/email" \
  -H "Content-Type: application/json" \
  -d '{"recipient": "test@example.com", "subject": "测试邮件", "message": "这是一封测试邮件"}')
echo "邮件任务响应: $email_task_response"

email_task_id=$(echo $email_task_response | python3 -c "import sys, json; print(json.load(sys.stdin)['task_id'])")
echo "邮件任务ID: $email_task_id"
echo ""

# 测试批量处理任务
echo "4️⃣ 测试批量用户处理任务..."
batch_task_response=$(curl -s -X POST "$BASE_URL/tasks/batch" \
  -H "Content-Type: application/json" \
  -d '{"user_ids": [1, 2, 3]}')
echo "批量任务响应: $batch_task_response"

batch_task_id=$(echo $batch_task_response | python3 -c "import sys, json; print(json.load(sys.stdin)['task_id'])")
echo "批量任务ID: $batch_task_id"
echo ""

# 测试长时间任务
echo "5️⃣ 测试长时间运行任务..."
long_task_response=$(curl -s -X POST "$BASE_URL/tasks/long" \
  -H "Content-Type: application/json" \
  -d '{"duration": 10, "task_name": "测试长任务"}')
echo "长任务响应: $long_task_response"

long_task_id=$(echo $long_task_response | python3 -c "import sys, json; print(json.load(sys.stdin)['task_id'])")
echo "长任务ID: $long_task_id"
echo ""

# 等待一些任务完成
echo "6️⃣ 等待任务执行..."
sleep 5

# 检查任务状态
echo "7️⃣ 检查任务状态..."
echo "快速任务状态:"
curl -s "$BASE_URL/tasks/$quick_task_id/status" | python3 -m json.tool
echo ""

echo "邮件任务状态:"
curl -s "$BASE_URL/tasks/$email_task_id/status" | python3 -m json.tool
echo ""

echo "批量任务状态:"
curl -s "$BASE_URL/tasks/$batch_task_id/status" | python3 -m json.tool
echo ""

echo "长任务状态:"
curl -s "$BASE_URL/tasks/$long_task_id/status" | python3 -m json.tool
echo ""

# 检查活跃任务
echo "8️⃣ 检查活跃任务..."
curl -s "$BASE_URL/tasks/active" | python3 -m json.tool
echo ""

# 检查所有任务
echo "9️⃣ 检查任务历史..."
curl -s "$BASE_URL/tasks/" | python3 -m json.tool
echo ""

# 测试并发演示
echo "🔟 运行并发任务演示..."
demo_response=$(curl -s -X POST "$BASE_URL/demo/run-concurrent-tasks")
echo "并发演示响应:"
echo $demo_response | python3 -m json.tool
echo ""

echo "✅ 测试完成!"
echo ""
echo "🌐 访问地址:"
echo "   FastAPI 文档: http://localhost:8000/docs"
echo "   Flower 监控: http://localhost:5555"
echo "   RabbitMQ 管理: http://localhost:15672"
echo ""
