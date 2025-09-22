# type
在 Python 中，当定义一个类时，默认情况下会使用 `type` 作为其**元类（metaclass）**，而不是父类（基类）。元类是“类的类”，用于控制类的创建过程。以下是对 `type` 的详细解释：

---

### **1. `type` 的双重身份**
- **作为内置函数**：`type(obj)` 返回对象的类型（如 `int`、`str`、自定义类等）。
  ```python
  print(type(42))          # <class 'int'>
  print(type("hello"))     # <class 'str'>
  ```
- **作为元类**：`type` 是所有类的默认元类（包括自身），负责创建类对象。

---

### **2. 类的创建过程**
当使用 `class` 关键字定义类时，Python 内部调用 `type` 来生成类对象：
```python
class MyClass:
    x = 10

# 等效于：
MyClass = type('MyClass', (), {'x': 10})
```
`type` 的三个参数：
1. **类名**（字符串）：`'MyClass'`
2. **基类元组**（继承的父类）：默认为空时，隐式继承 `object`
3. **命名空间字典**（类属性、方法）：`{'x': 10}`

类实际是type的实例：
```python
class MyClass:
    pass

print(type(MyClass))  # 输出: <class 'type'>
```

---

### **3. 元类与父类的区别**
- **父类（基类）**：影响类的继承关系和方法解析（如 `class Child(Parent)`）。
- **元类（metaclass）**：控制类的创建行为（如验证属性、自动注册类）。

#### **示例对比**
```python
# 父类是 object（默认）
class Base:
    pass

print(Base.__bases__)          # (<class 'object'>,)
print(type(Base))              # <class 'type'>（元类是 type）

# 显式指定元类为 type（默认行为）
class User(metaclass=type):
    pass
```

---

### **4. `type` 如何创建类**
#### **步骤拆解**
1. **收集类属性**：将类体中定义的属性和方法存入字典。
2. **调用 `type.__new__`**：根据类名、基类和属性字典创建类对象。
3. **初始化类**：调用 `type.__init__` 完成类对象的初始化。

#### **手动模拟类创建**
```python
# 定义类体中的方法
def say_hello(self):
    print(f"Hello, {self.name}!")

# 手动创建类
Person = type('Person', (object,), {
    'name': 'Anonymous',
    'greet': say_hello
})

p = Person()
p.greet()  # 输出: Hello, Anonymous!
```

---

### **5. 默认继承与元类的关系**
- **隐式继承 `object`**：若未指定基类，Python 自动将 `object` 作为基类。
- **元类始终为 `type`**：除非显式指定其他元类（如 `metaclass=MyMeta`）。

#### **验证代码**
```python
class A:
    pass

print(A.__bases__)    # 输出: (<class 'object'>,)
print(type(A))        # 输出: <class 'type'>
```

---

### **6. 自定义元类 vs 继承**
- **自定义元类**：通过 `metaclass=MyMeta` 改变类的创建逻辑。
- **继承**：通过基类添加共享方法或属性。

#### **示例：自定义元类**
```python
class Meta(type):
    def __new__(cls, name, bases, dct):
        dct['version'] = 1.0  # 自动添加版本属性
        return super().__new__(cls, name, bases, dct)

class App(metaclass=Meta):
    pass

print(App.version)  # 输出: 1.0
```

---

### **7. 为什么说 `type` 是自身的实例？**
`type` 的元类也是它自己，形成一个自洽的闭环：
```python
print(type(type))  # 输出: <class 'type'>
```
这说明 `type` 既是所有类的元类，也是自身的元类。

---

### **8. 总结**
- **`type` 是默认的元类**：负责创建所有类对象。
- **元类控制类的生成**：决定类的结构、属性和行为。
- **父类决定继承关系**：与元类职责分离，默认父类是 `object`。

理解 `type` 的双重身份和元类机制，是掌握 Python 面向对象底层原理的关键。