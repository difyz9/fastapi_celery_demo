"""
数据转换处理器
"""
import time
import re
from handlers import BaseHandler, ProcessingRequest, RequestType


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
        transformation_count = 0
        
        for field, transformation in transformations.items():
            if field in transformed_data:
                original_value = transformed_data[field]
                
                try:
                    new_value = self._apply_transformation(original_value, transformation, request)
                    if new_value != original_value:
                        transformed_data[field] = new_value
                        transformation_count += 1
                        request.add_log(
                            self.name, 
                            f"字段 {field}: {transformation} ({original_value} -> {new_value})"
                        )
                except Exception as e:
                    request.add_error(self.name, f"转换字段 {field} 时出错: {str(e)}")
        
        # 添加转换后的数据
        request.data['transformed_payload'] = transformed_data
        
        # 模拟转换处理时间
        time.sleep(0.3)
        
        request.add_log(self.name, f"成功转换了 {transformation_count} 个字段")
        return request
    
    def _apply_transformation(self, value, transformation: str, request):
        """应用具体的转换逻辑"""
        if transformation == 'uppercase':
            return str(value).upper()
        
        elif transformation == 'lowercase':
            return str(value).lower()
        
        elif transformation == 'strip':
            return str(value).strip()
        
        elif transformation == 'title_case':
            return str(value).title()
        
        elif transformation == 'capitalize':
            return str(value).capitalize()
        
        elif transformation == 'to_number':
            return self._convert_to_number(value)
        
        elif transformation == 'to_string':
            return str(value)
        
        elif transformation == 'to_boolean':
            return self._convert_to_boolean(value)
        
        elif transformation.startswith('multiply_'):
            factor = float(transformation.split('_')[1])
            return float(value) * factor
        
        elif transformation.startswith('divide_'):
            divisor = float(transformation.split('_')[1])
            if divisor == 0:
                raise ValueError("除数不能为零")
            return float(value) / divisor
        
        elif transformation.startswith('add_'):
            addend = float(transformation.split('_')[1])
            return float(value) + addend
        
        elif transformation.startswith('subtract_'):
            subtrahend = float(transformation.split('_')[1])
            return float(value) - subtrahend
        
        elif transformation.startswith('round_'):
            decimals = int(transformation.split('_')[1])
            return round(float(value), decimals)
        
        elif transformation == 'remove_spaces':
            return str(value).replace(' ', '')
        
        elif transformation == 'remove_special_chars':
            return re.sub(r'[^a-zA-Z0-9\s]', '', str(value))
        
        elif transformation == 'extract_numbers':
            return ''.join(re.findall(r'\d', str(value)))
        
        elif transformation == 'extract_letters':
            return ''.join(re.findall(r'[a-zA-Z]', str(value)))
        
        elif transformation.startswith('substring_'):
            # substring_start_end 格式
            parts = transformation.split('_')
            if len(parts) >= 2:
                start = int(parts[1])
                end = int(parts[2]) if len(parts) > 2 else None
                return str(value)[start:end]
        
        elif transformation.startswith('replace_'):
            # replace_old_new 格式
            parts = transformation.split('_', 2)
            if len(parts) == 3:
                old, new = parts[1], parts[2]
                return str(value).replace(old, new)
        
        elif transformation == 'reverse':
            return str(value)[::-1]
        
        elif transformation.startswith('format_'):
            # format_template 格式，例如 format_{:02d}
            template = transformation.split('_', 1)[1]
            return template.format(value)
        
        elif transformation == 'normalize_phone':
            return self._normalize_phone_number(str(value))
        
        elif transformation == 'normalize_email':
            return str(value).lower().strip()
        
        elif transformation == 'generate_slug':
            return self._generate_slug(str(value))
        
        else:
            request.add_warning(self.name, f"未知的转换类型: {transformation}")
            return value
    
    def _convert_to_number(self, value):
        """转换为数字"""
        try:
            # 尝试转换为整数
            if '.' not in str(value):
                return int(value)
            else:
                return float(value)
        except ValueError:
            raise ValueError(f"无法将 '{value}' 转换为数字")
    
    def _convert_to_boolean(self, value):
        """转换为布尔值"""
        if isinstance(value, bool):
            return value
        
        str_value = str(value).lower().strip()
        if str_value in ['true', '1', 'yes', 'on', 'enabled']:
            return True
        elif str_value in ['false', '0', 'no', 'off', 'disabled']:
            return False
        else:
            raise ValueError(f"无法将 '{value}' 转换为布尔值")
    
    def _normalize_phone_number(self, phone: str) -> str:
        """标准化电话号码格式"""
        # 移除所有非数字字符
        digits = re.sub(r'\D', '', phone)
        
        # 根据长度判断格式
        if len(digits) == 10:
            # 美国格式 (123) 456-7890
            return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
        elif len(digits) == 11 and digits.startswith('1'):
            # 美国格式带国家码 +1 (123) 456-7890
            return f"+1 ({digits[1:4]}) {digits[4:7]}-{digits[7:]}"
        elif len(digits) == 11 and digits.startswith('86'):
            # 中国格式 +86 138-0013-8000
            return f"+86 {digits[2:5]}-{digits[5:9]}-{digits[9:]}"
        else:
            # 保持原格式
            return phone
    
    def _generate_slug(self, text: str) -> str:
        """生成URL友好的slug"""
        # 转小写
        text = text.lower()
        # 替换空格为连字符
        text = re.sub(r'\s+', '-', text)
        # 移除特殊字符，只保留字母、数字和连字符
        text = re.sub(r'[^a-z0-9\-]', '', text)
        # 移除多余的连字符
        text = re.sub(r'-+', '-', text)
        # 移除首尾连字符
        return text.strip('-')
