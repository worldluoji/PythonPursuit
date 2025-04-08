
# uv配置环境变量

---

### **1. 了解环境变量的作用场景**
• **本地开发**：存储敏感信息（如 API 密钥、数据库密码）或配置不同环境的参数（如调试模式）。
• **工程隔离**：确保不同项目或虚拟环境中的变量互不干扰。

---

### **2. 添加环境变量的常用方法**

#### **方法一：临时设置（单次生效）**
在终端会话中直接设置变量（仅对当前终端窗口有效）：
```bash
# Linux/macOS
export OPENAI_API_KEY="sk-xxx"
export DEBUG_MODE="True"

# Windows（PowerShell）
$env:OPENAI_API_KEY = "sk-xxx"
$env:DEBUG_MODE = "True"
```

#### **方法二：持久化到虚拟环境（推荐）**
将变量写入虚拟环境的激活脚本，使变量仅在激活虚拟环境时生效：
1. **激活虚拟环境**（假设使用 `uv venv` 创建了 `.venv`）：
   ```bash
   source .venv/bin/activate  # Linux/macOS
   .venv\Scripts\activate     # Windows
   ```
2. **编辑激活脚本**，在文件末尾追加变量：
   ```bash
   # Linux/macOS（编辑 .venv/bin/activate）
   echo 'export OPENAI_API_KEY="sk-xxx"' >> .venv/bin/activate
   echo 'export DEBUG_MODE="True"' >> .venv/bin/activate

   # Windows（编辑 .venv/Scripts/activate.bat）
   # 在文件末尾添加：
   set OPENAI_API_KEY=sk-xxx
   set DEBUG_MODE=True
   ```
3. **重新激活环境**使变量生效：
   ```bash
   deactivate && source .venv/bin/activate  # Linux/macOS
   deactivate && .venv\Scripts\activate     # Windows
   ```

#### **方法三：使用 `.env` 文件（跨环境通用）**
1. 在工程根目录创建 `.env` 文件：
   ```bash
   # .env 内容示例
   OPENAI_API_KEY=sk-xxx
   DEBUG_MODE=True
   ```
2. **安装 `python-dotenv`** 加载变量：
   ```bash
   uv add python-dotenv
   ```
3. 在代码中读取变量：
   ```python
   from dotenv import load_dotenv
   import os

   load_dotenv()  # 默认加载 .env 文件
   api_key = os.getenv("OPENAI_API_KEY")
   debug_mode = os.getenv("DEBUG_MODE", "False") == "True"
   ```

---

### **3. 验证环境变量是否生效**
在 Python 脚本或终端中检查变量：
```python
# test_env.py
import os
print("API Key:", os.getenv("OPENAI_API_KEY"))
print("Debug Mode:", os.getenv("DEBUG_MODE"))
```
运行脚本：
```bash
# 激活虚拟环境后运行
python test_env.py
```

---

### **4. 安全注意事项**
• **不要提交敏感信息**：将 `.env` 添加到 `.gitignore`：
  ```bash
  echo ".env" >> .gitignore
  ```
• **区分不同环境**：为开发、测试、生产环境分别创建 `.env.dev`、`.env.prod`，按需加载：
  ```python
  load_dotenv(".env.prod")  # 加载生产环境配置
  ```

---

### **总结**
• **推荐方式**：使用 `.env` + `python-dotenv`，安全且跨平台。
• **虚拟环境隔离**：通过激活脚本设置变量，确保不同工程独立。
• **安全第一**：始终避免硬编码敏感信息，通过版本控制忽略 `.env` 文件。