#!/bin/bash

# 责任链模式功能测试脚本

BASE_URL="http://localhost:8000"

echo "🔗 责任链设计模式 - 功能演示"
echo "================================="

# 1. 单独测试数据验证处理器
echo "1️⃣ 测试数据验证处理器..."
validation_response=$(curl -s -X POST "$BASE_URL/chain/process" \
  -H "Content-Type: application/json" \
  -d '{
    "request_type": "data_validation",
    "data": {
      "payload": {
        "name": "Alice Smith",
        "age": 25,
        "email": "alice@example.com",
        "phone": "123-456-7890"
      },
      "required_fields": ["name", "email"],
      "validation_rules": {
        "name": {"type": "string", "min_length": 2},
        "age": {"type": "number"},
        "email": {"type": "string", "min_length": 5}
      }
    },
    "metadata": {"source": "manual_test"},
    "chain_type": "validation_only"
  }')

validation_task_id=$(echo $validation_response | python3 -c "import sys, json; print(json.load(sys.stdin)['task_id'])")
echo "   ✅ 验证任务ID: $validation_task_id"

# 2. 测试数据转换和导出链
echo ""
echo "2️⃣ 测试数据转换和导出链..."
transform_response=$(curl -s -X POST "$BASE_URL/chain/process" \
  -H "Content-Type: application/json" \
  -d '{
    "request_type": "data_transformation",
    "data": {
      "payload": {
        "first_name": "  john  ",
        "last_name": "  SMITH  ",
        "salary": "75000",
        "department": "ENGINEERING"
      },
      "transformations": {
        "first_name": "strip",
        "last_name": "strip",
        "salary": "to_number",
        "department": "lowercase"
      },
      "export_format": "json"
    },
    "chain_type": "transform_export"
  }')

transform_task_id=$(echo $transform_response | python3 -c "import sys, json; print(json.load(sys.stdin)['task_id'])")
echo "   ✅ 转换任务ID: $transform_task_id"

# 3. 测试数据丰富化和通知链
echo ""
echo "3️⃣ 测试数据丰富化和通知链..."
enrich_response=$(curl -s -X POST "$BASE_URL/chain/process" \
  -H "Content-Type: application/json" \
  -d '{
    "request_type": "data_enrichment",
    "data": {
      "payload": {
        "first_name": "Maria",
        "last_name": "Garcia",
        "age": 32,
        "email": "maria.garcia@company.com",
        "country": "Germany"
      },
      "notification_type": "email",
      "recipients": ["admin@example.com", "hr@example.com"],
      "message": "用户数据已成功丰富化"
    },
    "chain_type": "enrich_notify"
  }')

enrich_task_id=$(echo $enrich_response | python3 -c "import sys, json; print(json.load(sys.stdin)['task_id'])")
echo "   ✅ 丰富化任务ID: $enrich_task_id"

# 4. 测试动态链组装
echo ""
echo "4️⃣ 测试动态链组装..."
dynamic_response=$(curl -s -X POST "$BASE_URL/chain/dynamic" \
  -H "Content-Type: application/json" \
  -d '{
    "request_type": "data_transformation",
    "data": {
      "payload": {
        "title": "urgent message",
        "content": "system maintenance scheduled",
        "priority": "HIGH"
      },
      "transformations": {
        "title": "uppercase",
        "content": "uppercase",
        "priority": "lowercase"
      },
      "export_format": "xml",
      "notification_type": "email",
      "recipients": ["admin@example.com"],
      "message": "系统维护通知"
    },
    "handler_sequence": ["transformation", "export", "notification"]
  }')

dynamic_task_id=$(echo $dynamic_response | python3 -c "import sys, json; print(json.load(sys.stdin)['task_id'])")
echo "   ✅ 动态链任务ID: $dynamic_task_id"

# 5. 测试批量处理链
echo ""
echo "5️⃣ 测试批量处理链..."
batch_response=$(curl -s -X POST "$BASE_URL/chain/batch" \
  -H "Content-Type: application/json" \
  -d '{
    "batch_requests": [
      {
        "request_type": "data_validation",
        "data": {
          "payload": {"name": "User1", "email": "user1@example.com", "age": 25},
          "required_fields": ["name", "email"],
          "validation_rules": {"age": {"type": "number"}}
        }
      },
      {
        "request_type": "data_validation",
        "data": {
          "payload": {"name": "User2", "email": "user2@example.com", "age": 30},
          "required_fields": ["name", "email"],
          "validation_rules": {"age": {"type": "number"}}
        }
      },
      {
        "request_type": "data_validation",
        "data": {
          "payload": {"name": "User3", "email": "user3@example.com", "age": "invalid"},
          "required_fields": ["name", "email"],
          "validation_rules": {"age": {"type": "number"}}
        }
      }
    ],
    "chain_type": "standard"
  }')

