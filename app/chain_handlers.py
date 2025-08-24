"""
责任链设计模式实现 - 用于处理不同类型的数据处理任务
"""
import time
import logging
from typing import Optional

# 导入基础类
from handlers import BaseHandler, ProcessingRequest, RequestType

# 导入新的模块化处理器
from handlers.validation_handler import DataValidationHandler
from handlers.transformation_handler import DataTransformationHandler
from handlers.enrichment_handler import DataEnrichmentHandler
from handlers.export_handler import DataExportHandler, ReportExportHandler
from handlers.notification_handler import NotificationHandler, AlertHandler

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ChainBuilder:
    """责任链构建器"""
    
    def __init__(self):
        self.handlers = []
    
    def add_handler(self, handler: BaseHandler) -> 'ChainBuilder':
        """添加处理器"""
        self.handlers.append(handler)
        return self
    
    def build(self) -> Optional[BaseHandler]:
        """构建责任链"""
        if not self.handlers:
            return None
        
        # 链接所有处理器
        for i in range(len(self.handlers) - 1):
            self.handlers[i].set_next(self.handlers[i + 1])
        
        return self.handlers[0]  # 返回第一个处理器


class ChainProcessor:
    """责任链处理器"""
    
    def __init__(self):
        self.default_chain = None
        self.custom_chains = {}
    
    def set_default_chain(self, chain: BaseHandler):
        """设置默认责任链"""
        self.default_chain = chain
    
    def add_custom_chain(self, name: str, chain: BaseHandler):
        """添加自定义责任链"""
        self.custom_chains[name] = chain
    
    def process(self, request: ProcessingRequest, chain_name: Optional[str] = None) -> ProcessingRequest:
        """处理请求"""
        # 选择责任链
        if chain_name and chain_name in self.custom_chains:
            chain = self.custom_chains[chain_name]
        elif self.default_chain:
            chain = self.default_chain
        else:
            request.add_error("ChainProcessor", "未找到可用的责任链")
            return request
        
        # 执行处理
        start_time = time.time()
        result = chain.handle(request)
        processing_time = time.time() - start_time
        
        # 添加处理时间到元数据
        result.metadata['processing_time'] = processing_time
        result.metadata['total_handlers'] = len(result.processing_log)
        
        return result
    
    def build_standard_chain(self) -> BaseHandler:
        """构建标准数据处理链"""
        return (ChainBuilder()
                .add_handler(DataValidationHandler())
                .add_handler(DataTransformationHandler())
                .add_handler(DataEnrichmentHandler())
                .add_handler(DataExportHandler())
                .add_handler(NotificationHandler())
                .build())
    
    def build_validation_chain(self) -> BaseHandler:
        """构建验证链"""
        return (ChainBuilder()
                .add_handler(DataValidationHandler())
                .add_handler(NotificationHandler())
                .build())
    
    def build_export_chain(self) -> BaseHandler:
        """构建导出链"""
        return (ChainBuilder()
                .add_handler(DataExportHandler())
                .add_handler(NotificationHandler())
                .build())
    
    def build_enrichment_chain(self) -> BaseHandler:
        """构建丰富化链"""
        return (ChainBuilder()
                .add_handler(DataValidationHandler())
                .add_handler(DataEnrichmentHandler())
                .add_handler(DataExportHandler())
                .add_handler(NotificationHandler())
                .build())
