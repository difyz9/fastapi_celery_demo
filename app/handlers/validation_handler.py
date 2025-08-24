"""
数据验证处理器
"""
import time
from handlers import BaseHandler, ProcessingRequest, RequestType


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
        validation_result = self._validate_required_fields(data, request)
        if not validation_result:
            return request
        
        # 验证数据类型
        self._validate_data_types(data, request)
        
        # 验证业务规则
        self._validate_business_rules(data, request)
        
        # 模拟验证处理时间
        time.sleep(0.5)
        
        payload = data.get('payload', {})
        request.add_log(self.name, f"验证了 {len(payload)} 个字段")
        return request
    
    def _validate_required_fields(self, data: dict, request: ProcessingRequest) -> bool:
        """验证必填字段"""
        required_fields = data.get('required_fields', [])
        payload = data.get('payload', {})
        
        missing_fields = []
        for field in required_fields:
            if field not in payload:
                missing_fields.append(field)
        
        if missing_fields:
            request.add_error(self.name, f"缺少必填字段: {missing_fields}")
            return False
        
        return True
    
    def _validate_data_types(self, data: dict, request: ProcessingRequest):
        """验证数据类型"""
        validation_rules = data.get('validation_rules', {})
        payload = data.get('payload', {})
        
        for field, rule in validation_rules.items():
            if field in payload:
                value = payload[field]
                field_type = rule.get('type')
                
                if field_type == 'string' and not isinstance(value, str):
                    request.add_error(self.name, f"字段 {field} 应为字符串类型")
                elif field_type == 'number' and not isinstance(value, (int, float)):
                    request.add_error(self.name, f"字段 {field} 应为数字类型")
                elif field_type == 'email' and not self._is_valid_email(value):
                    request.add_error(self.name, f"字段 {field} 不是有效的邮箱格式")
                elif field_type == 'phone' and not self._is_valid_phone(value):
                    request.add_warning(self.name, f"字段 {field} 可能不是有效的电话号码格式")
    
    def _validate_business_rules(self, data: dict, request: ProcessingRequest):
        """验证业务规则"""
        validation_rules = data.get('validation_rules', {})
        payload = data.get('payload', {})
        
        for field, rule in validation_rules.items():
            if field in payload:
                value = payload[field]
                
                # 最小长度检查
                if rule.get('min_length') and len(str(value)) < rule['min_length']:
                    request.add_warning(self.name, f"字段 {field} 长度不足最小要求 {rule['min_length']}")
                
                # 最大长度检查
                if rule.get('max_length') and len(str(value)) > rule['max_length']:
                    request.add_error(self.name, f"字段 {field} 长度超过最大限制 {rule['max_length']}")
                
                # 数值范围检查
                if rule.get('min_value') and isinstance(value, (int, float)) and value < rule['min_value']:
                    request.add_error(self.name, f"字段 {field} 值小于最小值 {rule['min_value']}")
                
                if rule.get('max_value') and isinstance(value, (int, float)) and value > rule['max_value']:
                    request.add_error(self.name, f"字段 {field} 值大于最大值 {rule['max_value']}")
                
                # 正则表达式验证
                if rule.get('pattern'):
                    import re
                    if not re.match(rule['pattern'], str(value)):
                        request.add_error(self.name, f"字段 {field} 不匹配所需格式")
    
    def _is_valid_email(self, email: str) -> bool:
        """验证邮箱格式"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, str(email)) is not None
    
    def _is_valid_phone(self, phone: str) -> bool:
        """验证电话号码格式（简单验证）"""
        import re
        # 支持多种电话号码格式
        patterns = [
            r'^\+?1?[-.\s]?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}$',  # 美国格式
            r'^\+?86[-.\s]?1[0-9]{10}$',  # 中国手机格式
            r'^\+?[0-9]{1,4}[-.\s]?[0-9]{1,4}[-.\s]?[0-9]{1,4}[-.\s]?[0-9]{1,4}$'  # 通用格式
        ]
        return any(re.match(pattern, str(phone)) for pattern in patterns)
