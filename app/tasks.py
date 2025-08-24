import time
import random
import requests
from celery import current_task
from celery_app import celery_app
from database import SessionLocal, Task, User
from chain_handlers import (
    ProcessingRequest, RequestType, ChainBuilder, ChainProcessor
)
# 导入新的模块化处理器
from handlers.validation_handler import DataValidationHandler
from handlers.transformation_handler import DataTransformationHandler
from handlers.enrichment_handler import DataEnrichmentHandler
from handlers.export_handler import DataExportHandler, ReportExportHandler
from handlers.notification_handler import NotificationHandler, AlertHandler


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


# ===============================
# 责任链模式任务实现
# ===============================

@celery_app.task(bind=True, name="tasks.chain_data_processing")
def chain_data_processing(self, request_data: dict, chain_type: str = "standard"):
    """
    使用责任链模式处理数据的任务
    
    Args:
        request_data: 包含处理数据和配置的字典
        chain_type: 链类型 ("standard", "validation_only", "custom")
    """
    db = SessionLocal()
    try:
        task_record = Task(
            task_id=self.request.id,
            task_name="Chain Data Processing",
            status="RUNNING"
        )
        db.add(task_record)
        db.commit()
        
        # 创建处理请求
        request_type = RequestType(request_data.get('request_type', 'data_validation'))
        processing_request = ProcessingRequest(
            request_type=request_type,
            data=request_data.get('data', {}),
            metadata=request_data.get('metadata', {})
        )
        
        # 根据链类型构建处理链
        if chain_type == "standard":
            chain = ChainBuilder.build_standard_chain()
        elif chain_type == "validation_only":
            chain = DataValidationHandler()
        elif chain_type == "transform_export":
            handlers = [DataTransformationHandler(), DataExportHandler()]
            chain = ChainBuilder.build_custom_chain(handlers)
        elif chain_type == "enrich_notify":
            handlers = [DataEnrichmentHandler(), NotificationHandler()]
            chain = ChainBuilder.build_custom_chain(handlers)
        else:
            # 自定义链
            chain = ChainBuilder.build_standard_chain()
        
        # 创建处理器并执行
        processor = ChainProcessor(chain)
        
        # 更新任务进度
        current_task.update_state(
            state="PROGRESS",
            meta={"current": 1, "total": 3, "progress": 33, "status": "初始化处理链"}
        )
        
        # 执行处理链
        result = processor.process_request(processing_request)
        
        # 更新任务进度
        current_task.update_state(
            state="PROGRESS",
            meta={"current": 2, "total": 3, "progress": 66, "status": "处理链执行完成"}
        )
        
        # 添加额外的任务信息
        result['task_info'] = {
            'task_id': self.request.id,
            'chain_type': chain_type,
            'celery_worker': current_task.request.hostname
        }
        
        # 更新数据库
        task_record.status = "SUCCESS"
        task_record.result = str(result)
        db.commit()
        
        # 最终进度更新
        current_task.update_state(
            state="PROGRESS",
            meta={"current": 3, "total": 3, "progress": 100, "status": "任务完成"}
        )
        
        return result
        
    except Exception as e:
        task_record.status = "FAILURE"
        task_record.result = str(e)
        db.commit()
        raise e
    finally:
        db.close()


