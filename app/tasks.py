import time
import random
import requests
from celery import current_task
from celery_app import celery_app
from database import SessionLocal, Task, User


@celery_app.task(bind=True, name="tasks.long_running_task")
def long_running_task(self, duration: int = 60, task_name: str = "Long Task"):
    """
    长时间运行的任务，模拟数据处理
    """
    # 保存任务信息到数据库
    db = SessionLocal()
    try:
        task_record = Task(
            task_id=self.request.id,
            task_name=task_name,
            status="RUNNING"
        )
        db.add(task_record)
        db.commit()
        
        total_steps = duration
        for i in range(total_steps):
            time.sleep(1)  # 模拟处理时间
            
            # 更新任务进度
            progress = int((i + 1) / total_steps * 100)
            current_task.update_state(
                state="PROGRESS",
                meta={"current": i + 1, "total": total_steps, "progress": progress}
            )
        
        # 生成模拟结果
        result = {
            "status": "completed",
            "processed_items": total_steps,
            "execution_time": duration,
            "result_data": f"Processed {total_steps} items successfully"
        }
        
        # 更新数据库
        task_record.status = "SUCCESS"
        task_record.result = str(result)
        db.commit()
        
        return result
        
    except Exception as e:
        # 更新数据库状态为失败
        task_record.status = "FAILURE"
        task_record.result = str(e)
        db.commit()
        raise e
    finally:
        db.close()


@celery_app.task(name="tasks.quick_task")
def quick_task(data: dict):
    """
    快速任务，模拟简单计算
    """
    db = SessionLocal()
    try:
        task_record = Task(
            task_id=current_task.request.id,
            task_name="Quick Calculation",
            status="RUNNING"
        )
        db.add(task_record)
        db.commit()
        
        # 模拟快速计算
        numbers = data.get("numbers", [1, 2, 3, 4, 5])
        result = {
            "sum": sum(numbers),
            "avg": sum(numbers) / len(numbers),
            "max": max(numbers),
            "min": min(numbers),
            "count": len(numbers)
        }
        
        # 更新数据库
        task_record.status = "SUCCESS"
        task_record.result = str(result)
        db.commit()
        
        return result
        
    except Exception as e:
        task_record.status = "FAILURE"
        task_record.result = str(e)
        db.commit()
        raise e
    finally:
        db.close()


@celery_app.task(name="tasks.email_task")
def email_task(recipient: str, subject: str, message: str):
    """
    模拟邮件发送任务
    """
    db = SessionLocal()
    try:
        task_record = Task(
            task_id=current_task.request.id,
            task_name="Email Sending",
            status="RUNNING"
        )
        db.add(task_record)
        db.commit()
        
        # 模拟邮件发送延迟
        time.sleep(random.uniform(2, 5))
        
        # 模拟发送结果
        success = random.choice([True, True, True, False])  # 75% 成功率
        
        if success:
            result = {
                "status": "sent",
                "recipient": recipient,
                "subject": subject,
                "sent_at": time.time(),
                "message_id": f"msg_{random.randint(1000, 9999)}"
            }
            task_record.status = "SUCCESS"
        else:
            result = {
                "status": "failed",
                "recipient": recipient,
                "error": "SMTP connection timeout"
            }
            task_record.status = "FAILURE"
        
        task_record.result = str(result)
        db.commit()
        
        return result
        
    except Exception as e:
        task_record.status = "FAILURE"
        task_record.result = str(e)
        db.commit()
        raise e
    finally:
        db.close()


@celery_app.task(name="tasks.batch_user_processing")
def batch_user_processing(user_ids: list):
    """
    批量处理用户数据
    """
    db = SessionLocal()
    try:
        task_record = Task(
            task_id=current_task.request.id,
            task_name="Batch User Processing",
            status="RUNNING"
        )
        db.add(task_record)
        db.commit()
        
        processed_users = []
        total_users = len(user_ids)
        
        for i, user_id in enumerate(user_ids):
            # 查询用户
            user = db.query(User).filter(User.id == user_id).first()
            if user:
                # 模拟处理时间
                time.sleep(random.uniform(0.5, 2))
                
                processed_users.append({
                    "user_id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "processed_at": time.time()
                })
                
                # 更新进度
                progress = int((i + 1) / total_users * 100)
                current_task.update_state(
                    state="PROGRESS",
                    meta={
                        "current": i + 1,
                        "total": total_users,
                        "progress": progress,
                        "processed_users": len(processed_users)
                    }
                )
        
        result = {
            "status": "completed",
            "total_requested": total_users,
            "successfully_processed": len(processed_users),
            "processed_users": processed_users
        }
        
        task_record.status = "SUCCESS"
        task_record.result = str(result)
        db.commit()
        
        return result
        
    except Exception as e:
        task_record.status = "FAILURE"
        task_record.result = str(e)
        db.commit()
        raise e
    finally:
        db.close()


@celery_app.task(name="tasks.api_data_fetch")
def api_data_fetch(urls: list):
    """
    并发获取多个API数据
    """
    db = SessionLocal()
    try:
        task_record = Task(
            task_id=current_task.request.id,
            task_name="API Data Fetching",
            status="RUNNING"
        )
        db.add(task_record)
        db.commit()
        
        results = []
        total_urls = len(urls)
        
        for i, url in enumerate(urls):
            try:
                # 模拟API调用
                response_data = {
                    "url": url,
                    "status": "success",
                    "data": f"Mock data from {url}",
                    "response_time": random.uniform(0.1, 2.0),
                    "timestamp": time.time()
                }
                results.append(response_data)
                
            except Exception as e:
                results.append({
                    "url": url,
                    "status": "error",
                    "error": str(e),
                    "timestamp": time.time()
                })
            
            # 更新进度
            progress = int((i + 1) / total_urls * 100)
            current_task.update_state(
                state="PROGRESS",
                meta={
                    "current": i + 1,
                    "total": total_urls,
                    "progress": progress,
                    "completed_requests": len(results)
                }
            )
            
            # 模拟请求间隔
            time.sleep(random.uniform(0.5, 1.5))
        
        final_result = {
            "status": "completed",
            "total_urls": total_urls,
            "successful_requests": len([r for r in results if r["status"] == "success"]),
            "failed_requests": len([r for r in results if r["status"] == "error"]),
            "results": results
        }
        
        task_record.status = "SUCCESS"
        task_record.result = str(final_result)
        db.commit()
        
        return final_result
        
    except Exception as e:
        task_record.status = "FAILURE"
        task_record.result = str(e)
        db.commit()
        raise e
    finally:
        db.close()
