"""
数据导出处理器
"""
import json
import csv
import time
import xml.etree.ElementTree as ET
from io import StringIO
from handlers import BaseHandler, ProcessingRequest, RequestType


class DataExportHandler(BaseHandler):
    """数据导出处理器"""
    
    def __init__(self):
        super().__init__("DataExportHandler")
        self._export_formats = {
            'json': self._export_json,
            'csv': self._export_csv,
            'xml': self._export_xml,
            'excel': self._export_excel,
            'txt': self._export_txt,
            'yaml': self._export_yaml
        }
    
    def can_handle(self, request: ProcessingRequest) -> bool:
        return request.request_type == RequestType.DATA_EXPORT
    
    def process(self, request: ProcessingRequest) -> ProcessingRequest:
        """执行数据导出"""
        data = request.data
        export_config = data.get('export_config', {})
        
        # 获取导出格式
        export_format = export_config.get('format', 'json').lower()
        
        # 获取要导出的数据
        export_data = self._prepare_export_data(data, export_config)
        
        # 执行导出
        if export_format in self._export_formats:
            exported_content = self._export_formats[export_format](export_data, export_config)
            
            # 保存导出结果
            export_result = {
                'format': export_format,
                'content': exported_content,
                'size_bytes': len(exported_content.encode('utf-8')),
                'record_count': self._count_records(export_data),
                'exported_at': time.time(),
                'config': export_config
            }
            
            # 添加文件信息
            if 'filename' not in export_config:
                export_config['filename'] = f"export_{int(time.time())}.{export_format}"
            
            export_result['filename'] = export_config['filename']
            
            # 如果需要保存到文件
            if export_config.get('save_to_file', False):
                self._save_to_file(exported_content, export_result['filename'])
                export_result['file_saved'] = True
            
            request.data['export_result'] = export_result
            
            # 模拟导出处理时间
            time.sleep(0.5)
            
            request.add_log(self.name, f"导出 {export_result['record_count']} 条记录为 {export_format.upper()} 格式")
        else:
            request.add_log(self.name, f"不支持的导出格式: {export_format}")
            request.data['export_error'] = f"Unsupported format: {export_format}"
        
        return request
    
    def _prepare_export_data(self, data: dict, config: dict) -> dict:
        """准备导出数据"""
        # 获取数据源
        source = config.get('source', 'payload')
        
        if source == 'payload':
            export_data = data.get('payload', {})
        elif source == 'enriched_payload':
            export_data = data.get('enriched_payload', data.get('payload', {}))
        elif source == 'transformed_data':
            export_data = data.get('transformed_data', data.get('payload', {}))
        elif source == 'full':
            export_data = data.copy()
        else:
            export_data = data.get(source, {})
        
        # 应用字段过滤
        if 'fields' in config:
            filtered_data = {}
            for field in config['fields']:
                if field in export_data:
                    filtered_data[field] = export_data[field]
            export_data = filtered_data
        
        # 应用字段排除
        if 'exclude_fields' in config:
            for field in config['exclude_fields']:
                export_data.pop(field, None)
        
        # 应用数据转换
        if config.get('flatten', False):
            export_data = self._flatten_dict(export_data)
        
        return export_data
    
    def _export_json(self, data: dict, config: dict) -> str:
        """导出为JSON格式"""
        indent = config.get('indent', 2)
        ensure_ascii = config.get('ensure_ascii', False)
        sort_keys = config.get('sort_keys', False)
        
        return json.dumps(data, indent=indent, ensure_ascii=ensure_ascii, 
                         sort_keys=sort_keys, default=str)
    
    def _export_csv(self, data: dict, config: dict) -> str:
        """导出为CSV格式"""
        output = StringIO()
        
        # 如果数据是字典列表
        if isinstance(data, list) and data and isinstance(data[0], dict):
            fieldnames = config.get('fieldnames', list(data[0].keys()))
            writer = csv.DictWriter(output, fieldnames=fieldnames)
            
            if config.get('include_header', True):
                writer.writeheader()
            
            for row in data:
                # 确保所有值都是字符串
                clean_row = {k: str(v) if v is not None else '' for k, v in row.items()}
                writer.writerow(clean_row)
        
        # 如果数据是单个字典
        elif isinstance(data, dict):
            # 转换为键值对列表
            rows = [{'key': k, 'value': str(v)} for k, v in data.items()]
            writer = csv.DictWriter(output, fieldnames=['key', 'value'])
            
            if config.get('include_header', True):
                writer.writeheader()
            
            writer.writerows(rows)
        
        return output.getvalue()
    
    def _export_xml(self, data: dict, config: dict) -> str:
        """导出为XML格式"""
        root_name = config.get('root_element', 'data')
        item_name = config.get('item_element', 'item')
        
        root = ET.Element(root_name)
        
        # 如果数据是列表
        if isinstance(data, list):
            for item in data:
                item_elem = ET.SubElement(root, item_name)
                self._dict_to_xml(item, item_elem)
        
        # 如果数据是字典
        elif isinstance(data, dict):
            self._dict_to_xml(data, root)
        
        # 格式化XML
        self._indent_xml(root)
        return ET.tostring(root, encoding='unicode')
    
    def _export_excel(self, data: dict, config: dict) -> str:
        """导出为Excel格式（简化版，返回TSV）"""
        # 在真实应用中，这里应该使用openpyxl或xlswriter
        # 这里返回制表符分隔的值作为简化实现
        output = StringIO()
        
        if isinstance(data, list) and data and isinstance(data[0], dict):
            # 写入标题行
            fieldnames = config.get('fieldnames', list(data[0].keys()))
            output.write('\t'.join(fieldnames) + '\n')
            
            # 写入数据行
            for row in data:
                values = [str(row.get(field, '')) for field in fieldnames]
                output.write('\t'.join(values) + '\n')
        
        elif isinstance(data, dict):
            output.write('Key\tValue\n')
            for k, v in data.items():
                output.write(f'{k}\t{str(v)}\n')
        
        return output.getvalue()
    
    def _export_txt(self, data: dict, config: dict) -> str:
        """导出为文本格式"""
        template = config.get('template')
        
        if template:
            # 使用模板格式化
            return self._format_with_template(data, template)
        else:
            # 默认格式化
            return self._format_as_text(data, config)
    
    def _export_yaml(self, data: dict, config: dict) -> str:
        """导出为YAML格式（简化版）"""
        # 简化的YAML实现
        return self._dict_to_yaml(data, 0)
    
    def _dict_to_xml(self, data: dict, parent: ET.Element):
        """将字典转换为XML元素"""
        if isinstance(data, dict):
            for key, value in data.items():
                # 清理键名（XML标签名不能包含特殊字符）
                clean_key = self._clean_xml_tag(key)
                child = ET.SubElement(parent, clean_key)
                
                if isinstance(value, (dict, list)):
                    self._dict_to_xml(value, child)
                else:
                    child.text = str(value)
        
        elif isinstance(data, list):
            for item in data:
                item_elem = ET.SubElement(parent, 'item')
                self._dict_to_xml(item, item_elem)
    
    def _clean_xml_tag(self, tag: str) -> str:
        """清理XML标签名"""
        # 移除特殊字符，替换为下划线
        import re
        clean_tag = re.sub(r'[^a-zA-Z0-9_]', '_', str(tag))
        # 确保以字母开头
        if clean_tag and not clean_tag[0].isalpha():
            clean_tag = 'field_' + clean_tag
        return clean_tag or 'field'
    
    def _indent_xml(self, elem: ET.Element, level: int = 0):
        """格式化XML缩进"""
        i = "\n" + level * "  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for child in elem:
                self._indent_xml(child, level + 1)
            if not child.tail or not child.tail.strip():
                child.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i
    
    def _format_with_template(self, data: dict, template: str) -> str:
        """使用模板格式化数据"""
        try:
            return template.format(**data)
        except KeyError as e:
            return f"Template error: Missing key {e}"
    
    def _format_as_text(self, data: dict, config: dict) -> str:
        """格式化为文本"""
        lines = []
        separator = config.get('separator', ': ')
        line_ending = config.get('line_ending', '\n')
        
        def format_value(value, indent=0):
            prefix = '  ' * indent
            if isinstance(value, dict):
                result = []
                for k, v in value.items():
                    if isinstance(v, (dict, list)):
                        result.append(f"{prefix}{k}:")
                        result.append(format_value(v, indent + 1))
                    else:
                        result.append(f"{prefix}{k}{separator}{v}")
                return line_ending.join(result)
            elif isinstance(value, list):
                result = []
                for i, item in enumerate(value):
                    result.append(f"{prefix}- {format_value(item, indent)}")
                return line_ending.join(result)
            else:
                return f"{prefix}{value}"
        
        return format_value(data)
    
    def _dict_to_yaml(self, data: dict, indent: int) -> str:
        """将字典转换为YAML格式（简化版）"""
        lines = []
        prefix = '  ' * indent
        
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, dict):
                    lines.append(f"{prefix}{key}:")
                    lines.append(self._dict_to_yaml(value, indent + 1))
                elif isinstance(value, list):
                    lines.append(f"{prefix}{key}:")
                    for item in value:
                        if isinstance(item, dict):
                            lines.append(f"{prefix}- ")
                            lines.append(self._dict_to_yaml(item, indent + 1))
                        else:
                            lines.append(f"{prefix}- {item}")
                else:
                    lines.append(f"{prefix}{key}: {value}")
        
        return '\n'.join(lines)
    
    def _flatten_dict(self, data: dict, parent_key: str = '', sep: str = '.') -> dict:
        """扁平化嵌套字典"""
        items = []
        
        for k, v in data.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            
            if isinstance(v, dict):
                items.extend(self._flatten_dict(v, new_key, sep).items())
            elif isinstance(v, list):
                for i, item in enumerate(v):
                    if isinstance(item, dict):
                        items.extend(self._flatten_dict(item, f"{new_key}[{i}]", sep).items())
                    else:
                        items.append((f"{new_key}[{i}]", item))
            else:
                items.append((new_key, v))
        
        return dict(items)
    
    def _count_records(self, data: dict) -> int:
        """计算记录数量"""
        if isinstance(data, list):
            return len(data)
        elif isinstance(data, dict):
            # 如果字典包含列表，计算列表项数量
            max_count = 0
            for value in data.values():
                if isinstance(value, list):
                    max_count = max(max_count, len(value))
            return max_count or 1  # 至少1条记录
        else:
            return 1
    
    def _save_to_file(self, content: str, filename: str):
        """保存到文件（模拟）"""
        # 在实际应用中，这里会真正保存文件
        # 这里只是模拟保存过程
        print(f"模拟保存文件: {filename}, 大小: {len(content)} 字符")


