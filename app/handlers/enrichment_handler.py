"""
数据丰富化处理器
"""
import time
import random
from handlers import BaseHandler, ProcessingRequest, RequestType


class DataEnrichmentHandler(BaseHandler):
    """数据丰富化处理器"""
    
    def __init__(self):
        super().__init__("DataEnrichmentHandler")
        self._geo_database = self._init_geo_database()
        self._company_database = self._init_company_database()
    
    def can_handle(self, request: ProcessingRequest) -> bool:
        return request.request_type == RequestType.DATA_ENRICHMENT
    
    def process(self, request: ProcessingRequest) -> ProcessingRequest:
        """执行数据丰富化"""
        data = request.data
        payload = data.get('payload', {})
        
        # 创建丰富化数据副本
        enriched_data = payload.copy()
        
        # 添加基础元数据
        enriched_data['_metadata'] = self._create_metadata()
        
        # 应用各种丰富化规则
        self._enrich_personal_info(enriched_data, request)
        self._enrich_contact_info(enriched_data, request)
        self._enrich_geographic_info(enriched_data, request)
        self._enrich_demographic_info(enriched_data, request)
        self._enrich_professional_info(enriched_data, request)
        self._enrich_behavioral_info(enriched_data, request)
        
        # 保存丰富化结果
        request.data['enriched_payload'] = enriched_data
        
        # 模拟丰富化处理时间
        time.sleep(0.7)
        
        rules_count = len(enriched_data['_metadata']['enrichment_rules_applied'])
        request.add_log(self.name, f"应用了 {rules_count} 个丰富化规则")
        return request
    
    def _create_metadata(self) -> dict:
        """创建基础元数据"""
        return {
            'processed_at': time.time(),
            'processor': self.name,
            'version': '2.0',
            'enrichment_rules_applied': [],
            'confidence_scores': {},
            'data_sources': []
        }
    
    def _enrich_personal_info(self, data: dict, request):
        """丰富化个人信息"""
        metadata = data['_metadata']
        
        # 全名生成
        if 'first_name' in data and 'last_name' in data:
            data['full_name'] = f"{data['first_name']} {data['last_name']}"
            metadata['enrichment_rules_applied'].append('full_name_generation')
            metadata['confidence_scores']['full_name'] = 1.0
        
        # 姓名首字母
        if 'full_name' in data:
            parts = data['full_name'].split()
            if len(parts) >= 2:
                data['initials'] = ''.join([part[0].upper() for part in parts])
                metadata['enrichment_rules_applied'].append('initials_generation')
        
        # 年龄分类
        if 'age' in data:
            age = data['age']
            if isinstance(age, (int, float)):
                data['age_category'] = self._categorize_age(age)
                data['generation'] = self._determine_generation(age)
                metadata['enrichment_rules_applied'].extend(['age_categorization', 'generation_classification'])
        
        # 生日月份信息（如果有）
        if 'birth_date' in data:
            birth_info = self._analyze_birth_date(data['birth_date'])
            data.update(birth_info)
            metadata['enrichment_rules_applied'].append('birth_date_analysis')
    
    def _enrich_contact_info(self, data: dict, request):
        """丰富化联系信息"""
        metadata = data['_metadata']
        
        # 邮箱域名分析
        if 'email' in data:
            email = str(data['email'])
            if '@' in email:
                domain = email.split('@')[1].lower()
                data['email_domain'] = domain
                data['email_provider'] = self._classify_email_provider(domain)
                data['is_business_email'] = self._is_business_email(domain)
                metadata['enrichment_rules_applied'].extend([
                    'email_domain_extraction', 
                    'email_provider_classification',
                    'business_email_detection'
                ])
        
        # 电话号码分析
        if 'phone' in data:
            phone_info = self._analyze_phone_number(str(data['phone']))
            data.update(phone_info)
            metadata['enrichment_rules_applied'].append('phone_analysis')
    
    def _enrich_geographic_info(self, data: dict, request):
        """丰富化地理信息"""
        metadata = data['_metadata']
        
        # 国家信息丰富化
        if 'country' in data:
            country = data['country']
            if country in self._geo_database:
                geo_info = self._geo_database[country]
                data['geo_info'] = geo_info.copy()
                data['continent'] = geo_info['continent']
                data['timezone'] = geo_info['timezone']
                data['currency'] = geo_info['currency']
                data['country_code'] = geo_info['country_code']
                metadata['enrichment_rules_applied'].append('geo_enrichment')
                metadata['data_sources'].append('internal_geo_database')
        
        # 城市信息（模拟）
        if 'city' in data:
            city_info = self._get_city_info(data['city'], data.get('country'))
            if city_info:
                data['city_info'] = city_info
                metadata['enrichment_rules_applied'].append('city_enrichment')
        
        # 邮政编码分析
        if 'postal_code' in data:
            postal_info = self._analyze_postal_code(data['postal_code'], data.get('country'))
            if postal_info:
                data['postal_info'] = postal_info
                metadata['enrichment_rules_applied'].append('postal_code_analysis')
    
    def _enrich_demographic_info(self, data: dict, request):
        """丰富化人口统计信息"""
        metadata = data['_metadata']
        
        # 性别推断（基于名字，仅作演示）
        if 'first_name' in data and 'gender' not in data:
            gender_guess = self._guess_gender(data['first_name'])
            if gender_guess:
                data['predicted_gender'] = gender_guess
                metadata['enrichment_rules_applied'].append('gender_prediction')
                metadata['confidence_scores']['predicted_gender'] = 0.7  # 中等信心度
        
        # 收入等级估算（基于职业和年龄）
        if 'job_title' in data and 'age' in data:
            income_estimate = self._estimate_income(data['job_title'], data['age'])
            if income_estimate:
                data['estimated_income_range'] = income_estimate
                metadata['enrichment_rules_applied'].append('income_estimation')
                metadata['confidence_scores']['estimated_income_range'] = 0.6
    
    def _enrich_professional_info(self, data: dict, request):
        """丰富化职业信息"""
        metadata = data['_metadata']
        
        # 职业分类
        if 'job_title' in data:
            job_info = self._classify_job(data['job_title'])
            data.update(job_info)
            metadata['enrichment_rules_applied'].append('job_classification')
        
        # 公司信息
        if 'company' in data:
            company_info = self._get_company_info(data['company'])
            if company_info:
                data['company_info'] = company_info
                metadata['enrichment_rules_applied'].append('company_enrichment')
                metadata['data_sources'].append('company_database')
        
        # 行业经验估算
        if 'job_title' in data and 'age' in data:
            experience = self._estimate_experience(data['job_title'], data['age'])
            if experience:
                data['estimated_experience_years'] = experience
                metadata['enrichment_rules_applied'].append('experience_estimation')
    
    def _enrich_behavioral_info(self, data: dict, request):
        """丰富化行为信息"""
        metadata = data['_metadata']
        
        # 活跃时间段预测（基于时区）
        if 'timezone' in data:
            active_hours = self._predict_active_hours(data['timezone'])
            data['predicted_active_hours'] = active_hours
            metadata['enrichment_rules_applied'].append('active_hours_prediction')
        
        # 偏好预测（基于年龄和职业）
        if 'age' in data and 'job_title' in data:
            preferences = self._predict_preferences(data['age'], data['job_title'])
            data['predicted_preferences'] = preferences
            metadata['enrichment_rules_applied'].append('preference_prediction')
    
    def _categorize_age(self, age: int) -> str:
        """年龄分类"""
        if age < 13:
            return 'child'
        elif age < 20:
            return 'teenager'
        elif age < 35:
            return 'young_adult'
        elif age < 55:
            return 'middle_aged'
        elif age < 65:
            return 'senior'
        else:
            return 'elderly'
    
    def _determine_generation(self, age: int) -> str:
        """确定世代"""
        current_year = 2025
        birth_year = current_year - age
        
        if birth_year >= 2010:
            return 'Gen Alpha'
        elif birth_year >= 1997:
            return 'Gen Z'
        elif birth_year >= 1981:
            return 'Millennial'
        elif birth_year >= 1965:
            return 'Gen X'
        elif birth_year >= 1946:
            return 'Baby Boomer'
        else:
            return 'Silent Generation'
    
    def _classify_email_provider(self, domain: str) -> str:
        """分类邮箱提供商"""
        providers = {
            'gmail.com': 'Google',
            'yahoo.com': 'Yahoo',
            'outlook.com': 'Microsoft',
            'hotmail.com': 'Microsoft',
            'icloud.com': 'Apple',
            'qq.com': 'Tencent',
            '163.com': 'NetEase',
            'sina.com': 'Sina'
        }
        return providers.get(domain, 'Other')
    
    def _is_business_email(self, domain: str) -> bool:
        """判断是否为商务邮箱"""
        personal_domains = {
            'gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com',
            'icloud.com', 'qq.com', '163.com', 'sina.com'
        }
        return domain not in personal_domains
    
    def _analyze_phone_number(self, phone: str) -> dict:
        """分析电话号码"""
        result = {}
        
        # 提取数字
        digits = ''.join(filter(str.isdigit, phone))
        
        if len(digits) == 10:
            result['phone_country'] = 'US'
            result['phone_type'] = 'mobile' if digits[0] in '3456789' else 'landline'
        elif len(digits) == 11 and digits.startswith('1'):
            result['phone_country'] = 'US'
            result['phone_type'] = 'mobile'
        elif len(digits) == 11 and digits.startswith('86'):
            result['phone_country'] = 'China'
            result['phone_type'] = 'mobile' if digits[2] == '1' else 'landline'
        
        return result
    
    def _get_city_info(self, city: str, country: str = None) -> dict:
        """获取城市信息（模拟）"""
        # 这里应该连接真实的城市数据库
        mock_cities = {
            'New York': {'population': 8400000, 'area_km2': 783},
            'Beijing': {'population': 21540000, 'area_km2': 16411},
            'London': {'population': 8982000, 'area_km2': 1572},
            'Tokyo': {'population': 13960000, 'area_km2': 2194}
        }
        return mock_cities.get(city)
    
    def _analyze_postal_code(self, postal_code: str, country: str = None) -> dict:
        """分析邮政编码"""
        result = {}
        
        if country == 'US':
            if len(postal_code) == 5:
                result['postal_type'] = 'ZIP'
                result['region'] = 'US-' + postal_code[:2]
        elif country == 'China':
            if len(postal_code) == 6:
                result['postal_type'] = 'China Postal'
                result['province_code'] = postal_code[:2]
        
        return result
    
    def _guess_gender(self, first_name: str) -> str:
        """基于名字猜测性别（仅作演示）"""
        # 这是一个非常简化的示例，实际应用中需要更复杂的算法
        male_names = {'john', 'mike', 'david', 'james', 'robert', 'wang', 'li'}
        female_names = {'mary', 'susan', 'lisa', 'jennifer', 'maria', 'lily', 'alice'}
        
        name_lower = first_name.lower()
        if name_lower in male_names:
            return 'male'
        elif name_lower in female_names:
            return 'female'
        else:
            return None
    
    def _classify_job(self, job_title: str) -> dict:
        """职业分类"""
        job_lower = job_title.lower()
        
        if any(keyword in job_lower for keyword in ['engineer', 'developer', 'programmer']):
            return {
                'job_category': 'Technology',
                'job_level': 'professional',
                'skills_required': ['programming', 'problem_solving']
            }
        elif any(keyword in job_lower for keyword in ['manager', 'director', 'executive']):
            return {
                'job_category': 'Management',
                'job_level': 'leadership',
                'skills_required': ['leadership', 'communication']
            }
        elif any(keyword in job_lower for keyword in ['sales', 'marketing']):
            return {
                'job_category': 'Sales & Marketing',
                'job_level': 'professional',
                'skills_required': ['communication', 'persuasion']
            }
        else:
            return {
                'job_category': 'Other',
                'job_level': 'professional',
                'skills_required': ['general']
            }
    
    def _get_company_info(self, company: str) -> dict:
        """获取公司信息"""
        return self._company_database.get(company)
    
    def _estimate_income(self, job_title: str, age: int) -> str:
        """估算收入范围"""
        job_info = self._classify_job(job_title)
        category = job_info['job_category']
        
        base_ranges = {
            'Technology': (60000, 150000),
            'Management': (80000, 200000),
            'Sales & Marketing': (40000, 120000),
            'Other': (30000, 80000)
        }
        
        if category in base_ranges:
            low, high = base_ranges[category]
            # 根据年龄调整
            age_factor = min(1.5, 1 + (age - 25) * 0.02)
            return f"${int(low * age_factor):,} - ${int(high * age_factor):,}"
        
        return None
    
    def _estimate_experience(self, job_title: str, age: int) -> int:
        """估算工作经验年数"""
        # 假设22岁开始工作
        max_experience = max(0, age - 22)
        
        # 根据职位类型调整
        job_info = self._classify_job(job_title)
        if job_info['job_level'] == 'leadership':
            return min(max_experience, max(5, max_experience - 5))
        else:
            return max_experience
    
    def _predict_active_hours(self, timezone: str) -> dict:
        """预测活跃时间"""
        # 基于时区的活跃时间预测
        return {
            'morning': '8:00-10:00',
            'afternoon': '14:00-16:00',
            'evening': '19:00-21:00',
            'timezone': timezone
        }
    
    def _predict_preferences(self, age: int, job_title: str) -> dict:
        """预测偏好"""
        preferences = {}
        
        # 年龄相关偏好
        if age < 30:
            preferences['communication'] = ['social_media', 'messaging']
            preferences['shopping'] = ['online', 'mobile']
        else:
            preferences['communication'] = ['email', 'phone']
            preferences['shopping'] = ['online', 'in_store']
        
        # 职业相关偏好
        job_info = self._classify_job(job_title)
        if job_info['job_category'] == 'Technology':
            preferences['content'] = ['tech_news', 'tutorials']
        elif job_info['job_category'] == 'Management':
            preferences['content'] = ['business_news', 'leadership']
        
        return preferences
    
    def _analyze_birth_date(self, birth_date: str) -> dict:
        """分析生日信息"""
        try:
            from datetime import datetime
            date_obj = datetime.strptime(birth_date, '%Y-%m-%d')
            
            return {
                'birth_month': date_obj.month,
                'birth_day': date_obj.day,
                'zodiac_sign': self._get_zodiac_sign(date_obj.month, date_obj.day),
                'birth_season': self._get_season(date_obj.month)
            }
        except:
            return {}
    
    def _get_zodiac_sign(self, month: int, day: int) -> str:
        """获取星座"""
        zodiac_dates = [
            (1, 20, "Capricorn"), (2, 19, "Aquarius"), (3, 21, "Pisces"),
            (4, 20, "Aries"), (5, 21, "Taurus"), (6, 21, "Gemini"),
            (7, 23, "Cancer"), (8, 23, "Leo"), (9, 23, "Virgo"),
            (10, 23, "Libra"), (11, 22, "Scorpio"), (12, 22, "Sagittarius")
        ]
        
        for i, (end_month, end_day, sign) in enumerate(zodiac_dates):
            if month < end_month or (month == end_month and day <= end_day):
                return sign
        return "Capricorn"
    
    def _get_season(self, month: int) -> str:
        """获取季节"""
        if month in [12, 1, 2]:
            return "Winter"
        elif month in [3, 4, 5]:
            return "Spring"
        elif month in [6, 7, 8]:
            return "Summer"
        else:
            return "Fall"
    
    def _init_geo_database(self) -> dict:
        """初始化地理数据库"""
        return {
            'USA': {
                'continent': 'North America',
                'timezone': 'UTC-5',
                'currency': 'USD',
                'country_code': 'US',
                'language': 'English'
            },
            'China': {
                'continent': 'Asia',
                'timezone': 'UTC+8',
                'currency': 'CNY',
                'country_code': 'CN',
                'language': 'Chinese'
            },
            'Germany': {
                'continent': 'Europe',
                'timezone': 'UTC+1',
                'currency': 'EUR',
                'country_code': 'DE',
                'language': 'German'
            },
            'Japan': {
                'continent': 'Asia',
                'timezone': 'UTC+9',
                'currency': 'JPY',
                'country_code': 'JP',
                'language': 'Japanese'
            },
            'United Kingdom': {
                'continent': 'Europe',
                'timezone': 'UTC+0',
                'currency': 'GBP',
                'country_code': 'GB',
                'language': 'English'
            }
        }
    
    def _init_company_database(self) -> dict:
        """初始化公司数据库"""
        return {
            'Google': {
                'industry': 'Technology',
                'size': 'Large',
                'founded': 1998,
                'headquarters': 'Mountain View, CA'
            },
            'Microsoft': {
                'industry': 'Technology',
                'size': 'Large',
                'founded': 1975,
                'headquarters': 'Redmond, WA'
            },
            'Apple': {
                'industry': 'Technology',
                'size': 'Large',
                'founded': 1976,
                'headquarters': 'Cupertino, CA'
            }
        }
