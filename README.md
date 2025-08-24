# 🚀 分布式异步任务处理系统

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![Celery](https://img.shields.io/badge/Celery-5.3+-red.svg)](https://celeryproject.org)
[![Docker](https://img.shields.io/badge/Docker-Compose-blue.svg)](https://docker.com)

基于现代Python技术栈构建的企业级分布式异步任务处理系统，展示了微服务架构、责任链设计模式和容器化部署的最佳实践。

## 🏗️ 系统架构

```
celery_rabbit_demo/
├── 🐳 docker-compose.yml          # 容器编排配置
├── 📦 Dockerfile                  # 应用容器镜像
├── 📋 requirements.txt            # Python依赖管理
├── 🗄️ init.sql                    # 数据库初始化脚本
├── 🚀 start.sh                    # 一键启动脚本
├── 🧪 测试脚本套件/
│   ├── test.sh                   # 基础功能测试
│   ├── test_complete.sh          # 完整系统测试
│   ├── test_chain.sh             # 责任链模式测试
│   └── test_refactor.sh          # 重构验证测试
├── 📚 REFACTOR_SUMMARY.md         # 重构技术文档
└── 🎯 app/                        # 核心应用代码
    ├── main.py                   # FastAPI主应用入口
    ├── celery_app.py            # Celery分布式配置
    ├── tasks.py                 # 异步任务定义
    ├── database.py              # 数据访问层
    ├── chain_handlers.py        # 责任链框架
    └── handlers/                # 模块化处理器
        ├── __init__.py          # 基础类和接口
        ├── validation_handler.py     # 数据验证处理器
        ├── transformation_handler.py # 数据转换处理器
        ├── enrichment_handler.py     # 数据丰富化处理器
        ├── export_handler.py         # 数据导出处理器
        └── notification_handler.py   # 通知处理器
```

## � 核心特性

### 🎯 业务功能
- **多类型任务支持**: 长时运行、快速计算、邮件发送、批量处理、API调用
- **责任链设计模式**: 模块化数据处理管道，支持验证→转换→丰富化→导出→通知
- **灵活任务路由**: 不同任务类型智能分配到专用队列
- **实时任务监控**: 完整的任务生命周期跟踪和状态管理

### 🏗️ 技术架构
- **微服务架构**: 容器化部署，服务解耦，易于扩展
- **异步任务队列**: 高并发任务处理，支持任务重试和错误恢复
- **API优先设计**: RESTful接口，自动生成OpenAPI文档
- **模块化代码组织**: 单一职责原则，便于维护和测试

### 🔒 企业级特性
- **数据持久化**: MySQL存储任务记录，Redis缓存结果
- **监控告警**: Flower实时监控，支持性能指标和健康检查
- **配置管理**: 环境变量配置，支持开发/生产环境切换
- **错误处理**: 完善的异常处理和日志记录机制

## �🚀 技术栈

| 组件 | 版本 | 用途 | 端口 |
|------|------|------|------|
| **FastAPI** | 0.104.1 | Web框架，REST API服务 | 8000 |
| **Celery** | 5.3.4 | 分布式任务队列系统 | - |
| **RabbitMQ** | 3-management | 消息代理，任务分发 | 5672, 15672 |
| **Redis** | 7-alpine | 结果存储，缓存系统 | 6379 |
| **MySQL** | 8.0.42 | 关系数据库，持久化存储 | 3307 |
| **Flower** | 2.0.1 | Celery监控工具 | 5555 |
| **Docker** | Compose | 容器化部署编排 | - |

## 📦 服务详解

### 🐰 RabbitMQ (消息代理)
```yaml
角色: 任务消息的分发和路由中心
特性: 
  - 多队列管理 (long_tasks, quick_tasks, email_tasks)
  - 消息持久化和可靠传输
  - 管理界面可视化监控
访问: http://localhost:15672 (admin/admin123)
```

### 🗄️ MySQL (数据持久化)
```yaml
角色: 任务记录和业务数据存储
特性:
  - 任务执行历史记录
  - 用户数据管理
  - 事务一致性保证
连接: localhost:3307 (celery_user/celery_pass)
```

### ⚡ Redis (结果缓存)
```yaml
角色: 任务结果存储和高速缓存
特性:
  - 毫秒级数据访问
  - 任务状态实时更新
  - 内存数据结构存储
连接: localhost:6379
```

### 🔥 FastAPI (Web应用)
```yaml
角色: REST API服务和任务提交入口
特性:
  - 自动API文档生成
  - 异步请求处理
  - 数据验证和序列化
访问: http://localhost:8000/docs
```

### 👷 Celery Worker (任务执行)
```yaml
角色: 异步任务的实际执行单元
特性:
  - 多进程并发执行 (concurrency=4)
  - 任务预取和负载均衡
  - 自动故障恢复
```

### 🌸 Flower (监控平台)
```yaml
角色: Celery集群监控和管理
特性:
  - 实时任务状态监控
  - 工作进程性能指标
  - 任务历史统计分析
访问: http://localhost:5555
```

## ⚡ 快速开始

### 🚀 一键启动

```bash
# 克隆项目
git clone <repository-url>
cd celery_rabbit_demo

# 一键启动所有服务
./start.sh
```

### 🔍 验证部署

```bash
# 检查所有服务状态
docker-compose ps

# 查看关键服务日志
docker-compose logs -f web        # FastAPI应用日志
docker-compose logs -f celery-worker  # Celery工作进程日志
docker-compose logs -f rabbitmq   # RabbitMQ消息代理日志
```

### 🌐 访问服务

| 服务 | 地址 | 描述 |
|------|------|------|
| **FastAPI应用** | http://localhost:8000 | 主应用入口 |
| **API交互文档** | http://localhost:8000/docs | Swagger UI |
| **API技术文档** | http://localhost:8000/redoc | ReDoc |
| **Flower监控** | http://localhost:5555 | Celery任务监控 |
| **RabbitMQ管理** | http://localhost:15672 | 消息队列管理 |

### 🧪 快速测试

```bash
# 运行基础功能测试
./test.sh

# 运行完整系统测试
./test_complete.sh

# 运行责任链模式测试
./test_chain.sh

# 运行重构验证测试
./test_refactor.sh
```

## 🎯 核心API接口

### 🔍 系统监控
```http
GET /health                 # 服务健康检查
GET /                      # 系统信息总览
```

### 📝 任务管理
```http
POST /tasks/long           # 提交长时运行任务
POST /tasks/quick          # 提交快速计算任务  
POST /tasks/email          # 提交邮件发送任务
POST /tasks/batch          # 提交批量处理任务
POST /tasks/api-fetch      # 提交API数据获取任务
```

### 🔗 责任链处理
```http
POST /chain/process        # 单个责任链处理
POST /chain/batch         # 批量责任链处理
POST /chain/dynamic       # 动态组装处理链
POST /chain/demo          # 责任链功能演示
```

### 📊 状态查询
```http
GET /tasks/{task_id}/status     # 获取任务状态
GET /tasks/{task_id}/result     # 获取任务结果
GET /tasks/                     # 获取所有任务列表
GET /tasks/active              # 获取活跃任务列表
```

### 🎭 演示功能
```http
POST /demo/run-concurrent-tasks # 并发任务演示
```

## � API使用示例

### 💻 基础任务示例

#### 1. 长时运行任务 (数据处理场景)
```bash
curl -X POST "http://localhost:8000/tasks/long" \
  -H "Content-Type: application/json" \
  -d '{
    "duration": 30,
    "task_name": "大数据ETL处理"
  }'

# 响应示例
{
  "task_id": "abc123-def456-ghi789",
  "status": "PENDING",
  "message": "任务已提交，正在队列中等待执行",
  "estimated_duration": 30
}
```

#### 2. 快速计算任务 (数值处理场景)
```bash
curl -X POST "http://localhost:8000/tasks/quick" \
  -H "Content-Type: application/json" \
  -d '{
    "numbers": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
  }'

# 响应示例  
{
  "task_id": "calc123-456789",
  "status": "SUCCESS",
  "result": {
    "sum": 55,
    "average": 5.5,
    "max": 10,
    "min": 1
  }
}
```

#### 3. 邮件发送任务 (通知场景)
```bash
curl -X POST "http://localhost:8000/tasks/email" \
  -H "Content-Type: application/json" \
  -d '{
    "recipient": "user@company.com",
    "subject": "系统处理完成通知",
    "message": "您的数据处理任务已完成，请查看结果。"
  }'
```

#### 4. 批量处理任务 (批量操作场景)
```bash
curl -X POST "http://localhost:8000/tasks/batch" \
  -H "Content-Type: application/json" \
  -d '{
    "user_ids": [101, 102, 103, 104, 105]
  }'
```

#### 5. API数据获取任务 (数据集成场景)
```bash
curl -X POST "http://localhost:8000/tasks/api-fetch" \
  -H "Content-Type: application/json" \
  -d '{
    "urls": [
      "https://jsonplaceholder.typicode.com/posts/1",
      "https://jsonplaceholder.typicode.com/users/1"
    ]
  }'
```

### 📊 任务状态查询

```bash
# 查询任务状态
curl "http://localhost:8000/tasks/abc123-def456-ghi789/status"

# 获取任务结果
curl "http://localhost:8000/tasks/abc123-def456-ghi789/result"

# 获取所有活跃任务
curl "http://localhost:8000/tasks/active"
```

## 🔗 责任链设计模式

本项目实现了完整的责任链设计模式，用于构建灵活的数据处理管道。

### 📋 责任链特性

- **单一职责**: 每个处理器只负责特定的处理逻辑
- **松耦合**: 处理器之间相互独立，可以自由组合
- **可扩展**: 可以轻松添加新的处理器类型
- **动态配置**: 支持运行时动态组装处理链
- **错误处理**: 每个处理器都有独立的错误处理
- **进度跟踪**: 详细的处理日志和状态跟踪

### 🔧 处理器类型

1. **DataValidationHandler** - 数据验证
   - 检查必填字段
   - 验证数据类型
   - 应用验证规则

2. **DataTransformationHandler** - 数据转换
   - 字符串处理 (大小写、去空格)
   - 数据类型转换
   - 数值计算

3. **DataEnrichmentHandler** - 数据丰富化
   - 添加元数据
   - 推导新字段
   - 地理位置信息

4. **DataExportHandler** - 数据导出
   - JSON/CSV/XML 格式导出
   - 文件大小统计
   - 导出位置记录

5. **NotificationHandler** - 通知发送
   - 邮件通知
   - 发送状态跟踪
   - 错误重试

### 🎯 责任链演示

#### 1. 基础数据验证链
```bash
curl -X POST "http://localhost:8000/chain/process" \
  -H "Content-Type: application/json" \
  -d '{
    "request_type": "data_validation",
    "data": {
      "payload": {
        "name": "Alice Smith",
        "age": 25,
        "email": "alice@example.com"
      },
      "required_fields": ["name", "email"],
      "validation_rules": {
        "name": {"type": "string", "min_length": 2},
        "age": {"type": "number"}
      }
    },
    "chain_type": "validation_only"
  }'
```

#### 2. 数据转换和导出链
```bash
curl -X POST "http://localhost:8000/chain/process" \
  -H "Content-Type: application/json" \
  -d '{
    "request_type": "data_transformation",
    "data": {
      "payload": {
        "first_name": "  john  ",
        "salary": "75000"
      },
      "transformations": {
        "first_name": "strip",
        "salary": "to_number"
      },
      "export_format": "json"
    },
    "chain_type": "transform_export"
  }'
```

#### 3. 动态链组装
```bash
curl -X POST "http://localhost:8000/chain/dynamic" \
  -H "Content-Type: application/json" \
  -d '{
    "request_type": "data_transformation",
    "data": {
      "payload": {"message": "hello world"},
      "transformations": {"message": "uppercase"},
      "notification_type": "email",
      "recipients": ["admin@example.com"]
    },
    "handler_sequence": ["transformation", "export", "notification"]
  }'
```

#### 4. 批量责任链处理
```bash
curl -X POST "http://localhost:8000/chain/batch" \
  -H "Content-Type: application/json" \
  -d '{
    "batch_requests": [
      {
        "request_type": "data_validation",
        "data": {
          "payload": {"name": "User1", "email": "user1@example.com"},
          "required_fields": ["name", "email"]
        }
      },
      {
        "request_type": "data_validation", 
        "data": {
          "payload": {"name": "User2", "email": "user2@example.com"},
          "required_fields": ["name", "email"]
        }
      }
    ],
    "chain_type": "standard"
  }'
```

#### 5. 责任链完整演示
```bash
# 运行所有类型的责任链演示
curl -X POST "http://localhost:8000/chain/demo"

# 或者使用专用测试脚本
./test_chain.sh
```

### 🔄 链类型说明

- **validation_only**: 仅数据验证
- **transform_export**: 数据转换 + 导出
- **enrich_notify**: 数据丰富化 + 通知
- **standard**: 完整标准链 (验证 → 转换 → 丰富化 → 导出 → 通知)
- **custom/dynamic**: 自定义处理器序列

## 📊 监控和调试

### 1. Flower 监控界面
访问 http://localhost:5555 查看：
- 活跃任务和工作进程
- 任务执行统计
- 工作进程状态
- 任务历史记录

### 2. RabbitMQ 管理界面
访问 http://localhost:15672：
- 用户名: admin
- 密码: admin123
- 查看队列状态、消息统计

### 3. 任务状态查询
```bash
# 获取任务状态
curl "http://localhost:8000/tasks/{task_id}/status"

# 获取任务结果
curl "http://localhost:8000/tasks/{task_id}/result"

# 获取活跃任务
curl "http://localhost:8000/tasks/active"
```

## 🔧 配置说明

### Celery 配置特性
- **任务序列化**: JSON 格式
- **任务路由**: 不同类型任务分配到不同队列
- **并发控制**: 工作进程预取和最大任务数限制
- **任务确认**: 延迟确认机制保证任务可靠性

### 任务队列路由
- `long_tasks` - 长时间运行任务
- `quick_tasks` - 快速计算任务
- `email_tasks` - 邮件发送任务

### 数据库集成
- 任务状态持久化存储
- 任务执行历史记录
- 用户数据管理

## 🛠️ 开发和扩展

### 添加新任务类型
1. 在 `app/tasks.py` 中定义新任务
2. 在 `app/main.py` 中添加对应的 API 端点
3. 更新任务路由配置

### 扩展工作进程
```bash
# 增加工作进程数量
docker-compose up --scale celery-worker=3
```

### 自定义队列配置
修改 `app/celery_app.py` 中的 `task_routes` 配置

## 🛑 停止服务

```bash
# 停止所有服务
docker-compose down

# 删除旧的 Docker 镜像并重新构建：
docker-compose build --no-cache



# 在启动服务：

docker-compose up -d


# 停止并删除卷数据
docker-compose down -v

# 查看资源使用
docker system df
```

## 📝 注意事项

1. **端口冲突**: 确保端口 3306, 5672, 6379, 8000, 5555, 15672 未被占用
2. **内存使用**: MySQL 和 RabbitMQ 需要足够的内存资源
3. **数据持久化**: 数据存储在 Docker 卷中，使用 `docker-compose down -v` 会删除数据
4. **生产环境**: 生产环境中需要修改默认密码和安全配置

## 🚀 性能优化建议

1. **Celery 优化**:
   - 调整 `worker_concurrency` 并发数
   - 配置 `worker_prefetch_multiplier`
   - 启用 `task_acks_late`

2. **RabbitMQ 优化**:
   - 配置内存和磁盘限制
   - 启用集群模式
   - 配置消息持久化

3. **数据库优化**:
   - 添加索引
   - 配置连接池
   - 启用查询缓存

这个项目展示了如何构建一个完整的分布式异步任务处理系统，适合学习和在生产环境中使用。
