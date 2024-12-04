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