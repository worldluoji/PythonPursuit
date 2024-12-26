# JSON
在 Python 中读取 JSON 文件或字符串是一个常见的任务，Python 提供了内置的 `json` 模块来处理 JSON 数据。以下是如何使用 `json` 模块读取 JSON 文件和 JSON 字符串的基本示例。

### 读取 JSON 文件

假设你有一个名为 `data.json` 的文件，内容如下：

```json
{
  "name": "Alice",
  "age": 30,
  "is_student": false,
  "courses": ["Math", "Science"]
}
```

你可以使用以下代码来读取这个 JSON 文件并将其解析为 Python 字典：

#### 示例代码：从文件读取 JSON

```python
import json

# 打开并读取 JSON 文件
with open('data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# 现在 data 是一个 Python 字典
print(data)
print(type(data))  # 输出: <class 'dict'>

# 将字典转换为 JSON 字符串
json_string = json.dumps(data)
```

### 读取 JSON 字符串

如果你有一个 JSON 格式的字符串，可以直接使用 `json.loads()` 方法将其解析为 Python 对象。

#### 示例代码：从字符串读取 JSON

```python
import json

# JSON 字符串
json_string = '{"name": "Bob", "age": 25, "is_student": true, "courses": ["History", "Geography"]}'

# 解析 JSON 字符串为 Python 字典
data = json.loads(json_string)

# 现在 data 是一个 Python 字典
print(data)
print(type(data))  # 输出: <class 'dict'>
```

### 处理复杂的 JSON 数据

有时 JSON 数据可能包含嵌套的对象、数组等复杂结构。`json` 模块可以很好地处理这些情况，并将它们转换为相应的 Python 数据类型（如字典、列表等）。

#### 示例代码：处理复杂的 JSON 数据

```python
import json

# 假设我们有一个更复杂的 JSON 字符串
complex_json_string = '''
{
  "user": {
    "name": "Charlie",
    "age": 22,
    "preferences": {
      "theme": "dark",
      "notifications": true
    }
  },
  "orders": [
    {"id": 1, "item": "Laptop", "quantity": 1},
    {"id": 2, "item": "Mouse", "quantity": 2}
  ]
}
'''

# 解析 JSON 字符串为 Python 字典
data = json.loads(complex_json_string)

# 访问嵌套的数据
print("User's name:", data['user']['name'])
print("First order item:", data['orders'][0]['item'])

# 遍历订单列表
for order in data['orders']:
    print(f"Order ID {order['id']}: {order['quantity']}x {order['item']}")
```

### 错误处理

在实际应用中，读取 JSON 数据时可能会遇到格式错误或其他问题。为了确保程序的健壮性，应该添加适当的错误处理逻辑。

#### 示例代码：添加错误处理

```python
import json

try:
    with open('data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
except FileNotFoundError:
    print("The file was not found.")
except json.JSONDecodeError as e:
    print(f"Failed to decode JSON: {e}")
else:
    print("JSON data loaded successfully.")
finally:
    print("Operation completed.")
```
