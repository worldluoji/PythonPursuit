# __all__

在Python中，`__all__` 是一个特殊的模块级变量，**用于控制当其他代码通过 `from module import *` 导入该模块时，哪些名称（变量、函数、类等）会被自动暴露给外部**。以下是具体分析：

---

### **1. `__all__` 的核心作用**
- **白名单机制**：当模块定义了 `__all__` 时，`from module import *` **只会导入 `__all__` 列表中明确列出的名称**。
- **隐藏非公开接口**：未在 `__all__` 中列出的名称（即使它们是全局的且不以 `_` 开头）不会被导入。
- **代码自文档化**：明确声明模块的公开接口，便于维护和理解。

---

### **2. 示例代码分析**
```python
from . import server  # 从当前包导入 server 模块

def main():
    """Main entry point for the package."""
    server.main()

# 定义 __all__，指定公开暴露的名称
__all__ = ["main", "server"]
```

#### **关键行为解释**：
1. **默认情况（无 `__all__`）**：  
   若没有 `__all__`，`from package import *` 会导入模块中所有 **不以单下划线 `_` 开头** 的全局名称。  
   - 在该示例中，默认会导出 `main` 和 `server`（因为它们符合条件）。

2. **显式定义 `__all__` 后**：  
   - 即使有其他全局名称，只有 `main` 和 `server` 会被 `from package import *` 导入。
   - 即使存在其他名称（例如内部工具函数或变量），也会被隐藏。

---

### **3. 使用场景**
#### **场景 1：限制暴露的接口**
假设模块中定义了多个函数，但只有部分是对外公开的：
```python
def public_func():
    pass

def _internal_helper():
    pass

__all__ = ["public_func"]  # 只允许导入 public_func
```

#### **场景 2：明确包的公共入口**
在包的 `__init__.py` 中，通过 `__all__` 声明包级别的公开接口：
```python
# mypackage/__init__.py
from .submodule import func1, func2
from .utils import helper

__all__ = ["func1", "func2"]  # 隐藏 helper
```

---

### **4. 注意事项**
- **仅对 `import *` 生效**：  
  显式导入（如 `from module import foo`）或直接导入模块（如 `import module`）**不受 `__all__` 限制**。
- **动态名称处理**：  
  `__all__` 中的名称必须是字符串，且需与模块中的全局名称完全一致。
- **与 `_` 前缀的互补性**：  
  即使名称以单下划线 `_` 开头，若其被加入 `__all__`，仍会被导出。二者可组合使用，但通常优先用 `__all__`。

---

### **5. 示例代码的实际意义**
在用户提供的代码中：
```python
__all__ = ["main", "server"]
```
- **目的**：  
  明确声明该模块的公开接口是 `main` 函数和 `server` 模块。
- **效果**：  
  当用户执行 `from package import *` 时，只能访问这两个名称，其他名称（即使存在）被隐藏。

---

### **总结**
`__all__` 是一个用于精细化控制模块导出行为的工具，**通过白名单机制确保模块的公共接口清晰可控**。在团队协作或构建公共库时，定义 `__all__` 能有效避免意外暴露内部实现细节，提升代码的可维护性。