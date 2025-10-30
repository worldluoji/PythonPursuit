# OrderedDict
`OrderedDict` 是 `collections` 模块中的一个字典子类，它记住了键值对的插入顺序。在 Python 3.7+ 中，普通字典也保持了插入顺序，但 `OrderedDict` 仍然有独特的用途。

## 基本用法

```python
from collections import OrderedDict

# 创建有序字典
od = OrderedDict()
od['z'] = 1
od['a'] = 2
od['c'] = 3

print(od)  # OrderedDict([('z', 1), ('a', 2), ('c', 3)])

# 遍历时会保持插入顺序
for key, value in od.items():
    print(key, value)
# 输出:
# z 1
# a 2
# c 3
```

## 与普通字典的区别

### Python 3.6 及之前版本

```python
# 在 Python 3.6 之前，普通字典不保持顺序
regular_dict = {}
regular_dict['z'] = 1
regular_dict['a'] = 2
regular_dict['c'] = 3

# 顺序可能不同
print(regular_dict)  # 可能是 {'a': 2, 'c': 3, 'z': 1}

# 但 OrderedDict 总是保持顺序
ordered_dict = OrderedDict()
ordered_dict['z'] = 1
ordered_dict['a'] = 2
ordered_dict['c'] = 3
print(ordered_dict)  # 总是 OrderedDict([('z', 1), ('a', 2), ('c', 3)])
```

### Python 3.7+ 版本

在 Python 3.7+ 中，普通字典也保持了插入顺序，但 `OrderedDict` 仍有特殊功能：

```python
# Python 3.7+ 中普通字典也保持顺序
regular_dict = {'z': 1, 'a': 2, 'c': 3}
print(regular_dict)  # {'z': 1, 'a': 2, 'c': 3}

ordered_dict = OrderedDict([('z', 1), ('a', 2), ('c', 3)])
print(ordered_dict)  # OrderedDict([('z', 1), ('a', 2), ('c', 3)])
```

## OrderedDict 的特有方法

### 1. `move_to_end()` - 移动元素到开头或结尾

```python
from collections import OrderedDict

od = OrderedDict([('a', 1), ('b', 2), ('c', 3), ('d', 4)])
print("原始:", list(od.keys()))  # ['a', 'b', 'c', 'd']

# 移动到末尾
od.move_to_end('b')
print("移动b到末尾:", list(od.keys()))  # ['a', 'c', 'd', 'b']

# 移动到开头
od.move_to_end('c', last=False)
print("移动c到开头:", list(od.keys()))  # ['c', 'a', 'd', 'b']
```

### 2. `popitem()` - 弹出指定位置的元素

```python
od = OrderedDict([('a', 1), ('b', 2), ('c', 3)])

# 弹出最后一个元素 (LIFO)
last_item = od.popitem()
print("弹出的元素:", last_item)  # ('c', 3)
print("剩余字典:", dict(od))  # {'a': 1, 'b': 2}

# 弹出第一个元素 (FIFO)
od = OrderedDict([('a', 1), ('b', 2), ('c', 3)])
first_item = od.popitem(last=False)
print("弹出的元素:", first_item)  # ('a', 1)
print("剩余字典:", dict(od))  # {'b': 2, 'c': 3}
```

## 实际应用场景

### 1. 实现 LRU（最近最少使用）缓存

```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.capacity = capacity
    
    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        # 将访问的键移动到末尾（表示最近使用）
        self.cache.move_to_end(key)
        return self.cache[key]
    
    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            # 如果键已存在，移动到末尾
            self.cache.move_to_end(key)
        self.cache[key] = value
        
        # 如果超过容量，移除最久未使用的（开头的元素）
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)

# 使用示例
cache = LRUCache(2)
cache.put(1, 1)
cache.put(2, 2)
print(cache.get(1))  # 1
cache.put(3, 3)      # 这会使得键 2 被移除（因为容量为2）
print(cache.get(2))  # -1（已被移除）
```

### 2. 保持配置文件的读取顺序

```python
from collections import OrderedDict

def read_config(filename):
    config = OrderedDict()
    with open(filename, 'r') as f:
        for line in f:
            if '=' in line and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                config[key] = value
    return config

# 假设配置文件内容：
# [database]
# host=localhost
# port=5432
# name=mydb

config = read_config('config.ini')
for key, value in config.items():
    print(f"{key} = {value}")
# 保持配置文件中的顺序输出
```

### 3. 处理需要顺序的JSON数据

```python
import json
from collections import OrderedDict

# 有些JSON需要保持键的顺序
data = OrderedDict([
    ('name', 'Alice'),
    ('age', 30),
    ('city', 'New York'),
    ('country', 'USA')
])

# 转换为JSON字符串
json_str = json.dumps(data, indent=2)
print(json_str)
# 输出会保持 name, age, city, country 的顺序
```

### 4. 构建有序的配置类

```python
from collections import OrderedDict

class ConfigBuilder:
    def __init__(self):
        self._sections = OrderedDict()
    
    def add_section(self, name, **options):
        self._sections[name] = OrderedDict(options)
        return self
    
    def build(self):
        return self._sections

# 使用示例
config = (ConfigBuilder()
    .add_section('database', host='localhost', port=5432)
    .add_section('server', host='0.0.0.0', port=8000)
    .add_section('logging', level='INFO', file='app.log')
    .build())

for section_name, options in config.items():
    print(f"[{section_name}]")
    for key, value in options.items():
        print(f"{key} = {value}")
    print()
```

## 与普通字典的性能比较

```python
from collections import OrderedDict
import time

# 创建测试
size = 100000

# 普通字典
start = time.time()
regular_dict = {str(i): i for i in range(size)}
regular_time = time.time() - start

# 有序字典
start = time.time()
ordered_dict = OrderedDict((str(i), i) for i in range(size))
ordered_time = time.time() - start

print(f"普通字典创建时间: {regular_time:.4f}秒")
print(f"有序字典创建时间: {ordered_time:.4f}秒")
```

## 注意事项

1. **内存使用**: `OrderedDict` 比普通字典占用更多内存，因为它维护了一个双向链表来记录顺序
2. **Python 版本**: 在 Python 3.7+ 中，如果需要顺序，普通字典通常足够用了
3. **特殊操作**: 只有在需要 `move_to_end()` 等特殊操作时才必须使用 `OrderedDict`
4. **相等比较**: `OrderedDict` 会考虑顺序，而普通字典不会

```python
# 顺序比较
dict1 = {'a': 1, 'b': 2}
dict2 = {'b': 2, 'a': 1}
print(dict1 == dict2)  # True（普通字典不考虑顺序）

od1 = OrderedDict([('a', 1), ('b', 2)])
od2 = OrderedDict([('b', 2), ('a', 1)])
print(od1 == od2)  # False（OrderedDict 考虑顺序）
```

`OrderedDict` 在处理需要严格顺序的场景中非常有用，特别是在需要重新排列元素顺序或实现特定缓存策略时。