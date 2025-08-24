#!/bin/bash

echo "🧪 测试新的模块化处理器结构"
echo "============================"

cd app

# 测试新模块的导入
echo "1️⃣ 测试模块导入..."
python3 -c "
try:
    from handlers.validation_handler import DataValidationHandler
    print('   ✅ 验证处理器模块导入成功')
    
    from handlers.transformation_handler import DataTransformationHandler
    print('   ✅ 转换处理器模块导入成功')
    
    from handlers.enrichment_handler import DataEnrichmentHandler
    print('   ✅ 丰富化处理器模块导入成功')
    
    from handlers.export_handler import DataExportHandler, ReportExportHandler
    print('   ✅ 导出处理器模块导入成功')
    
    from handlers.notification_handler import NotificationHandler, AlertHandler
    print('   ✅ 通知处理器模块导入成功')
    
    from chain_handlers import ChainBuilder, ChainProcessor, RequestType
    print('   ✅ 责任链框架导入成功')
    
except ImportError as e:
    print(f'   ❌ 导入失败: {e}')
    exit(1)
"

# 测试处理器实例化
echo -e "\n2️⃣ 测试处理器实例化..."
python3 -c "
try:
    from handlers.validation_handler import DataValidationHandler
    from handlers.transformation_handler import DataTransformationHandler
    from handlers.enrichment_handler import DataEnrichmentHandler
    from handlers.export_handler import DataExportHandler, ReportExportHandler
    from handlers.notification_handler import NotificationHandler, AlertHandler
    
    # 实例化所有处理器
    handlers = [
        DataValidationHandler(),
        DataTransformationHandler(),
        DataEnrichmentHandler(),
        DataExportHandler(),
        ReportExportHandler(),
        NotificationHandler(),
        AlertHandler()
    ]
    
    print(f'   ✅ 成功实例化 {len(handlers)} 个处理器')
    
    # 检查处理器名称
    for handler in handlers:
        print(f'   - {handler.name}')
        
except Exception as e:
    print(f'   ❌ 实例化失败: {e}')
    exit(1)
"

# 测试责任链构建
echo -e "\n3️⃣ 测试责任链构建..."
python3 -c "
try:
    from chain_handlers import ChainBuilder, ChainProcessor
    from handlers.validation_handler import DataValidationHandler
    from handlers.transformation_handler import DataTransformationHandler
    from handlers.notification_handler import NotificationHandler
    
    # 构建测试链
    processor = ChainProcessor()
    
    # 构建标准链
    standard_chain = processor.build_standard_chain()
    print('   ✅ 标准处理链构建成功')
    
    # 构建验证链
    validation_chain = processor.build_validation_chain()
    print('   ✅ 验证处理链构建成功')
    
    # 构建导出链
    export_chain = processor.build_export_chain()
    print('   ✅ 导出处理链构建成功')
    
    # 构建丰富化链
    enrichment_chain = processor.build_enrichment_chain()
    print('   ✅ 丰富化处理链构建成功')
    
except Exception as e:
    print(f'   ❌ 链构建失败: {e}')
    exit(1)
"

# 测试简单的责任链执行
echo -e "\n4️⃣ 测试简单的责任链执行..."
python3 -c "
try:
    from chain_handlers import ChainBuilder, ProcessingRequest, RequestType
    from handlers.validation_handler import DataValidationHandler
    from handlers.notification_handler import NotificationHandler
    
    # 创建简单的验证链
    chain = (ChainBuilder()
            .add_handler(DataValidationHandler())
            .add_handler(NotificationHandler())
            .build())
    
    # 创建测试请求
    test_data = {
        'payload': {
            'name': 'Test User',
            'email': 'test@example.com',
            'age': 25
        }
    }
    
    request = ProcessingRequest(RequestType.DATA_VALIDATION, test_data)
    
    # 执行处理
    result = chain.handle(request)
    
    print(f'   ✅ 责任链执行成功')
    print(f'   📊 处理器数量: {len(result.processing_log)}')
    print(f'   📝 错误数量: {len(result.errors)}')
    print(f'   ⚠️ 警告数量: {len(result.warnings)}')
    
    # 显示处理日志
    for log in result.processing_log:
        print(f'   - {log[\"handler\"]}: {log[\"message\"]}')
        
except Exception as e:
    print(f'   ❌ 执行失败: {e}')
    exit(1)
"

echo -e "\n5️⃣ 检查文件结构..."
echo "   📁 handlers目录:"
ls -la app/handlers/ | grep "\.py$" | while read line; do
    echo "   - $line"
done

echo -e "\n✅ 模块化处理器结构测试完成!"
echo "🎯 重构优势:"
echo "   - 代码组织更清晰，每个处理器独立文件"
echo "   - 更好的模块化和可维护性"
echo "   - 支持单独测试每个处理器"
echo "   - 更容易扩展新的处理器类型"
echo "   - 符合单一职责原则"
