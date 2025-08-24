"""
通知处理器
"""
import time
import json
import random
from datetime import datetime, timedelta
from handlers import BaseHandler, ProcessingRequest, RequestType


class NotificationHandler(BaseHandler):
    """通知处理器"""
    
    def __init__(self):
        super().__init__("NotificationHandler")
        self._notification_channels = {
            'email': self._send_email,
            'sms': self._send_sms,
            'webhook': self._send_webhook,
            'slack': self._send_slack,
            'discord': self._send_discord,
            'teams': self._send_teams,
            'push': self._send_push_notification
        }
        self._templates = {
            'success': self._get_success_template,
            'error': self._get_error_template,
            'warning': self._get_warning_template,
            'info': self._get_info_template
        }
    
    def can_handle(self, request: ProcessingRequest) -> bool:
        return request.request_type == RequestType.NOTIFICATION
    
    def process(self, request: ProcessingRequest) -> ProcessingRequest:
        """执行通知发送"""
        data = request.data
        notification_config = data.get('notification_config', {})
        
        # 获取通知类型和渠道
        notification_type = notification_config.get('type', 'info')
        channels = notification_config.get('channels', ['email'])
        
        # 确保channels是列表
        if isinstance(channels, str):
            channels = [channels]
        
        # 准备通知内容
        notification_content = self._prepare_notification_content(data, notification_config)
        
        # 发送结果
        send_results = []
        
        # 逐个渠道发送通知
        for channel in channels:
            if channel in self._notification_channels:
                try:
                    result = self._notification_channels[channel](notification_content, notification_config)
                    send_results.append({
                        'channel': channel,
                        'status': 'success',
                        'result': result,
                        'sent_at': time.time()
                    })
                    request.add_log(self.name, f"通过 {channel} 渠道发送通知成功")
                except Exception as e:
                    send_results.append({
                        'channel': channel,
                        'status': 'failed',
                        'error': str(e),
                        'sent_at': time.time()
                    })
                    request.add_log(self.name, f"通过 {channel} 渠道发送通知失败: {str(e)}")
            else:
                send_results.append({
                    'channel': channel,
                    'status': 'failed',
                    'error': f"Unsupported channel: {channel}",
                    'sent_at': time.time()
                })
                request.add_log(self.name, f"不支持的通知渠道: {channel}")
        
        # 保存通知结果
        notification_result = {
            'type': notification_type,
            'channels': channels,
            'results': send_results,
            'success_count': len([r for r in send_results if r['status'] == 'success']),
            'failed_count': len([r for r in send_results if r['status'] == 'failed']),
            'content': notification_content,
            'config': notification_config
        }
        
        request.data['notification_result'] = notification_result
        
        # 模拟通知处理时间
        time.sleep(0.3)
        
        return request
    
    def _prepare_notification_content(self, data: dict, config: dict) -> dict:
        """准备通知内容"""
        notification_type = config.get('type', 'info')
        
        # 获取模板
        template = None
        if notification_type in self._templates:
            template = self._templates[notification_type](data, config)
        
        # 如果有自定义模板
        custom_template = config.get('template')
        if custom_template:
            template = custom_template
        
        # 准备模板变量
        template_vars = self._prepare_template_variables(data, config)
        
        # 渲染内容
        content = {
            'subject': self._render_template(template.get('subject', ''), template_vars),
            'body': self._render_template(template.get('body', ''), template_vars),
            'html_body': self._render_template(template.get('html_body', ''), template_vars),
            'variables': template_vars,
            'priority': config.get('priority', 'normal'),
            'timestamp': datetime.now().isoformat()
        }
        
        return content
    
    def _prepare_template_variables(self, data: dict, config: dict) -> dict:
        """准备模板变量"""
        variables = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'task_id': data.get('task_id', 'unknown'),
            'status': 'success' if not data.get('error') else 'failed',
            'processing_time': data.get('processing_time', 0),
        }
        
        # 添加处理日志信息
        if 'logs' in data:
            variables['log_count'] = len(data['logs'])
            variables['last_log'] = data['logs'][-1] if data['logs'] else None
            variables['handlers_used'] = [log['handler'] for log in data['logs']]
        
        # 添加数据信息
        payload = data.get('payload', {})
        if isinstance(payload, dict):
            variables['record_count'] = 1
            variables['data_keys'] = list(payload.keys())
        elif isinstance(payload, list):
            variables['record_count'] = len(payload)
            variables['data_keys'] = list(payload[0].keys()) if payload else []
        
        # 添加错误信息
        if 'error' in data:
            variables['error_message'] = data['error']
            variables['error_type'] = type(data['error']).__name__
        
        # 添加自定义变量
        custom_vars = config.get('variables', {})
        variables.update(custom_vars)
        
        return variables
    
    def _render_template(self, template: str, variables: dict) -> str:
        """渲染模板"""
        try:
            return template.format(**variables)
        except KeyError as e:
            return f"Template error: Missing variable {e}"
        except Exception as e:
            return f"Template error: {str(e)}"
    
    def _send_email(self, content: dict, config: dict) -> dict:
        """发送邮件通知"""
        # 模拟邮件发送
        recipients = config.get('recipients', ['admin@example.com'])
        sender = config.get('sender', 'noreply@example.com')
        
        # 模拟发送延迟
        time.sleep(random.uniform(0.1, 0.3))
        
        # 模拟发送结果
        message_id = f"email_{int(time.time())}_{random.randint(1000, 9999)}"
        
        return {
            'message_id': message_id,
            'recipients': recipients,
            'sender': sender,
            'subject': content['subject'],
            'delivery_status': 'sent',
            'delivery_time': datetime.now().isoformat()
        }
    
    def _send_sms(self, content: dict, config: dict) -> dict:
        """发送短信通知"""
        # 模拟短信发送
        phone_numbers = config.get('phone_numbers', ['+1234567890'])
        
        # 短信内容通常较短
        sms_body = content['body'][:160]  # SMS通常限制在160字符
        
        time.sleep(random.uniform(0.05, 0.15))
        
        message_id = f"sms_{int(time.time())}_{random.randint(1000, 9999)}"
        
        return {
            'message_id': message_id,
            'recipients': phone_numbers,
            'body': sms_body,
            'delivery_status': 'sent',
            'delivery_time': datetime.now().isoformat(),
            'character_count': len(sms_body)
        }
    
    def _send_webhook(self, content: dict, config: dict) -> dict:
        """发送Webhook通知"""
        # 模拟Webhook发送
        webhook_url = config.get('webhook_url', 'https://example.com/webhook')
        
        payload = {
            'notification': content,
            'timestamp': datetime.now().isoformat(),
            'source': 'celery_task_system'
        }
        
        time.sleep(random.uniform(0.1, 0.2))
        
        # 模拟HTTP响应
        response_code = random.choice([200, 200, 200, 201, 400, 500])  # 大部分成功
        
        return {
            'webhook_url': webhook_url,
            'payload': payload,
            'response_code': response_code,
            'response_time_ms': random.randint(100, 500),
            'delivery_status': 'success' if response_code < 400 else 'failed',
            'delivery_time': datetime.now().isoformat()
        }
    
    def _send_slack(self, content: dict, config: dict) -> dict:
        """发送Slack通知"""
        # 模拟Slack消息发送
        channel = config.get('slack_channel', '#general')
        username = config.get('slack_username', 'TaskBot')
        
        # 格式化Slack消息
        slack_message = {
            'channel': channel,
            'username': username,
            'text': content['subject'],
            'attachments': [{
                'color': self._get_slack_color(config.get('type', 'info')),
                'fields': [
                    {'title': 'Message', 'value': content['body'], 'short': False},
                    {'title': 'Timestamp', 'value': content['timestamp'], 'short': True}
                ]
            }]
        }
        
        time.sleep(random.uniform(0.1, 0.3))
        
        return {
            'channel': channel,
            'message': slack_message,
            'delivery_status': 'sent',
            'delivery_time': datetime.now().isoformat(),
            'ts': str(time.time())
        }
    
    def _send_discord(self, content: dict, config: dict) -> dict:
        """发送Discord通知"""
        # 模拟Discord消息发送
        channel_id = config.get('discord_channel_id', '123456789')
        bot_token = config.get('discord_bot_token', 'bot_token')
        
        # Discord embed格式
        embed = {
            'title': content['subject'],
            'description': content['body'],
            'color': self._get_discord_color(config.get('type', 'info')),
            'timestamp': content['timestamp'],
            'footer': {'text': 'Celery Task System'}
        }
        
        time.sleep(random.uniform(0.1, 0.25))
        
        return {
            'channel_id': channel_id,
            'embed': embed,
            'delivery_status': 'sent',
            'delivery_time': datetime.now().isoformat(),
            'message_id': f"discord_{int(time.time())}"
        }
    
    def _send_teams(self, content: dict, config: dict) -> dict:
        """发送Microsoft Teams通知"""
        # 模拟Teams消息发送
        webhook_url = config.get('teams_webhook_url', 'https://outlook.office.com/webhook/...')
        
        # Teams Adaptive Card格式
        card = {
            '@type': 'MessageCard',
            '@context': 'http://schema.org/extensions',
            'themeColor': self._get_teams_color(config.get('type', 'info')),
            'summary': content['subject'],
            'sections': [{
                'activityTitle': content['subject'],
                'activitySubtitle': content['timestamp'],
                'text': content['body'],
                'facts': [
                    {'name': 'Priority', 'value': content['priority']},
                    {'name': 'Timestamp', 'value': content['timestamp']}
                ]
            }]
        }
        
        time.sleep(random.uniform(0.1, 0.3))
        
        return {
            'webhook_url': webhook_url,
            'card': card,
            'delivery_status': 'sent',
            'delivery_time': datetime.now().isoformat()
        }
    
    def _send_push_notification(self, content: dict, config: dict) -> dict:
        """发送推送通知"""
        # 模拟推送通知发送
        device_tokens = config.get('device_tokens', ['token1', 'token2'])
        
        push_payload = {
            'title': content['subject'],
            'body': content['body'][:100],  # 推送通知通常有长度限制
            'badge': 1,
            'sound': 'default',
            'data': {
                'timestamp': content['timestamp'],
                'priority': content['priority']
            }
        }
        
        time.sleep(random.uniform(0.05, 0.15))
        
        return {
            'device_tokens': device_tokens,
            'payload': push_payload,
            'delivery_status': 'sent',
            'delivery_time': datetime.now().isoformat(),
            'push_id': f"push_{int(time.time())}"
        }
    
    def _get_success_template(self, data: dict, config: dict) -> dict:
        """获取成功通知模板"""
        return {
            'subject': '✅ 任务处理成功 - {task_id}',
            'body': '任务 {task_id} 已成功完成处理。\n\n处理时间: {timestamp}\n记录数量: {record_count}\n使用处理器: {handlers_used}',
            'html_body': '''
            <html>
            <body>
                <h2 style="color: green;">✅ 任务处理成功</h2>
                <p><strong>任务ID:</strong> {task_id}</p>
                <p><strong>处理时间:</strong> {timestamp}</p>
                <p><strong>记录数量:</strong> {record_count}</p>
                <p><strong>使用处理器:</strong> {handlers_used}</p>
                <p style="color: green;">任务已成功完成所有处理步骤。</p>
            </body>
            </html>
            '''
        }
    
    def _get_error_template(self, data: dict, config: dict) -> dict:
        """获取错误通知模板"""
        return {
            'subject': '❌ 任务处理失败 - {task_id}',
            'body': '任务 {task_id} 处理失败。\n\n错误信息: {error_message}\n错误类型: {error_type}\n发生时间: {timestamp}',
            'html_body': '''
            <html>
            <body>
                <h2 style="color: red;">❌ 任务处理失败</h2>
                <p><strong>任务ID:</strong> {task_id}</p>
                <p><strong>发生时间:</strong> {timestamp}</p>
                <p><strong>错误信息:</strong> <span style="color: red;">{error_message}</span></p>
                <p><strong>错误类型:</strong> {error_type}</p>
                <p>请检查任务配置和输入数据。</p>
            </body>
            </html>
            '''
        }
    
    def _get_warning_template(self, data: dict, config: dict) -> dict:
        """获取警告通知模板"""
        return {
            'subject': '⚠️ 任务处理警告 - {task_id}',
            'body': '任务 {task_id} 处理完成，但有警告。\n\n处理时间: {timestamp}\n记录数量: {record_count}\n请检查处理日志。',
            'html_body': '''
            <html>
            <body>
                <h2 style="color: orange;">⚠️ 任务处理警告</h2>
                <p><strong>任务ID:</strong> {task_id}</p>
                <p><strong>处理时间:</strong> {timestamp}</p>
                <p><strong>记录数量:</strong> {record_count}</p>
                <p style="color: orange;">任务完成，但有部分警告，请检查处理日志。</p>
            </body>
            </html>
            '''
        }
    
    def _get_info_template(self, data: dict, config: dict) -> dict:
        """获取信息通知模板"""
        return {
            'subject': 'ℹ️ 任务处理信息 - {task_id}',
            'body': '任务 {task_id} 状态更新。\n\n处理时间: {timestamp}\n当前状态: {status}\n记录数量: {record_count}',
            'html_body': '''
            <html>
            <body>
                <h2 style="color: blue;">ℹ️ 任务处理信息</h2>
                <p><strong>任务ID:</strong> {task_id}</p>
                <p><strong>处理时间:</strong> {timestamp}</p>
                <p><strong>当前状态:</strong> {status}</p>
                <p><strong>记录数量:</strong> {record_count}</p>
                <p>这是一条信息通知。</p>
            </body>
            </html>
            '''
        }
    
    def _get_slack_color(self, notification_type: str) -> str:
        """获取Slack消息颜色"""
        colors = {
            'success': 'good',
            'error': 'danger',
            'warning': 'warning',
            'info': '#36a64f'
        }
        return colors.get(notification_type, '#36a64f')
    
    def _get_discord_color(self, notification_type: str) -> int:
        """获取Discord embed颜色"""
        colors = {
            'success': 0x00ff00,  # 绿色
            'error': 0xff0000,    # 红色
            'warning': 0xffa500,  # 橙色
            'info': 0x0099ff      # 蓝色
        }
        return colors.get(notification_type, 0x0099ff)
    
    def _get_teams_color(self, notification_type: str) -> str:
        """获取Teams消息颜色"""
        colors = {
            'success': '00FF00',
            'error': 'FF0000',
            'warning': 'FFA500',
            'info': '0099FF'
        }
        return colors.get(notification_type, '0099FF')


