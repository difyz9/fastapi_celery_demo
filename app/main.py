from fastapi import FastAPI, BackgroundTasks, Depends, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session
import uuid

from celery_app import celery_app
from database import get_db, Task, User
import tasks

app = FastAPI(
    title="Celery RabbitMQ Demo API",
    description="异步任务处理演示API",
    version="1.0.0"
)

# Pydantic 模型
class TaskCreate(BaseModel):
    task_type: str
    parameters: dict

class QuickTaskData(BaseModel):
    numbers: List[int]

class EmailTaskData(BaseModel):
    recipient: str
    subject: str
    message: str

class BatchProcessData(BaseModel):
    user_ids: List[int]

class APIFetchData(BaseModel):
    urls: List[str]

class LongTaskData(BaseModel):
    duration: int = 60
    task_name: str = "Long Running Task"

@app.get("/")
async def root():
    return {
        "message": "Celery RabbitMQ Demo API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "tasks": {
                "submit_long_task": "/tasks/long",
                "submit_quick_task": "/tasks/quick",
                "submit_email_task": "/tasks/email",
                "submit_batch_task": "/tasks/batch",
                "submit_api_fetch_task": "/tasks/api-fetch"
            },
            "monitoring": {
                "task_status": "/tasks/{task_id}/status",
                "task_result": "/tasks/{task_id}/result",
                "all_tasks": "/tasks/",
                "active_tasks": "/tasks/active"
            },
            "users": "/users/"
        }
    }

@app.get("/health")
async def health_check():
    """健康检查端点"""
    try:
        # 检查 Celery 连接
        celery_status = celery_app.control.inspect().active()
        
        return {
            "status": "healthy",
            "celery_workers": len(celery_status) if celery_status else 0,
            "database": "connected"
        }
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={"status": "unhealthy", "error": str(e)}
        )

@app.post("/tasks/long")
async def submit_long_task(data: LongTaskData):
    """提交长时间运行的任务"""
    task = tasks.long_running_task.delay(data.duration, data.task_name)
    return {
        "task_id": task.id,
        "status": "submitted",
        "message": f"Long running task submitted with duration {data.duration}s"
    }

@app.post("/tasks/quick")
async def submit_quick_task(data: QuickTaskData):
    """提交快速计算任务"""
    task = tasks.quick_task.delay({"numbers": data.numbers})
    return {
        "task_id": task.id,
        "status": "submitted",
        "message": "Quick calculation task submitted"
    }

@app.post("/tasks/email")
async def submit_email_task(data: EmailTaskData):
    """提交邮件发送任务"""
    task = tasks.email_task.delay(data.recipient, data.subject, data.message)
    return {
        "task_id": task.id,
        "status": "submitted",
        "message": f"Email task submitted for {data.recipient}"
    }

@app.post("/tasks/batch")
async def submit_batch_task(data: BatchProcessData):
    """提交批量用户处理任务"""
    task = tasks.batch_user_processing.delay(data.user_ids)
    return {
        "task_id": task.id,
        "status": "submitted",
        "message": f"Batch processing task submitted for {len(data.user_ids)} users"
    }

@app.post("/tasks/api-fetch")
async def submit_api_fetch_task(data: APIFetchData):
    """提交API数据获取任务"""
    task = tasks.api_data_fetch.delay(data.urls)
    return {
        "task_id": task.id,
        "status": "submitted",
        "message": f"API fetch task submitted for {len(data.urls)} URLs"
    }

@app.get("/tasks/{task_id}/status")
async def get_task_status(task_id: str):
    """获取任务状态"""
    try:
        task = celery_app.AsyncResult(task_id)
        
        if task.state == "PENDING":
            response = {
                "task_id": task_id,
                "state": task.state,
                "status": "Task is waiting to be processed"
            }
        elif task.state == "PROGRESS":
            response = {
                "task_id": task_id,
                "state": task.state,
                "current": task.info.get("current", 0),
                "total": task.info.get("total", 1),
                "progress": task.info.get("progress", 0),
                "status": "Task is currently being processed"
            }
        elif task.state == "SUCCESS":
            response = {
                "task_id": task_id,
                "state": task.state,
                "result": task.result,
                "status": "Task completed successfully"
            }
        else:  # FAILURE
            response = {
                "task_id": task_id,
                "state": task.state,
                "error": str(task.info),
                "status": "Task failed"
            }
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Task not found: {str(e)}")

