import os
from celery import Celery

# Celery 配置
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "amqp://admin:admin123@rabbitmq:5672//")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0")

# 创建 Celery 实例
celery_app = Celery(
    "celery_app",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
    include=["tasks"]  # 包含任务模块
)

# Celery 配置
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    # 工作进程配置
    worker_prefetch_multiplier=1,
    task_acks_late=True,
    worker_max_tasks_per_child=1000,
    # 启用连接重试
    broker_connection_retry_on_startup=True,
)