@celery_app.task(bind=True, name="tasks.batch_chain_processing")
def batch_chain_processing(self, batch_requests: list, chain_type: str = "standard"):
    """
    批量责任链处理任务
    
    Args:
        batch_requests: 批量请求列表
        chain_type: 链类型
    """
    db = SessionLocal()
    try:
        task_record = Task(
            task_id=self.request.id,
            task_name="Batch Chain Processing",
            status="RUNNING"
        )
        db.add(task_record)
        db.commit()
        
        total_requests = len(batch_requests)
        processed_results = []
        
        # 构建处理链
        if chain_type == "standard":
            chain = ChainBuilder.build_standard_chain()
        else:
            chain = ChainBuilder.build_standard_chain()
        
        processor = ChainProcessor(chain)
        
        for i, request_data in enumerate(batch_requests):
            try:
                # 创建处理请求
                request_type = RequestType(request_data.get('request_type', 'data_validation'))
                processing_request = ProcessingRequest(
                    request_type=request_type,
                    data=request_data.get('data', {}),
                    metadata=request_data.get('metadata', {})
                )
                
                # 执行处理
                result = processor.process_request(processing_request)
                result['batch_index'] = i
                processed_results.append(result)
                
                # 更新进度
                progress = int((i + 1) / total_requests * 100)
                current_task.update_state(
                    state="PROGRESS",
                    meta={
                        "current": i + 1,
                        "total": total_requests,
                        "progress": progress,
                        "status": f"处理第 {i + 1}/{total_requests} 个请求"
                    }
                )
                
                # 模拟处理间隔
                time.sleep(0.1)
                
            except Exception as e:
                processed_results.append({
                    'batch_index': i,
                    'error': str(e),
                    'success': False
                })
        
        # 生成批量处理结果
        batch_result = {
            'total_requests': total_requests,
            'successful_requests': len([r for r in processed_results if r.get('success', False)]),
            'failed_requests': len([r for r in processed_results if not r.get('success', True)]),
            'results': processed_results,
            'chain_type': chain_type,
            'processing_summary': {
                'total_errors': sum(len(r.get('errors', [])) for r in processed_results),
                'total_warnings': sum(len(r.get('warnings', [])) for r in processed_results),
                'average_processing_duration': sum(r.get('processing_duration', 0) for r in processed_results) / len(processed_results) if processed_results else 0
            }
        }
        
        # 更新数据库
        task_record.status = "SUCCESS"
        task_record.result = str(batch_result)
        db.commit()
        
        return batch_result
        
    except Exception as e:
        task_record.status = "FAILURE"
        task_record.result = str(e)
        db.commit()
        raise e
    finally:
        db.close()


@celery_app.task(bind=True, name="tasks.dynamic_chain_assembly")
def dynamic_chain_assembly(self, request_data: dict, handler_sequence: list):
    """
    动态组装责任链的任务
    
    Args:
        request_data: 处理数据
        handler_sequence: 处理器序列 ["validation", "transformation", "enrichment", "export", "notification"]
    """
    db = SessionLocal()
    try:
        task_record = Task(
            task_id=self.request.id,
            task_name="Dynamic Chain Assembly",
            status="RUNNING"
        )
        db.add(task_record)
        db.commit()
        
        # 创建处理请求
        request_type = RequestType(request_data.get('request_type', 'data_validation'))
        processing_request = ProcessingRequest(
            request_type=request_type,
            data=request_data.get('data', {}),
            metadata=request_data.get('metadata', {})
        )
        
        # 动态创建处理器
        handler_map = {
            'validation': DataValidationHandler(),
            'transformation': DataTransformationHandler(),
            'enrichment': DataEnrichmentHandler(),
            'export': DataExportHandler(),
            'notification': NotificationHandler()
        }
        
        # 根据序列构建处理器链
        handlers = []
        for handler_name in handler_sequence:
            if handler_name in handler_map:
                handlers.append(handler_map[handler_name])
        
        if not handlers:
            raise ValueError("没有有效的处理器序列")
        
        # 构建自定义链
        chain = ChainBuilder.build_custom_chain(handlers)
        processor = ChainProcessor(chain)
        
        # 更新进度
        current_task.update_state(
            state="PROGRESS",
            meta={
                "current": 1,
                "total": 2,
                "progress": 50,
                "status": f"组装了 {len(handlers)} 个处理器的链"
            }
        )
        
        # 执行处理链
        result = processor.process_request(processing_request)
        
        # 添加动态链信息
        result['dynamic_chain_info'] = {
            'handler_sequence': handler_sequence,
            'handlers_used': len(handlers),
            'task_id': self.request.id
        }
        
        # 更新数据库
        task_record.status = "SUCCESS"
        task_record.result = str(result)
        db.commit()
        
        # 最终进度
        current_task.update_state(
            state="PROGRESS",
            meta={
                "current": 2,
                "total": 2,
                "progress": 100,
                "status": "动态链处理完成"
            }
        )
        
        return result
        
    except Exception as e:
        task_record.status = "FAILURE"
        task_record.result = str(e)
        db.commit()
        raise e
    finally:
        db.close()
