from abc import ABC, abstractmethod
import xml.etree.ElementTree as ET

# 现有系统接口
class LegacyDataService:
    """遗留系统 - 只返回XML格式数据"""
    def get_user_data_xml(self) -> str:
        return '''<user>
    <id>123</id>
    <name>张三</name>
    <email>zhangsan@example.com</email>
</user>'''

# 新系统期望的接口
class ModernSystem(ABC):
    """现代系统 - 期望JSON格式数据"""
    @abstractmethod
    def get_user_data_json(self) -> dict:
        pass

# 适配器：让旧系统适配新接口
class XMLToJSONAdapter(ModernSystem):
    def __init__(self, legacy_service: LegacyDataService):
        self.legacy_service = legacy_service
    
    def get_user_data_json(self) -> dict:
        # 获取XML数据
        xml_data = self.legacy_service.get_user_data_xml()
        
        # 解析XML并转换为JSON
        root = ET.fromstring(xml_data)
        user_data = {child.tag: child.text for child in root}
        
        return user_data

# Pythonic的适配器：使用函数和字典
def create_modern_adapter(legacy_service):
    """更Pythonic的适配器工厂"""
    def adapter():
        xml_data = legacy_service.get_user_data_xml()
        root = ET.fromstring(xml_data)
        return {child.tag: child.text for child in root}
    return adapter

# 测试适配器模式
def test_adapter_pattern():
    print("=== 适配器模式测试 ===")
    
    # 传统适配器
    legacy_service = LegacyDataService()
    adapter = XMLToJSONAdapter(legacy_service)
    user_data = adapter.get_user_data_json()
    print(f"📊 适配后的用户数据: {user_data}")
    
    # Pythonic适配器
    modern_adapter = create_modern_adapter(legacy_service)
    user_data_pythonic = modern_adapter()
    print(f"🐍 Pythonic适配结果: {user_data_pythonic}")

test_adapter_pattern()