class ReportExportHandler(BaseHandler):
    """报告导出处理器"""
    
    def __init__(self):
        super().__init__("ReportExportHandler")
        self._report_templates = {
            'summary': self._generate_summary_report,
            'detailed': self._generate_detailed_report,
            'analytics': self._generate_analytics_report,
            'comparison': self._generate_comparison_report
        }
    
    def can_handle(self, request: ProcessingRequest) -> bool:
        return (request.request_type == RequestType.DATA_EXPORT and 
                request.data.get('export_config', {}).get('type') == 'report')
    
    def process(self, request: ProcessingRequest) -> ProcessingRequest:
        """生成并导出报告"""
        data = request.data
        export_config = data.get('export_config', {})
        
        # 获取报告类型
        report_type = export_config.get('report_type', 'summary')
        
        # 生成报告
        if report_type in self._report_templates:
            report_content = self._report_templates[report_type](data, export_config)
            
            # 创建报告结果
            report_result = {
                'type': report_type,
                'content': report_content,
                'generated_at': time.time(),
                'format': export_config.get('format', 'html'),
                'config': export_config
            }
            
            request.data['report_result'] = report_result
            request.add_log(self.name, f"生成 {report_type} 类型报告")
        else:
            request.add_log(self.name, f"不支持的报告类型: {report_type}")
            request.data['report_error'] = f"Unsupported report type: {report_type}"
        
        return request
    
    def _generate_summary_report(self, data: dict, config: dict) -> str:
        """生成摘要报告"""
        template = """
        <html>
        <head><title>数据处理摘要报告</title></head>
        <body>
            <h1>数据处理摘要报告</h1>
            <h2>基本信息</h2>
            <p>处理时间: {timestamp}</p>
            <p>记录数量: {record_count}</p>
            <p>处理状态: {status}</p>
            
            <h2>处理步骤</h2>
            <ul>
            {processing_steps}
            </ul>
            
            <h2>结果概览</h2>
            <pre>{result_summary}</pre>
        </body>
        </html>
        """
        
        processing_steps = ""
        if 'logs' in data:
            for log in data['logs']:
                processing_steps += f"<li>{log['handler']}: {log['message']}</li>\n"
        
        return template.format(
            timestamp=time.strftime('%Y-%m-%d %H:%M:%S'),
            record_count=self._count_data_records(data),
            status="Success",
            processing_steps=processing_steps,
            result_summary=json.dumps(data.get('payload', {}), indent=2)
        )
    
    def _generate_detailed_report(self, data: dict, config: dict) -> str:
        """生成详细报告"""
        # 详细报告实现
        return f"详细报告内容 - 生成时间: {time.strftime('%Y-%m-%d %H:%M:%S')}"
    
    def _generate_analytics_report(self, data: dict, config: dict) -> str:
        """生成分析报告"""
        # 分析报告实现
        return f"分析报告内容 - 生成时间: {time.strftime('%Y-%m-%d %H:%M:%S')}"
    
    def _generate_comparison_report(self, data: dict, config: dict) -> str:
        """生成对比报告"""
        # 对比报告实现
        return f"对比报告内容 - 生成时间: {time.strftime('%Y-%m-%d %H:%M:%S')}"
    
    def _count_data_records(self, data: dict) -> int:
        """计算数据记录数"""
        payload = data.get('payload', {})
        if isinstance(payload, list):
            return len(payload)
        elif isinstance(payload, dict):
            return 1
        else:
            return 0
