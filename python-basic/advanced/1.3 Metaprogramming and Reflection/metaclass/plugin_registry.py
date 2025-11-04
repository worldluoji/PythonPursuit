class PluginRegistry(type):
    """插件自动注册的元类"""
    _plugins = {}
    
    def __new__(cls, name, bases, namespace):
        new_class = super().__new__(cls, name, bases, namespace)
        
        # 自动注册非抽象类
        if not name.startswith('Abstract'):
            cls._plugins[name] = new_class
            print(f"📥 注册插件: {name}")
        
        return new_class
    
    @classmethod
    def get_plugins(cls):
        return cls._plugins

# 使用自动注册元类
class DataProcessor(metaclass=PluginRegistry):
    pass

class CSVProcessor(DataProcessor):
    """CSV处理插件"""
    def process(self, data):
        return f"Processing CSV: {data}"

class JSONProcessor(DataProcessor):
    """JSON处理插件"""
    def process(self, data):
        return f"Processing JSON: {data}"

# 查看自动注册的插件
print(f"📋 已注册插件: {list(PluginRegistry.get_plugins().keys())}")