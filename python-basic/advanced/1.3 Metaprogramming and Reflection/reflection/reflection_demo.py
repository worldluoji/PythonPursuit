import inspect

class SimpleMeta(type):
    """简单的元类示例"""
    
    def __new__(cls, name, bases, namespace):
        print(f"🔮 正在创建类: {name}")
        print(f"📦 命名空间内容: {list(namespace.keys())}")
        print(f"⌚️ bases 是一个元组，包含了正在创建的类所继承的所有父类: {bases}")
        
        # 在创建类时自动添加一些属性
        namespace['created_by'] = 'SimpleMeta'
        namespace['creation_timestamp'] = '2024'
        
        return super().__new__(cls, name, bases, namespace)

# 使用我们的元类创建类
class MyClass(metaclass=SimpleMeta):
    """使用自定义元类的示例类"""
    class_attribute = "Hello"
    
    def my_method(self):
        return "World"
    
def demonstrate_reflection(obj):
    """演示Python的反射能力"""
    
    print(f"🔍 检查对象: {obj}")
    
    # 获取所有属性和方法
    members = inspect.getmembers(obj)
    print(f"📋 所有成员: {[name for name, _ in members if not name.startswith('_')]}")
    
    # 动态获取和调用方法
    if hasattr(obj, 'my_method'):
        method = getattr(obj, 'my_method')
        result = method()
        print(f"⚡ 动态调用结果: {result}")
    
    # 修改对象属性
    if hasattr(obj, 'class_attribute'):
        current_value = getattr(obj, 'class_attribute')
        setattr(obj, 'class_attribute', f"Modified: {current_value}")
        print(f"🔧 修改后属性: {getattr(obj, 'class_attribute')}")

# 测试反射功能
demonstrate_reflection(MyClass())

# 更高级的反射：动态创建类
def create_class_dynamically(class_name, attributes):
    """动态创建类"""
    namespace = {}
    for attr_name, attr_value in attributes.items():
        namespace[attr_name] = attr_value
    
    # 使用type动态创建类
    DynamicClass = type(class_name, (), namespace)
    return DynamicClass

# 动态创建一个类
dynamic_class = create_class_dynamically(
    "DynamicClass", 
    {"dynamic_attr": "I was created dynamically!", "get_info": lambda self: self.dynamic_attr}
)


instance = dynamic_class()
print(f"🎭 动态创建的对象: {instance.get_info()}")