class AlertHandler(BaseHandler):
    """告警处理器"""
    
    def __init__(self):
        super().__init__("AlertHandler")
        self._alert_rules = [
            {'condition': 'error_rate > 0.1', 'severity': 'high', 'action': 'immediate'},
            {'condition': 'processing_time > 300', 'severity': 'medium', 'action': 'delayed'},
            {'condition': 'memory_usage > 0.8', 'severity': 'medium', 'action': 'delayed'},
            {'condition': 'queue_size > 1000', 'severity': 'low', 'action': 'scheduled'}
        ]
    
    def can_handle(self, request: ProcessingRequest) -> bool:
        return (request.request_type == RequestType.NOTIFICATION and 
                request.data.get('notification_config', {}).get('type') == 'alert')
    
    def process(self, request: ProcessingRequest) -> ProcessingRequest:
        """处理告警"""
        data = request.data
        
        # 评估告警条件
        alerts = self._evaluate_alert_conditions(data)
        
        if alerts:
            # 处理告警
            for alert in alerts:
                self._process_alert(alert, data, request)
            
            request.data['alerts'] = alerts
            request.add_log(self.name, f"触发 {len(alerts)} 个告警")
        else:
            request.add_log(self.name, "未触发任何告警")
        
        return request
    
    def _evaluate_alert_conditions(self, data: dict) -> list:
        """评估告警条件"""
        alerts = []
        
        # 模拟一些指标
        metrics = {
            'error_rate': random.uniform(0, 0.2),
            'processing_time': random.uniform(10, 400),
            'memory_usage': random.uniform(0.3, 0.9),
            'queue_size': random.randint(10, 1500)
        }
        
        # 检查每个告警规则
        for rule in self._alert_rules:
            condition = rule['condition']
            
            # 简单的条件评估（实际应用中需要更复杂的表达式解析）
            if self._evaluate_condition(condition, metrics):
                alert = {
                    'rule': rule,
                    'condition': condition,
                    'severity': rule['severity'],
                    'action': rule['action'],
                    'metrics': metrics.copy(),
                    'triggered_at': time.time()
                }
                alerts.append(alert)
        
        return alerts
    
    def _evaluate_condition(self, condition: str, metrics: dict) -> bool:
        """评估告警条件（简化版）"""
        # 这是一个简化的条件评估器
        for metric, value in metrics.items():
            condition = condition.replace(metric, str(value))
        
        try:
            return eval(condition)
        except:
            return False
    
    def _process_alert(self, alert: dict, data: dict, request: ProcessingRequest):
        """处理单个告警"""
        severity = alert['severity']
        action = alert['action']
        
        # 根据严重程度和动作类型处理告警
        if action == 'immediate':
            # 立即发送告警
            self._send_immediate_alert(alert, data)
        elif action == 'delayed':
            # 延迟发送告警
            self._schedule_delayed_alert(alert, data)
        elif action == 'scheduled':
            # 定期汇总告警
            self._add_to_scheduled_alerts(alert, data)
    
    def _send_immediate_alert(self, alert: dict, data: dict):
        """发送即时告警"""
        # 实际应用中会立即发送告警通知
        print(f"即时告警: {alert['condition']} - 严重程度: {alert['severity']}")
    
    def _schedule_delayed_alert(self, alert: dict, data: dict):
        """安排延迟告警"""
        # 实际应用中会安排延迟发送
        print(f"延迟告警: {alert['condition']} - 将在5分钟后发送")
    
    def _add_to_scheduled_alerts(self, alert: dict, data: dict):
        """添加到定期告警"""
        # 实际应用中会添加到定期汇总列表
        print(f"定期告警: {alert['condition']} - 将在下次汇总中发送")