@app.get("/tasks/{task_id}/result")
async def get_task_result(task_id: str):
    """获取任务结果"""
    try:
        task = celery_app.AsyncResult(task_id)
        
        if not task.ready():
            raise HTTPException(status_code=202, detail="Task is still processing")
        
        if task.successful():
            return {
                "task_id": task_id,
                "status": "success",
                "result": task.result
            }
        else:
            return {
                "task_id": task_id,
                "status": "failed",
                "error": str(task.info)
            }
            
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Task not found: {str(e)}")

@app.get("/tasks/")
async def get_all_tasks(db: Session = Depends(get_db)):
    """获取所有任务记录"""
    tasks = db.query(Task).order_by(Task.created_at.desc()).limit(50).all()
    return {
        "total": len(tasks),
        "tasks": [
            {
                "id": task.id,
                "task_id": task.task_id,
                "task_name": task.task_name,
                "status": task.status,
                "created_at": task.created_at,
                "updated_at": task.updated_at
            }
            for task in tasks
        ]
    }

@app.get("/tasks/active")
async def get_active_tasks():
    """获取当前活跃的任务"""
    try:
        inspect = celery_app.control.inspect()
        active_tasks = inspect.active()
        
        if not active_tasks:
            return {"active_tasks": [], "total": 0}
        
        all_active = []
        for worker, tasks in active_tasks.items():
            for task in tasks:
                all_active.append({
                    "worker": worker,
                    "task_id": task["id"],
                    "task_name": task["name"],
                    "args": task["args"],
                    "kwargs": task["kwargs"]
                })
        
        return {
            "active_tasks": all_active,
            "total": len(all_active),
            "workers": list(active_tasks.keys())
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get active tasks: {str(e)}")

@app.get("/users/")
async def get_users(db: Session = Depends(get_db)):
    """获取用户列表"""
    users = db.query(User).all()
    return {
        "total": len(users),
        "users": [
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "created_at": user.created_at
            }
            for user in users
        ]
    }

@app.post("/demo/run-concurrent-tasks")
async def run_concurrent_demo():
    """运行并发任务演示"""
    
    # 同时提交多个不同类型的任务
    tasks_submitted = []
    
    # 1. 长时间任务
    long_task = tasks.long_running_task.delay(30, "Demo Long Task")
    tasks_submitted.append({"type": "long_task", "task_id": long_task.id})
    
    # 2. 快速计算任务
    quick_task = tasks.quick_task.delay({"numbers": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]})
    tasks_submitted.append({"type": "quick_task", "task_id": quick_task.id})
    
    # 3. 邮件任务
    email_task = tasks.email_task.delay("demo@example.com", "Demo Email", "This is a demo email")
    tasks_submitted.append({"type": "email_task", "task_id": email_task.id})
    
    # 4. 批量处理任务
    batch_task = tasks.batch_user_processing.delay([1, 2, 3])
    tasks_submitted.append({"type": "batch_task", "task_id": batch_task.id})
    
    # 5. API获取任务
    api_task = tasks.api_data_fetch.delay([
        "https://jsonplaceholder.typicode.com/posts/1",
        "https://jsonplaceholder.typicode.com/posts/2",
        "https://jsonplaceholder.typicode.com/posts/3"
    ])
    tasks_submitted.append({"type": "api_task", "task_id": api_task.id})
    
    return {
        "message": "Concurrent demo tasks submitted successfully",
        "total_tasks": len(tasks_submitted),
        "tasks": tasks_submitted,
        "monitoring_urls": {
            "flower": "http://localhost:5555",
            "rabbitmq": "http://localhost:15672"
        }
    }
