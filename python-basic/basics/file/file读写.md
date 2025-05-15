# file读写
以下是 Python 3 中文件读写的详细指南，涵盖常见场景和最佳实践：

---

### **一、基础文件操作**
#### **1. 文件打开模式**
| 模式 | 描述 | 示例 |
|------|------|------|
| `r`  | 只读（默认） | `open('file.txt', 'r')` |
| `w`  | 写入（覆盖） | `open('file.txt', 'w')` |
| `a`  | 追加写入 | `open('file.txt', 'a')` |
| `r+` | 读写模式 | `open('file.txt', 'r+')` |
| `b`  | 二进制模式 | `open('image.png', 'rb')` |

---

#### **2. 读取文件**
##### **基础读取**
```python
# 使用 with 语句自动关闭文件
with open('example.txt', 'r', encoding='utf-8') as f:
    content = f.read()  # 读取全部内容
    lines = f.readlines()  # 读取为列表（每行一个元素）
    line = f.readline()  # 逐行读取
```

##### **逐行读取大文件**
```python
with open('large_file.txt', 'r') as f:
    for line in f:  # 逐行迭代，内存友好
        print(line.strip())
```

---

#### **3. 写入文件**
##### **覆盖写入**
```python
with open('output.txt', 'w', encoding='utf-8') as f:
    f.write('Hello, Python!\n')  # 写入字符串
    f.writelines(['Line 1\n', 'Line 2\n'])  # 写入列表
```

##### **追加写入**
```python
with open('log.txt', 'a') as f:
    f.write('New log entry\n')
```

---

### **二、高级文件操作**
#### **1. 处理 JSON 文件**
```python
import json

# 写入 JSON
data = {'name': 'Alice', 'age': 30}
with open('data.json', 'w') as f:
    json.dump(data, f, indent=4)

# 读取 JSON
with open('data.json', 'r') as f:
    loaded_data = json.load(f)
    print(loaded_data['name'])  # 输出: Alice
```

---

#### **2. 处理 CSV 文件**
```python
import csv

# 写入 CSV
with open('data.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Name', 'Age'])
    writer.writerow(['Bob', 25])

# 读取 CSV
with open('data.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)  # 输出: ['Name', 'Age'], ['Bob', '25']
```

---

#### **3. 二进制文件操作**
```python
# 读取二进制文件（如图片）
with open('image.png', 'rb') as f:
    binary_data = f.read()

# 写入二进制文件
with open('copy.png', 'wb') as f:
    f.write(binary_data)
```

---

### **三、异常处理**
```python
try:
    with open('non_existent.txt', 'r') as f:
        print(f.read())
except FileNotFoundError:
    print("文件不存在！")
except PermissionError:
    print("无权限访问文件！")
except Exception as e:
    print(f"未知错误: {e}")
```

---

### **四、路径处理（`pathlib` 模块）**
```python
from pathlib import Path

# 创建路径对象
file_path = Path('data') / 'example.txt'

# 检查文件是否存在
if file_path.exists():
    print(f"文件大小: {file_path.stat().st_size} bytes")

# 写入文件
file_path.write_text('Hello from Pathlib!', encoding='utf-8')
```

---

### **五、最佳实践**
1. **始终使用 `with` 语句**  
   确保文件正确关闭，避免资源泄漏。

2. **指定文件编码**  
   使用 `encoding='utf-8'` 避免跨平台编码问题。

3. **处理大文件时逐行读取**  
   避免一次性加载全部内容导致内存溢出。

4. **优先使用 `pathlib`**  
   替代传统 `os.path`，更简洁安全。

5. **谨慎使用 `w` 模式**  
   覆盖写入会永久删除原内容，必要时先备份。

---

### **六、性能对比**
| 方法 | 内存占用 | 适用场景 |
|------|----------|----------|
| `f.read()` | 高 | 小文件快速处理 |
| `f.readlines()` | 高 | 需要行列表的场景 |
| 逐行迭代 | 低 | 大文件处理 |
