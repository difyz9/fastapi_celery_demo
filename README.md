# Celery + RabbitMQ + FastAPI + Flower + MySQL 异步任务并发执行案例

这是一个完整的异步任务处理系统演示，展示如何使用 Celery、RabbitMQ、FastAPI、Flower 和 MySQL 构建高性能的分布式任务系统。

## 🏗️ 项目架构

```
celery_rabbit_demo/
├── docker-compose.yml      # Docker 编排文件
├── Dockerfile             # 应用镜像构建文件
├── requirements.txt       # Python 依赖
├── init.sql              # MySQL 初始化脚本
├── start.sh              # 启动脚本
└── app/
    ├── main.py           # FastAPI 主应用
    ├── celery_app.py     # Celery 配置
    ├── tasks.py          # 异步任务定义
    └── database.py       # 数据库配置和模型
```

## 🚀 技术栈

- **FastAPI**: Web 框架，提供 REST API
- **Celery**: 分布式任务队列
- **RabbitMQ**: 消息代理 (Message Broker)
- **Redis**: 任务结果存储
- **MySQL**: 关系型数据库
- **Flower**: Celery 监控工具
- **Docker Compose**: 容器编排

## 📦 服务组件

### 1. RabbitMQ (消息代理)
- 端口: 5672 (AMQP), 15672 (管理界面)
- 用户名/密码: admin/admin123
- 负责任务消息的路由和分发

### 2. MySQL (数据库)
- 端口: 3306
- 数据库: celery_demo
- 用户名/密码: celery_user/celery_pass
- 存储任务记录和用户数据

### 3. Redis (结果存储)
- 端口: 6379
- 用于存储 Celery 任务执行结果

### 4. FastAPI (Web 应用)
- 端口: 8000
- 提供任务提交和查询 API
- 自动生成 API 文档

### 5. Celery Worker (任务执行器)
- 并发数: 4
- 执行各种类型的异步任务

### 6. Flower (监控工具)
- 端口: 5555
- 实时监控 Celery 任务和工作进程

## 🛠️ 快速开始

### 1. 启动所有服务

```bash
# 使用启动脚本
./start.sh

# 或者手动启动
docker-compose up --build -d
```

### 2. 验证服务状态

```bash
# 查看所有服务状态
docker-compose ps

# 查看服务日志
docker-compose logs -f web
docker-compose logs -f celery-worker
```

### 3. 访问服务

- **FastAPI 应用**: http://localhost:8000
- **API 文档**: http://localhost:8000/docs
- **Flower 监控**: http://localhost:5555
- **RabbitMQ 管理**: http://localhost:15672

## 📋 API 端点

### 健康检查
- `GET /health` - 服务健康状态

### 任务提交
- `POST /tasks/long` - 提交长时间运行任务
- `POST /tasks/quick` - 提交快速计算任务
- `POST /tasks/email` - 提交邮件发送任务
- `POST /tasks/batch` - 提交批量处理任务
- `POST /tasks/api-fetch` - 提交API数据获取任务

### 任务监控
- `GET /tasks/{task_id}/status` - 获取任务状态
- `GET /tasks/{task_id}/result` - 获取任务结果
- `GET /tasks/` - 获取所有任务
- `GET /tasks/active` - 获取活跃任务

### 演示功能
- `POST /demo/run-concurrent-tasks` - 运行并发任务演示

## 🎯 任务类型演示

### 1. 长时间运行任务
```bash
curl -X POST "http://localhost:8000/tasks/long" \
  -H "Content-Type: application/json" \
  -d '{"duration": 30, "task_name": "数据处理任务"}'
```

### 2. 快速计算任务
```bash
curl -X POST "http://localhost:8000/tasks/quick" \
  -H "Content-Type: application/json" \
  -d '{"numbers": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}'
```

### 3. 邮件发送任务
```bash
curl -X POST "http://localhost:8000/tasks/email" \
  -H "Content-Type: application/json" \
  -d '{"recipient": "user@example.com", "subject": "测试邮件", "message": "这是一封测试邮件"}'
```

### 4. 批量用户处理
```bash
curl -X POST "http://localhost:8000/tasks/batch" \
  -H "Content-Type: application/json" \
  -d '{"user_ids": [1, 2, 3]}'
```

### 5. API数据获取
```bash
curl -X POST "http://localhost:8000/tasks/api-fetch" \
  -H "Content-Type: application/json" \
  -d '{"urls": ["https://jsonplaceholder.typicode.com/posts/1", "https://jsonplaceholder.typicode.com/posts/2"]}'
```

### 6. 并发任务演示
```bash
curl -X POST "http://localhost:8000/demo/run-concurrent-tasks"
```

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
