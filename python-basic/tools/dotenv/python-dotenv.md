# python-dotenv
`python-dotenv` 是一个用于管理环境变量的Python库，它可以帮助开发者更优雅地处理项目配置。以下是详细的使用指南：

---

### **核心价值**
• 将敏感配置（API密钥、数据库密码等）与代码分离
• 实现不同环境（开发/测试/生产）的配置切换
• 符合12要素应用原则（The Twelve-Factor App）

---

### **基础使用**

#### 1. 安装
```bash
pip install python-dotenv  #3.13之前全局安装

uv add python-dotenv # 在uv创建的虚拟环境中，使用uv安装
```

#### 2. 创建 `.env` 文件
在项目根目录创建文件：
```ini
# .env
DATABASE_URL=postgres://user:password@localhost/dbname
SECRET_KEY=your-super-secret-key
DEBUG=True
API_TIMEOUT=30
```

#### 3. 加载配置
```python
from dotenv import load_dotenv
import os

# 自动搜索.env文件并加载
load_dotenv()  

# 使用配置
db_url = os.getenv("DATABASE_URL")
secret = os.getenv("SECRET_KEY")
debug_mode = os.getenv("DEBUG", False)  # 带默认值
```

---

### **高级用法**

#### 1. 指定自定义路径
```python
load_dotenv('/path/to/special/.env')
```

#### 2. 多环境配置
```bash
.env          # 基础配置
.env.local    # 本地覆盖配置（加入.gitignore）
.env.prod     # 生产环境配置
```

加载指定环境：
```python
load_dotenv('.env.prod')
```

#### 3. 类型转换
```python
from dotenv import dotenv_values

config = dotenv_values()  # 返回字典
timeout = int(config["API_TIMEOUT"])  # 转换为整数
is_debug = config["DEBUG"].lower() in ('true', '1', 't')  # 转布尔
```

#### 4. 动态值
支持命令替换（需安装`python-dotenv[cli]`）：
```ini
TIMESTAMP=@datetime.now().strftime("%Y%m%d")
```

---

### **最佳实践**

#### 1. 安全规范
```ini
# 正确格式
SECURE_KEY="value-with-special$#characters"
MULTILINE_VAR="Line1\nLine2"

# 错误示范
UNSAFE_KEY = value with spaces  # 需要引号包裹
```

#### 2. 版本控制
• 提交 `.env.example`（无敏感值）
• 将 `.env` 加入 `.gitignore`

示例 `.env.example`：
```ini
DATABASE_URL=
SECRET_KEY=your-key-here
DEBUG=False
```

#### 3. 与框架集成
Flask示例：
```python
from flask import Flask
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
```

---

### **常见问题处理**

#### 1. 变量覆盖问题
```python
# 优先使用系统环境变量
load_dotenv(override=False)  
```

#### 2. 多行值处理
```ini
CERTIFICATE="-----BEGIN CERT-----\n...\n-----END CERT-----"
```

#### 3. 嵌套变量
```ini
BASE_DIR=/opt/myapp
LOG_FILE=${BASE_DIR}/app.log
```

---

### **调试技巧**
查看已加载的环境变量：
```python
import pprint
from dotenv import dotenv_values

pprint.pprint(dotenv_values())
```

通过命令行验证：
```bash
python -m dotenv list  # 查看解析结果
python -m dotenv run -- python your_script.py  # 带环境执行
```

---

### **版本兼容性**
• 支持Python 3.7+
• 支持跨平台（Windows/Linux/macOS）
• 最新版本（1.0+）默认不覆盖已存在的环境变量

---

合理使用 `python-dotenv` 可以使你的项目配置管理更加专业和安全，特别是在团队协作和持续集成场景中能显著提升开发体验。建议结合配置文件验证工具（如pydantic的 `BaseSettings`）使用效果更佳。