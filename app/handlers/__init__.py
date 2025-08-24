"""
处理器基础类和公共接口
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
import time
import logging
from enum import Enum

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RequestType(Enum):
    """请求类型枚举"""
    DATA_VALIDATION = "data_validation"
    DATA_TRANSFORMATION = "data_transformation"
    DATA_ENRICHMENT = "data_enrichment"
    DATA_EXPORT = "data_export"
    NOTIFICATION = "notification"


class ProcessingRequest:
    """处理请求对象"""
    
    def __init__(self, request_type: RequestType, data: Dict[str, Any], 
                 metadata: Optional[Dict[str, Any]] = None):
        self.request_type = request_type
        self.data = data
        self.metadata = metadata or {}
        self.processing_log = []
        self.created_at = time.time()
        self.errors = []
        self.warnings = []
    
    def add_log(self, handler_name: str, message: str, status: str = "INFO"):
        """添加处理日志"""
        self.processing_log.append({
            "handler": handler_name,
            "message": message,
            "status": status,
            "timestamp": time.time()
        })
    
    def add_error(self, handler_name: str, error: str):
        """添加错误信息"""
        self.errors.append({
            "handler": handler_name,
            "error": error,
            "timestamp": time.time()
        })
    
    def add_warning(self, handler_name: str, warning: str):
        """添加警告信息"""
        self.warnings.append({
            "handler": handler_name,
            "warning": warning,
            "timestamp": time.time()
        })


class BaseHandler(ABC):
    """处理器基类"""
    
    def __init__(self, name: str):
        self.name = name
        self._next_handler: Optional['BaseHandler'] = None
    
    def set_next(self, handler: 'BaseHandler') -> 'BaseHandler':
        """设置下一个处理器"""
        self._next_handler = handler
        return handler
    
    def handle(self, request: ProcessingRequest) -> ProcessingRequest:
        """处理请求"""
        if self.can_handle(request):
            logger.info(f"{self.name} 正在处理请求类型: {request.request_type.value}")
            request.add_log(self.name, f"开始处理请求", "INFO")
            try:
                request = self.process(request)
                request.add_log(self.name, f"处理完成", "SUCCESS")
            except Exception as e:
                error_msg = f"处理失败: {str(e)}"
                request.add_error(self.name, error_msg)
                logger.error(f"{self.name}: {error_msg}")
        
        # 传递给下一个处理器
        if self._next_handler:
            return self._next_handler.handle(request)
        
        return request
    
    @abstractmethod
    def can_handle(self, request: ProcessingRequest) -> bool:
        """判断是否可以处理此请求"""
        pass
    
    @abstractmethod
    def process(self, request: ProcessingRequest) -> ProcessingRequest:
        """具体的处理逻辑"""
        pass
