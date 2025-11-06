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

# 看看创建了什么
print(f"🎯 类属性: {MyClass.class_attribute}")
print(f"🔧 元类添加的属性: {MyClass.created_by}")