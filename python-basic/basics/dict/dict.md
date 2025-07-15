# dict

## 遍历
遍历一个字典（`dict`）有几种常见的方式，以下是一些遍历字典的方法：

1. 遍历键（Keys）：
   使用 `.keys()` 方法或者直接遍历字典会默认遍历其键。
   ```python
   my_dict = {'a': 1, 'b': 2, 'c': 3}
   for key in my_dict:  # 或者使用 my_dict.keys()
       print(key)
   ```

2. 遍历值（Values）：
   如果你只对字典的值感兴趣，可以使用 `.values()` 方法。
   ```python
   for value in my_dict.values():
       print(value)
   ```

3. 同时遍历键和值（Key-Value Pairs）：
   使用 `.items()` 方法来同时获取键和值。
   ```python
   for key, value in my_dict.items():
       print(f"{key}: {value}")
   ```

4. 使用 `enumerate()` 获取索引和键值对：
   如果你需要知道当前项的索引位置，可以结合 `enumerate()` 和 `.items()` 来使用。
   ```python
   for index, (key, value) in enumerate(my_dict.items()):
       print(f"Index {index}: {key} -> {value}")
   ```

5. 按特定顺序遍历：
   如果需要按键排序后遍历，可以先将键转换为列表并排序。
   ```python
   for key in sorted(my_dict.keys()):
       print(f"{key}: {my_dict[key]}")
   ```

6. 反向遍历：
   如果想要反向遍历字典的键，可以在遍历之前先反转键的列表。
   ```python
   for key in reversed(list(my_dict.keys())):
       print(f"{key}: {my_dict[key]}")
   ```

## 判断key值是否存在于字典中
```python
if ("a" in my_dict):
    print("a存在于字典中")
```

---

## dict设置值

在Python中，字典（`dict`）的值设置是数据处理的核心操作之一。以下是综合多种场景的完整指南，涵盖基础语法、进阶技巧及性能优化策略：

---

### **一、基础设置方法**
1. **直接赋值**  
   - **语法**：`dict[key] = value`  
   - **功能**：若键存在则覆盖值，不存在则新增键值对。  
   - **示例**：  
     ```python
     my_dict = {"name": "Alice", "age": 25}
     my_dict["age"] = 26  # 更新现有键
     my_dict["city"] = "New York"  # 新增键
     print(my_dict)  # {'name': 'Alice', 'age': 26, 'city': 'New York'}
     ```  
     *适用场景*：单键更新或添加。

2. **`update()` 方法**  
   - **语法**：`dict.update(other_dict)`  
   - **功能**：合并另一个字典或键值对可迭代对象，重复键会被覆盖。  
   - **示例**：  
     ```python
     my_dict.update({"age": 27, "country": "USA"})
     # 或通过解包合并：my_dict.update({**dict2, **dict3})
     ```  
     *优势*：批量更新效率高。

3. **`setdefault()` 方法**  
   - **语法**：`dict.setdefault(key, default_value)`  
   - **功能**：若键存在则返回其值，否则设置默认值并返回。  
   - **示例**：  
     ```python
     gender = my_dict.setdefault("gender", "unknown")  # 若键不存在则添加
     ```  
     *适用场景*：需避免覆盖现有值时使用。

---

### **二、进阶操作技巧**
1. **字典解包合并**  
   - **语法**：`{**dict1, **dict2}`  
   - **功能**：合并多个字典生成新字典，原字典不变。  
   - **示例**：  
     ```python
     merged_dict = {**dict1, **dict2}  # dict2覆盖dict1的重复键
     ```  
     *优势*：不修改原字典，适合需要保留原始数据的场景。

2. **字典推导式**  
   - **语法**：`{k: v for k, v in iterable}`  
   - **功能**：基于现有数据生成新字典，支持条件过滤或值转换。  
   - **示例**：  
     ```python
     # 将原字典值翻倍
     doubled_values = {k: v*2 for k, v in my_dict.items() if isinstance(v, int)}
     ```  
     *适用场景*：复杂数据转换或筛选。

3. **条件更新**  
   - **语法**：结合条件判断动态更新值。  
   - **示例**：  
     ```python
     if "age" in my_dict and my_dict["age"] < 30:
         my_dict["age"] += 1
     ```  
     *优势*：避免无效更新，提升代码健壮性。

---

### **三、特殊场景处理**
1. **嵌套字典更新**  
   - **问题**：直接赋值无法更新深层嵌套结构。  
   - **解决方案**：递归更新或使用`collections.defaultdict`。  
   - **示例**：  
     ```python
     # 递归更新嵌套字典
     def update_nested(d, key_path, value):
         keys = key_path.split(".")
         for k in keys[:-1]:
             d = d.setdefault(k, {})
         d[keys[-1]] = value

     update_nested(my_dict, "address.city", "Los Angeles")
     ```  
     *输出*：`{'address': {'city': 'Los Angeles'}, ...}`。

2. **默认值管理**  
   - **`collections.defaultdict`**：自动为不存在的键生成默认值。  
   - **示例**：  
     ```python
     from collections import defaultdict
     nested_dict = defaultdict(lambda: defaultdict(int))
     nested_dict["stats"]["count"] += 1  # 自动创建嵌套结构
     ```  
     *优势*：简化嵌套字典初始化。

---

### **四、性能优化建议**
1. **减少重复查找**  
   - 对频繁访问的键，先赋值给变量：  
     ```python
     key = "age"
     count = 0
     for _ in range(1000):
         count += my_dict[key]  # 避免多次哈希查找
     ```

2. **批量操作优先**  
   - 使用`update()`或解包合并替代循环赋值，减少函数调用开销。

3. **不可变字典优化**  
   - 对无需修改的字典，使用`types.MappingProxyType`创建只读视图，提升并发安全性。

---

### **五、常见错误与规避**
| **错误类型**         | **示例**                          | **修正方案**                     |
|-----------------------|-----------------------------------|----------------------------------|
| `KeyError`            | `my_dict["non_existent_key"]`     | 使用`get()`或`setdefault()`      |
| 覆盖嵌套数据          | `my_dict["a"]["b"] = 2`（若`a`不存在） | 先确保父键存在或使用`defaultdict` |
| 解包合并顺序错误      | `{**dict2, **dict1}`（`dict1`覆盖`dict2`） | 调整顺序：`{**dict1, **dict2}`   |

---

### **六、总结**
- **简单操作**：直接赋值（单键）或`update()`（批量）是最常用方法。  
- **复杂场景**：嵌套更新用递归或`defaultdict`，条件更新结合逻辑判断。  
- **性能敏感**：优先使用字典推导式或解包合并，避免循环内重复操作。  