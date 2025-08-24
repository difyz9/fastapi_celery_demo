# 🚀 分布式异步任务处理系统

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![Celery](https://img.shields.io/badge/Celery-5.3+-red.svg)](https://celeryproject.org)
[![Docker](https://img.shields.io/badge/Docker-Compose-blue.svg)](https://docker.com)

基于现代Python技术栈构建的企业级分布式异步任务处理系统，展示了微服务架构、责任链设计模式和容器化部署的最佳实践。

## 🏗️ 系统架构

## 🎓 学习指南

### 📚 技术栈学习路径

#### 1. 初级开发者 (入门级)
```
学习顺序:
1️⃣ 基础概念理解
   - 异步编程概念
   - 分布式系统基础  
   - REST API设计

2️⃣ 环境搭建实践
   - Docker基础使用
   - 运行./start.sh启动系统
   - 访问各个监控界面

3️⃣ API测试体验
   - 使用curl测试基础任务
   - 查看Flower监控界面
   - 观察任务执行过程
```

#### 2. 中级开发者 (进阶级)
```
深入学习:
1️⃣ 责任链模式理解
   - 运行./test_chain.sh
   - 分析处理器设计
   - 尝试修改处理逻辑

2️⃣ 任务队列优化
   - 调整Celery配置
   - 理解消息路由机制
   - 监控性能指标

3️⃣ 数据库集成
   - 理解ORM模型设计
   - 任务状态管理
   - 数据一致性保证
```

#### 3. 高级开发者 (专家级)
```
架构深化:
1️⃣ 系统扩展设计
   - 添加新的处理器类型
   - 实现自定义路由规则
   - 设计集群部署方案

2️⃣ 性能调优实践
   - 压力测试和性能分析
   - 瓶颈识别和优化
   - 监控告警体系建设

3️⃣ 生产环境部署
   - 安全配置加固
   - 容灾备份方案
   - CI/CD流水线集成
```

### 🧪 实验和扩展

#### 🔬 实验项目建议
```
1. 添加新的处理器类型
   - 图像处理器 (ImageProcessingHandler)
   - 文档解析器 (DocumentParsingHandler)  
   - 机器学习推理器 (MLInferenceHandler)

2. 集成外部服务
   - 第三方API调用
   - 云存储服务集成
   - 消息推送服务

3. 监控增强
   - Prometheus指标收集
   - Grafana可视化面板
   - 自定义告警规则
```

### 📖 相关资源

#### 🔗 官方文档
- [Celery官方文档](https://docs.celeryproject.org/)
- [FastAPI官方文档](https://fastapi.tiangolo.com/)
- [RabbitMQ官方文档](https://www.rabbitmq.com/documentation.html)

#### 📺 推荐学习资源
- [异步编程最佳实践](https://realpython.com/async-io-python/)
- [分布式系统设计模式](https://microservices.io/patterns/)
- [Docker容器化部署指南](https://docs.docker.com/get-started/)

## 🤝 贡献指南

### 💻 开发环境搭建
```bash
# 1. 克隆项目
git clone <repository-url>
cd celery_rabbit_demo

# 2. 创建开发分支
git checkout -b feature/your-feature-name

# 3. 安装开发依赖
pip install -r requirements.txt

# 4. 运行测试
./test_complete.sh
```

### 🔧 代码贡献流程
```
1. 🍴 Fork项目到个人仓库
2. 🌿 创建功能分支: git checkout -b feature/amazing-feature
3. 💻 编写代码和测试用例
4. ✅ 运行所有测试确保通过
5. 📝 提交代码: git commit -m 'Add amazing feature'
6. 🚀 推送分支: git push origin feature/amazing-feature
7. 🔀 创建Pull Request
```

### 📋 代码规范
```python
# 处理器开发规范
class NewHandler(BaseHandler):
    """
    新处理器类文档字符串
    
    功能描述: 详细说明处理器的作用
    输入格式: 描述期望的输入数据格式
    输出格式: 描述处理后的输出格式
    """
    
    def __init__(self):
        super().__init__("NewHandler")
    
    def can_handle(self, request: ProcessingRequest) -> bool:
        """判断是否能处理此请求"""
        return request.request_type == RequestType.NEW_TYPE
    
    def process(self, request: ProcessingRequest) -> ProcessingRequest:
        """处理逻辑实现"""
        # 添加详细的处理逻辑
        request.add_log(self.name, "处理完成")
        return request
```

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

感谢以下开源项目为本项目提供的基础支持：

- [Celery](https://celeryproject.org/) - 分布式任务队列
- [FastAPI](https://fastapi.tiangolo.com/) - 现代Python Web框架
- [RabbitMQ](https://www.rabbitmq.com/) - 可靠的消息代理
- [Docker](https://www.docker.com/) - 容器化平台

## 📞 联系我们

- 📧 邮箱: [your-email@example.com]
- 🐛 问题反馈: [GitHub Issues](https://github.com/your-username/celery_rabbit_demo/issues)
- 💬 讨论交流: [GitHub Discussions](https://github.com/your-username/celery_rabbit_demo/discussions)

---

## 🎯 项目总结

本项目是一个**企业级分布式异步任务处理系统**的完整演示，它不仅展示了现代Python技术栈的强大能力，更通过**责任链设计模式**的巧妙应用，提供了灵活、可扩展的数据处理解决方案。

### ✨ 核心价值
- **🏗️ 架构示范**: 展示微服务架构和容器化部署的最佳实践
- **🎨 设计模式**: 完整实现责任链模式，代码组织清晰优雅  
- **🚀 生产就绪**: 包含监控、日志、错误处理等企业级特性
- **📚 学习价值**: 适合不同水平开发者学习异步编程和分布式系统

### 🌟 技术亮点
- **模块化设计**: 处理器独立成模块，符合单一职责原则
- **动态组装**: 支持运行时灵活组装处理链
- **完整监控**: Flower + RabbitMQ管理界面 + 自定义API监控
- **容器化部署**: 一键启动，开箱即用

无论您是想学习异步编程、分布式系统设计，还是寻找生产环境的解决方案，本项目都能为您提供宝贵的参考和启发。

**开始您的异步任务处理之旅吧！** 🚀

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

本项目的核心亮点是实现了完整的**责任链设计模式**，构建了灵活的数据处理管道系统。经过模块化重构，现在具有更好的代码组织和可维护性。

### 🏗️ 架构设计

```
责任链处理流程:
Input → Validation → Transformation → Enrichment → Export → Notification → Output

模块化结构:
handlers/
├── __init__.py              # 基础类和接口定义
├── validation_handler.py    # 数据验证处理器
├── transformation_handler.py # 数据转换处理器  
├── enrichment_handler.py    # 数据丰富化处理器
├── export_handler.py        # 数据导出处理器
└── notification_handler.py  # 通知处理器
```

### ⭐ 设计模式特性

| 特性 | 描述 | 优势 |
|------|------|------|
| **单一职责** | 每个处理器只负责特定功能 | 代码清晰，易于维护 |
| **松耦合** | 处理器之间相互独立 | 可自由组合和替换 |
| **可扩展** | 轻松添加新处理器类型 | 适应业务变化 |
| **动态配置** | 运行时动态组装处理链 | 灵活的业务流程 |
| **错误隔离** | 独立的错误处理机制 | 提高系统稳定性 |
| **进度跟踪** | 详细的处理日志记录 | 便于调试和监控 |

### 🔧 处理器详解

#### 1. 📋 DataValidationHandler (数据验证)
```python
功能特性:
✅ 必填字段检查
✅ 数据类型验证  
✅ 格式规则验证 (邮箱、电话等)
✅ 业务规则验证
✅ 自定义验证器支持

处理场景:
- 用户输入数据验证
- API请求参数检查
- 数据质量保证
```

#### 2. 🔄 DataTransformationHandler (数据转换)
```python
功能特性:
✅ 字符串处理 (大小写转换、去空格、格式化)
✅ 数值计算 (四则运算、百分比、四舍五入)
✅ 日期时间处理
✅ 数据类型转换
✅ 自定义转换规则

处理场景:
- 数据标准化
- 格式统一化
- 计算衍生字段
```

#### 3. 📈 DataEnrichmentHandler (数据丰富化)
```python
功能特性:
✅ 个人信息丰富化 (姓名解析、年龄分组)
✅ 地理信息丰富化 (国家信息、时区)
✅ 职业信息丰富化 (行业分类、经验估算)
✅ 联系方式分析 (邮箱域名、电话区号)
✅ 行为偏好预测

处理场景:
- 用户画像构建
- 数据补全增强
- 智能标签生成
```

#### 4. 📤 DataExportHandler (数据导出)
```python
功能特性:
✅ 多格式支持 (JSON、CSV、XML、Excel)
✅ 模板化导出
✅ 数据筛选和字段映射
✅ 文件大小统计
✅ 报告生成

处理场景:
- 数据交换
- 报表生成
- 数据备份
```

#### 5. 📢 NotificationHandler (通知处理)
```python
功能特性:
✅ 多渠道通知 (邮件、短信、Webhook、Slack等)
✅ 模板化消息
✅ 告警规则引擎
✅ 发送状态跟踪
✅ 失败重试机制

处理场景:
- 任务完成通知
- 异常告警
- 状态变更通知
```

### 🎯 责任链使用示例

#### 🔍 1. 数据验证链 (适用于数据质量检查)
```bash
curl -X POST "http://localhost:8000/chain/process" \
  -H "Content-Type: application/json" \
  -d '{
    "request_type": "data_validation",
    "data": {
      "payload": {
        "name": "Alice Smith",
        "age": 25,
        "email": "alice@company.com",
        "phone": "+1-555-0123"
      },
      "required_fields": ["name", "email"],
      "validation_rules": {
        "name": {"type": "string", "min_length": 2},
        "age": {"type": "number", "min": 0, "max": 150},
        "email": {"type": "email"},
        "phone": {"type": "phone"}
      }
    },
    "chain_type": "validation_only"
  }'
```

#### 🔄 2. 数据转换导出链 (适用于数据标准化)
```bash
curl -X POST "http://localhost:8000/chain/process" \
  -H "Content-Type: application/json" \
  -d '{
    "request_type": "data_transformation",
    "data": {
      "payload": {
        "first_name": "  john  ",
        "last_name": "DOE",
        "salary": "75000.50",
        "join_date": "2023-01-15"
      },
      "transformations": {
        "first_name": "strip_and_title",
        "last_name": "lowercase",
        "salary": "to_number",
        "join_date": "parse_date"
      },
      "export_config": {
        "format": "json",
        "filename": "processed_employee.json"
      }
    },
    "chain_type": "transform_export"
  }'
```

#### 📈 3. 数据丰富化链 (适用于用户画像构建)
```bash
curl -X POST "http://localhost:8000/chain/process" \
  -H "Content-Type: application/json" \
  -d '{
    "request_type": "data_enrichment",
    "data": {
      "payload": {
        "name": "张三",
        "age": 28,
        "email": "zhangsan@company.com",
        "city": "Beijing",
        "country": "China",
        "job_title": "Software Engineer"
      },
      "enrichment_rules": [
        "geo_info", "demographic_info", 
        "professional_info", "contact_analysis"
      ]
    },
    "chain_type": "enrich_notify"
  }'
```

#### 🚀 4. 动态链组装 (适用于灵活业务流程)
```bash
curl -X POST "http://localhost:8000/chain/dynamic" \
  -H "Content-Type: application/json" \
  -d '{
    "request_type": "data_transformation",
    "data": {
      "payload": {
        "message": "hello world",
        "score": "85.5",
        "category": "IMPORTANT"
      },
      "transformations": {
        "message": "uppercase",
        "score": "to_number",
        "category": "lowercase"
      },
      "export_config": {
        "format": "csv"
      },
      "notification_config": {
        "type": "success",
        "channels": ["email", "slack"],
        "recipients": ["admin@company.com"]
      }
    },
    "handler_sequence": ["transformation", "export", "notification"]
  }'
```

#### 📦 5. 批量责任链处理 (适用于大数据批处理)
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
        "request_type": "data_transformation",
        "data": {
          "payload": {"message": "test data"},
          "transformations": {"message": "uppercase"}
        }
      },
      {
        "request_type": "data_enrichment",
        "data": {
          "payload": {"country": "USA", "age": 30},
          "enrichment_rules": ["geo_info"]
        }
      }
    ],
    "chain_type": "standard"
  }'
```

#### 🎭 6. 完整演示 (展示所有功能)
```bash
# 运行所有类型的责任链演示
curl -X POST "http://localhost:8000/chain/demo"

# 或使用专用测试脚本
./test_chain.sh
```

### 🔄 预定义链类型

| 链类型 | 处理器组合 | 适用场景 |
|--------|------------|----------|
| **validation_only** | 验证 | 数据质量检查 |
| **transform_export** | 转换 → 导出 | 数据标准化输出 |
| **enrich_notify** | 丰富化 → 通知 | 数据增强处理 |
| **standard** | 验证 → 转换 → 丰富化 → 导出 → 通知 | 完整数据处理流程 |
| **custom/dynamic** | 自定义序列 | 灵活业务需求 |

### 📊 处理结果示例

```json
{
  "task_id": "chain_task_123456",
  "status": "SUCCESS",
  "processing_time": 1.25,
  "handlers_executed": [
    "DataValidationHandler",
    "DataTransformationHandler", 
    "DataEnrichmentHandler",
    "DataExportHandler",
    "NotificationHandler"
  ],
  "logs": [
    {
      "handler": "DataValidationHandler",
      "message": "验证了 5 个字段，全部通过",
      "timestamp": 1692876543.123
    },
    {
      "handler": "DataTransformationHandler", 
      "message": "应用了 3 个转换规则",
      "timestamp": 1692876543.456
    }
  ],
  "errors": [],
  "warnings": [],
  "result": {
    "validated_data": { "name": "Alice Smith", "email": "alice@company.com" },
    "transformed_data": { "name": "Alice Smith", "email": "alice@company.com" },
    "enriched_data": { "name": "Alice Smith", "full_name": "Alice Smith" },
    "export_result": { "format": "json", "size_bytes": 1024 },
    "notification_result": { "channels": ["email"], "success_count": 1 }
  }
}
```

## 📊 监控和运维

### 🌸 Flower监控平台
访问 **http://localhost:5555** 获取全面的任务监控：

```
🔍 实时监控功能:
├── 📈 任务执行统计 (成功率、失败率、处理时间)
├── 👷 工作进程状态 (CPU、内存使用情况)  
├── 📋 任务队列监控 (队列长度、消息积压)
├── 📜 任务历史记录 (执行日志、错误追踪)
├── ⚙️ 配置信息查看 (路由规则、队列配置)
└── 🔄 实时任务控制 (取消、重试、查看详情)
```

### 🐰 RabbitMQ管理控制台
访问 **http://localhost:15672** (admin/admin123)：

```
🔧 队列管理功能:
├── 📊 队列状态监控 (消息数量、消费速率)
├── 🔄 Exchange配置 (路由规则、绑定关系)
├── 👥 连接管理 (活跃连接、信道状态)
├── 📈 性能指标 (吞吐量、延迟统计)
└── ⚠️ 告警设置 (队列阈值、连接监控)
```

### 🔍 任务状态API
```bash
# 获取特定任务状态
curl "http://localhost:8000/tasks/{task_id}/status"
# 响应: {"status": "SUCCESS", "current": 100, "total": 100}

# 获取任务执行结果
curl "http://localhost:8000/tasks/{task_id}/result"  
# 响应: {"result": {...}, "traceback": null, "children": []}

# 获取所有活跃任务
curl "http://localhost:8000/tasks/active"
# 响应: [{"task_id": "...", "status": "RUNNING", "name": "..."}]

# 系统健康检查
curl "http://localhost:8000/health"
# 响应: {"status": "healthy", "services": {...}}
```

### � 日志查看
```bash
# 查看应用日志
docker-compose logs -f web

# 查看Celery工作进程日志
docker-compose logs -f celery-worker

# 查看RabbitMQ日志
docker-compose logs -f rabbitmq

# 查看MySQL日志
docker-compose logs -f mysql

# 查看Redis日志  
docker-compose logs -f redis
```

## 🛠️ 运维和扩展

### ⚙️ 配置管理

#### Celery任务配置
```python
# app/celery_app.py
CELERY_CONFIG = {
    'worker_concurrency': 4,          # 工作进程并发数
    'task_acks_late': True,           # 延迟任务确认
    'worker_prefetch_multiplier': 1,  # 预取任务数量
    'task_routes': {                  # 任务路由规则
        'tasks.long_running_task': {'queue': 'long_tasks'},
        'tasks.quick_computation': {'queue': 'quick_tasks'},
        'tasks.send_email': {'queue': 'email_tasks'}
    }
}
```

#### 数据库连接配置
```python
# app/database.py
DATABASE_CONFIG = {
    'host': 'mysql',
    'port': 3306,
    'database': 'celery_demo',
    'username': 'celery_user',
    'password': 'celery_pass',
    'pool_size': 10,
    'max_overflow': 20
}
```

### 🚀 性能优化

#### 1. Celery优化
```bash
# 调整工作进程数量
docker-compose up --scale celery-worker=3

# 优化预取设置
export CELERY_WORKER_PREFETCH_MULTIPLIER=2

# 启用任务结果压缩
export CELERY_RESULT_COMPRESSION='gzip'
```

#### 2. RabbitMQ优化  
```bash
# 设置内存限制
docker exec rabbitmq rabbitmqctl set_vm_memory_high_watermark 0.6

# 配置磁盘空间阈值
docker exec rabbitmq rabbitmqctl set_disk_free_limit 2GB
```

#### 3. MySQL优化
```sql
-- 添加任务查询索引
CREATE INDEX idx_task_status ON tasks(status);
CREATE INDEX idx_task_created ON tasks(created_at);

-- 配置连接池
SET GLOBAL max_connections = 200;
SET GLOBAL innodb_buffer_pool_size = 1073741824;
```

### � 扩展部署

#### 水平扩展工作节点
```bash
# 启动多个工作进程
docker-compose up --scale celery-worker=5

# 添加专用队列工作节点
docker run -d --name worker-emails \
  --network celery_rabbit_demo_default \
  celery_rabbit_demo_web \
  celery -A celery_app worker -Q email_tasks
```

#### 负载均衡配置
```yaml
# docker-compose.yml 负载均衡扩展
services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - web

  web:
    build: .
    expose:
      - "8000"
    deploy:
      replicas: 3
```

### 🔐 安全配置

#### 生产环境安全设置
```bash
# 环境变量配置文件 .env
MYSQL_ROOT_PASSWORD=strong_password_123
MYSQL_PASSWORD=celery_secure_pass_456
RABBITMQ_DEFAULT_PASS=rabbit_secure_pass_789

# Redis密码保护
REDIS_PASSWORD=redis_secure_pass_012

# FastAPI安全设置
SECRET_KEY=your_very_secret_key_here
DEBUG=False
```

#### 网络安全
```yaml
# docker-compose.yml 网络隔离
networks:
  backend:
    driver: bridge
    internal: true  # 内部网络，外部无法访问
  frontend:
    driver: bridge  # 前端网络，暴露必要端口
```

## 🛑 部署维护

### � 服务管理
```bash
# 启动所有服务
./start.sh

# 停止所有服务
docker-compose down

# 重启特定服务
docker-compose restart celery-worker

# 查看服务状态
docker-compose ps

# 查看资源使用
docker stats
```

### 🗄️ 数据备份
```bash
# MySQL数据备份
docker exec mysql mysqldump -u celery_user -pcelery_pass celery_demo > backup.sql

# Redis数据备份  
docker exec redis redis-cli BGSAVE

# 恢复MySQL数据
docker exec -i mysql mysql -u celery_user -pcelery_pass celery_demo < backup.sql
```

### 🧹 清理维护
```bash
# 清理停止的容器
docker container prune

# 清理未使用的镜像
docker image prune

# 清理未使用的卷
docker volume prune

# 完全清理重建
docker-compose down -v
docker system prune -a
docker-compose up --build -d
```
