"""
责任链设计模式实现 - 用于处理不同类型的数据处理任务
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
import time
import logging
from enum import Enum

# 导入新的模块化处理器
from handlers.validation_handler import DataValidationHandler
from handlers.transformation_handler import DataTransformationHandler
from handlers.enrichment_handler import DataEnrichmentHandler
from handlers.export_handler import DataExportHandler, ReportExportHandler
from handlers.notification_handler import NotificationHandler, AlertHandler

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
    
    def get_logs(self) -> List[Dict[str, Any]]:
        """获取所有日志"""
        return self.processing_log


class BaseHandler(ABC):
    """抽象处理器基类"""
    
    def __init__(self, name: str):
        self.name = name
        self.next_handler: Optional['BaseHandler'] = None
    
    def set_next(self, handler: 'BaseHandler') -> 'BaseHandler':
        """设置下一个处理器"""
        self.next_handler = handler
        return handler
    
    @abstractmethod
    def can_handle(self, request: ProcessingRequest) -> bool:
        """判断是否能处理该请求"""
        pass
    
    @abstractmethod
    def process(self, request: ProcessingRequest) -> ProcessingRequest:
        """处理请求"""
        pass
    
    def handle(self, request: ProcessingRequest) -> ProcessingRequest:
        """处理请求的入口方法"""
        try:
            if self.can_handle(request):
                logger.info(f"{self.name} 开始处理请求")
                request = self.process(request)
                logger.info(f"{self.name} 处理完成")
            
            # 传递给下一个处理器
            if self.next_handler:
                return self.next_handler.handle(request)
            
            return request
            
        except Exception as e:
            error_msg = f"处理器 {self.name} 发生错误: {str(e)}"
            logger.error(error_msg)
            request.add_error(self.name, error_msg)
            return request


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


class DataValidationHandler(BaseHandler):
    """数据验证处理器"""
    
    def __init__(self):
        super().__init__("DataValidationHandler")
    
    def can_handle(self, request: ProcessingRequest) -> bool:
        return request.request_type == RequestType.DATA_VALIDATION
    
    def process(self, request: ProcessingRequest) -> ProcessingRequest:
        """执行数据验证"""
        data = request.data
        
        # 检查必填字段
        required_fields = data.get('required_fields', [])
        payload = data.get('payload', {})
        
        missing_fields = []
        for field in required_fields:
            if field not in payload:
                missing_fields.append(field)
        
        if missing_fields:
            request.add_error(self.name, f"缺少必填字段: {missing_fields}")
            return request
        
        # 验证数据类型
        validation_rules = data.get('validation_rules', {})
        for field, rule in validation_rules.items():
            if field in payload:
                value = payload[field]
                if rule.get('type') == 'string' and not isinstance(value, str):
                    request.add_error(self.name, f"字段 {field} 应为字符串类型")
                elif rule.get('type') == 'number' and not isinstance(value, (int, float)):
                    request.add_error(self.name, f"字段 {field} 应为数字类型")
                elif rule.get('min_length') and len(str(value)) < rule['min_length']:
                    request.add_warning(self.name, f"字段 {field} 长度不足最小要求")
        
        # 模拟验证处理时间
        time.sleep(0.5)
        
        request.add_log(self.name, f"验证了 {len(payload)} 个字段")
        return request


class DataTransformationHandler(BaseHandler):
    """数据转换处理器"""
    
    def __init__(self):
        super().__init__("DataTransformationHandler")
    
    def can_handle(self, request: ProcessingRequest) -> bool:
        return request.request_type == RequestType.DATA_TRANSFORMATION
    
    def process(self, request: ProcessingRequest) -> ProcessingRequest:
        """执行数据转换"""
        data = request.data
        payload = data.get('payload', {})
        transformations = data.get('transformations', {})
        
        transformed_data = payload.copy()
        
        for field, transformation in transformations.items():
            if field in transformed_data:
                value = transformed_data[field]
                
                if transformation == 'uppercase':
                    transformed_data[field] = str(value).upper()
                elif transformation == 'lowercase':
                    transformed_data[field] = str(value).lower()
                elif transformation == 'strip':
                    transformed_data[field] = str(value).strip()
                elif transformation == 'to_number':
                    try:
                        transformed_data[field] = float(value)
                    except ValueError:
                        request.add_warning(self.name, f"无法将 {field} 转换为数字")
                elif transformation.startswith('multiply_'):
                    factor = float(transformation.split('_')[1])
                    try:
                        transformed_data[field] = float(value) * factor
                    except ValueError:
                        request.add_warning(self.name, f"无法对 {field} 执行乘法运算")
        
        # 添加转换后的数据
        request.data['transformed_payload'] = transformed_data
        
        # 模拟转换处理时间
        time.sleep(0.3)
        
        request.add_log(self.name, f"转换了 {len(transformations)} 个字段")
        return request


class DataEnrichmentHandler(BaseHandler):
    """数据丰富化处理器"""
    
    def __init__(self):
        super().__init__("DataEnrichmentHandler")
    
    def can_handle(self, request: ProcessingRequest) -> bool:
        return request.request_type == RequestType.DATA_ENRICHMENT
    
    def process(self, request: ProcessingRequest) -> ProcessingRequest:
        """执行数据丰富化"""
        data = request.data
        payload = data.get('payload', {})
        
        # 添加元数据
        enriched_data = payload.copy()
        enriched_data['_metadata'] = {
            'processed_at': time.time(),
            'processor': self.name,
            'version': '1.0',
            'enrichment_rules_applied': []
        }
        
        # 根据现有数据推导新字段
        if 'first_name' in payload and 'last_name' in payload:
            enriched_data['full_name'] = f"{payload['first_name']} {payload['last_name']}"
            enriched_data['_metadata']['enrichment_rules_applied'].append('full_name_generation')
        
        if 'age' in payload:
            age = payload['age']
            if isinstance(age, (int, float)):
                if age < 18:
                    enriched_data['age_category'] = 'minor'
                elif age < 65:
                    enriched_data['age_category'] = 'adult'
                else:
                    enriched_data['age_category'] = 'senior'
                enriched_data['_metadata']['enrichment_rules_applied'].append('age_categorization')
        
        if 'email' in payload:
            email = payload['email']
            if '@' in str(email):
                domain = str(email).split('@')[1]
                enriched_data['email_domain'] = domain
                enriched_data['_metadata']['enrichment_rules_applied'].append('email_domain_extraction')
        
        # 添加地理位置信息（模拟）
        if 'country' in payload:
            country_info = {
                'USA': {'continent': 'North America', 'timezone': 'UTC-5'},
                'China': {'continent': 'Asia', 'timezone': 'UTC+8'},
                'Germany': {'continent': 'Europe', 'timezone': 'UTC+1'},
                'Japan': {'continent': 'Asia', 'timezone': 'UTC+9'}
            }
            country = payload['country']
            if country in country_info:
                enriched_data['geo_info'] = country_info[country]
                enriched_data['_metadata']['enrichment_rules_applied'].append('geo_enrichment')
        
        request.data['enriched_payload'] = enriched_data
        
        # 模拟丰富化处理时间
        time.sleep(0.7)
        
        rules_count = len(enriched_data['_metadata']['enrichment_rules_applied'])
        request.add_log(self.name, f"应用了 {rules_count} 个丰富化规则")
        return request


class DataExportHandler(BaseHandler):
    """数据导出处理器"""
    
    def __init__(self):
        super().__init__("DataExportHandler")
    
    def can_handle(self, request: ProcessingRequest) -> bool:
        return request.request_type == RequestType.DATA_EXPORT
    
    def process(self, request: ProcessingRequest) -> ProcessingRequest:
        """执行数据导出"""
        data = request.data
        export_format = data.get('export_format', 'json')
        payload = data.get('payload', {})
        
        export_result = {
            'format': export_format,
            'size_bytes': 0,
            'record_count': 0,
            'export_location': '',
            'export_time': time.time()
        }
        
        if export_format == 'json':
            import json
            exported_data = json.dumps(payload, indent=2)
            export_result['size_bytes'] = len(exported_data.encode('utf-8'))
            export_result['export_location'] = '/exports/data.json'
            
        elif export_format == 'csv':
            # 模拟 CSV 导出
            if isinstance(payload, dict):
                headers = list(payload.keys())
                export_result['size_bytes'] = len(','.join(headers)) + len(','.join(str(v) for v in payload.values()))
                export_result['export_location'] = '/exports/data.csv'
            
        elif export_format == 'xml':
            # 模拟 XML 导出
            xml_content = f"<data>{len(str(payload))}</data>"
            export_result['size_bytes'] = len(xml_content.encode('utf-8'))
            export_result['export_location'] = '/exports/data.xml'
        
        if isinstance(payload, dict):
            export_result['record_count'] = 1
        elif isinstance(payload, list):
            export_result['record_count'] = len(payload)
        
        request.data['export_result'] = export_result
        
        # 模拟导出处理时间
        time.sleep(0.4)
        
        request.add_log(self.name, f"导出为 {export_format} 格式，大小: {export_result['size_bytes']} 字节")
        return request


class NotificationHandler(BaseHandler):
    """通知处理器"""
    
    def __init__(self):
        super().__init__("NotificationHandler")
    
    def can_handle(self, request: ProcessingRequest) -> bool:
        return request.request_type == RequestType.NOTIFICATION
    
    def process(self, request: ProcessingRequest) -> ProcessingRequest:
        """执行通知发送"""
        data = request.data
        notification_type = data.get('notification_type', 'email')
        recipients = data.get('recipients', [])
        message = data.get('message', '')
        
        notification_result = {
            'type': notification_type,
            'recipients_count': len(recipients),
            'message_length': len(message),
            'sent_at': time.time(),
            'delivery_status': []
        }
        
        # 模拟发送通知
        for recipient in recipients:
            # 模拟发送成功率 90%
            import random
            success = random.random() > 0.1
            
            status = {
                'recipient': recipient,
                'status': 'delivered' if success else 'failed',
                'timestamp': time.time()
            }
            
            if not success:
                status['error'] = 'Connection timeout'
                request.add_warning(self.name, f"发送给 {recipient} 失败")
            
            notification_result['delivery_status'].append(status)
        
        request.data['notification_result'] = notification_result
        
        # 模拟通知处理时间
        time.sleep(0.6)
        
        successful_sends = sum(1 for status in notification_result['delivery_status'] if status['status'] == 'delivered')
        request.add_log(self.name, f"发送了 {successful_sends}/{len(recipients)} 个通知")
        return request


class ChainBuilder:
    """责任链构建器"""
    
    @staticmethod
    def build_standard_chain() -> BaseHandler:
        """构建标准处理链"""
        validation_handler = DataValidationHandler()
        transformation_handler = DataTransformationHandler()
        enrichment_handler = DataEnrichmentHandler()
        export_handler = DataExportHandler()
        notification_handler = NotificationHandler()
        
        # 构建链条
        validation_handler.set_next(transformation_handler) \
                         .set_next(enrichment_handler) \
                         .set_next(export_handler) \
                         .set_next(notification_handler)
        
        return validation_handler
    
    @staticmethod
    def build_custom_chain(handlers: List[BaseHandler]) -> BaseHandler:
        """构建自定义处理链"""
        if not handlers:
            raise ValueError("处理器列表不能为空")
        
        for i in range(len(handlers) - 1):
            handlers[i].set_next(handlers[i + 1])
        
        return handlers[0]


class ChainProcessor:
    """责任链处理器包装类"""
    
    def __init__(self, chain: BaseHandler):
        self.chain = chain
    
    def process_request(self, request: ProcessingRequest) -> Dict[str, Any]:
        """处理请求并返回详细结果"""
        start_time = time.time()
        
        # 执行处理链
        processed_request = self.chain.handle(request)
        
        end_time = time.time()
        processing_duration = end_time - start_time
        
        # 构建返回结果
        result = {
            'request_id': id(request),
            'request_type': request.request_type.value,
            'processing_duration': processing_duration,
            'total_handlers': len(processed_request.processing_log),
            'success': len(processed_request.errors) == 0,
            'errors': processed_request.errors,
            'warnings': processed_request.warnings,
            'processing_log': processed_request.processing_log,
            'original_data': request.data,
            'processed_data': {
                'transformed_payload': processed_request.data.get('transformed_payload'),
                'enriched_payload': processed_request.data.get('enriched_payload'),
                'export_result': processed_request.data.get('export_result'),
                'notification_result': processed_request.data.get('notification_result')
            },
            'metadata': processed_request.metadata
        }
        
        return result