batch_task_id=$(echo $batch_response | python3 -c "import sys, json; print(json.load(sys.stdin)['task_id'])")
echo "   ✅ 批量处理任务ID: $batch_task_id"

# 等待任务执行
echo ""
echo "6️⃣ 等待任务执行完成..."
sleep 8

# 7. 检查任务结果
echo ""
echo "7️⃣ 检查任务执行结果..."

echo ""
echo "📊 数据验证结果:"
curl -s "$BASE_URL/tasks/$validation_task_id/result" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    result = data['result']
    print(f'  状态: {data[\"status\"]}')
    print(f'  处理时长: {result[\"processing_duration\"]:.3f}s')
    print(f'  处理器数量: {result[\"total_handlers\"]}')
    print(f'  是否成功: {result[\"success\"]}')
    print(f'  错误数量: {len(result[\"errors\"])}')
    print(f'  警告数量: {len(result[\"warnings\"])}')
except:
    print('  任务还在处理中...')
"

echo ""
echo "🔄 数据转换结果:"
curl -s "$BASE_URL/tasks/$transform_task_id/result" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    result = data['result']
    print(f'  状态: {data[\"status\"]}')
    print(f'  处理时长: {result[\"processing_duration\"]:.3f}s')
    print(f'  处理器数量: {result[\"total_handlers\"]}')
    print(f'  原始数据字段: {len(result[\"original_data\"][\"payload\"])}')
    if result['processed_data']['transformed_payload']:
        print(f'  转换后字段: {len(result[\"processed_data\"][\"transformed_payload\"])}')
except:
    print('  任务还在处理中...')
"

echo ""
echo "📈 数据丰富化结果:"
curl -s "$BASE_URL/tasks/$enrich_task_id/result" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    result = data['result']
    print(f'  状态: {data[\"status\"]}')
    print(f'  处理时长: {result[\"processing_duration\"]:.3f}s')
    print(f'  处理器数量: {result[\"total_handlers\"]}')
    if result['processed_data']['enriched_payload']:
        enriched = result['processed_data']['enriched_payload']
        if '_metadata' in enriched:
            rules_applied = len(enriched['_metadata'].get('enrichment_rules_applied', []))
            print(f'  丰富化规则应用: {rules_applied}')
except:
    print('  任务还在处理中...')
"

echo ""
echo "🔧 动态链组装结果:"
curl -s "$BASE_URL/tasks/$dynamic_task_id/result" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    result = data['result']
    print(f'  状态: {data[\"status\"]}')
    print(f'  处理时长: {result[\"processing_duration\"]:.3f}s')
    print(f'  处理器数量: {result[\"total_handlers\"]}')
    if 'dynamic_chain_info' in result:
        chain_info = result['dynamic_chain_info']
        print(f'  处理器序列: {chain_info[\"handler_sequence\"]}')
        print(f'  使用的处理器: {chain_info[\"handlers_used\"]}')
except:
    print('  任务还在处理中...')
"

echo ""
echo "📦 批量处理结果:"
curl -s "$BASE_URL/tasks/$batch_task_id/result" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    result = data['result']
    print(f'  状态: {data[\"status\"]}')
    print(f'  总请求数: {result[\"total_requests\"]}')
    print(f'  成功请求: {result[\"successful_requests\"]}')
    print(f'  失败请求: {result[\"failed_requests\"]}')
    if 'processing_summary' in result:
        summary = result['processing_summary']
        print(f'  总错误数: {summary[\"total_errors\"]}')
        print(f'  总警告数: {summary[\"total_warnings\"]}')
        print(f'  平均处理时长: {summary[\"average_processing_duration\"]:.3f}s')
except:
    print('  任务还在处理中...')
"

echo ""
echo ""
echo "8️⃣ 责任链模式特性总结:"
echo "   ✅ 单一职责: 每个处理器只负责特定的处理逻辑"
echo "   ✅ 松耦合: 处理器之间相互独立，可以自由组合"
echo "   ✅ 可扩展: 可以轻松添加新的处理器类型"
echo "   ✅ 动态配置: 支持运行时动态组装处理链"
echo "   ✅ 错误处理: 每个处理器都有独立的错误处理"
echo "   ✅ 进度跟踪: 详细的处理日志和状态跟踪"

echo ""
echo "🌐 监控界面:"
echo "   Flower: http://localhost:5555"
echo "   FastAPI文档: http://localhost:8000/docs"

echo ""
echo "✅ 责任链模式演示完成!"
