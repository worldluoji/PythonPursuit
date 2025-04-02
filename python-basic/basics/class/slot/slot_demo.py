class DefaultUser:
    def __init__(self, name, age):
        self.name = name
        self.age = age

# 实例内存开销示例
import sys
u1 = DefaultUser("Bob", 25)
print(sys.getsizeof(u1.__dict__))  # 输出约 296 字节


class SlotUser:
    __slots__ = ('name', 'age') # 仅允许实例拥有name和age属性
    def __init__(self, name, age):
        self.name = name
        self.age = age

u2 = SlotUser("Bob", 25)
print(sys.getsizeof(u2))  # 输出约 48 字节