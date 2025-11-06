class PropertyLevelControl:
    """描述符：在属性访问时介入"""

    def __init__(self, initial_value=None):
        self.value = initial_value
        self.access_count = 0

    def __get__(self, instance, owner):
        self.access_count += 1
        print(f"🔍 属性被访问第{self.access_count}次")
        return self.value

    def __set__(self, instance, value):
        print(f"✏️ 属性被设置为: {value}")
        self.value = value

    def __delete__(self, instance):
        print("🗑️ 属性被删除")
        self.value = None


class DataClass:
    data = PropertyLevelControl("初始值")  # 描述符实例


# 测试：每次属性访问都会触发自定义逻辑
obj = DataClass()
print(obj.data)  # 触发__get__
obj.data = "新值"  # 触发__set__
print(obj.data)  # 再次触发__get__
del obj.data