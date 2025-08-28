# TypedDict
TypedDict 是 Python 类型提示系统中的一个重要工具，它允许你为字典定义具体的结构类型。

## 主要作用

1. **类型安全**：为字典提供明确的键和值类型提示
2. **代码可读性**：清晰表达字典应有的结构
3. **静态检查**：帮助类型检查器（如 mypy）验证代码正确性

## 基本用法

```python
from typing import TypedDict

class Person(TypedDict):
    name: str
    age: int
    email: str | None  # 可选字段

# 使用示例
person: Person = {
    "name": "Alice",
    "age": 30,
    "email": "alice@example.com"
}

def process_person(data: Person) -> None:
    print(f"Processing {data['name']}, age {data['age']}")
```

## 高级特性

```python
from typing import TypedDict, Optional

# 全部字段必填
class RequiredFields(TypedDict):
    required_field: str

# 可选字段（两种写法）
class OptionalFields(TypedDict, total=False):
    optional_field: str

class MixedFields(TypedDict):
    required_field: str
    optional_field: Optional[str]  # 与 Optional[str] 相同
```

## 实际应用场景

- API 请求/响应数据的类型定义
- 配置文件的类型验证
- 数据处理流水线中的中间数据结构

## 注意事项

- TypedDict 仅在类型检查时有效，运行时不会强制类型约束
- 需要配合 mypy 或其他类型检查器使用
- Python 3.8+ 推荐使用标准库中的 `typing.TypedDict`

TypedDict 大大提升了处理字典数据时的类型安全性和代码可维护性。