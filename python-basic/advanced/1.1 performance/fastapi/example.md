# FastAPI综合示例
下面是一个覆盖多种常用功能的FastAPI示例，包含配置管理、多种响应类型、表单处理、JSON处理和文件上传功能。

## 1. 项目结构

```
fastapi_demo/
├── main.py
├── config.py
├── .env
├── templates/
│   └── index.html
└── static/
    ├── css/
    │   └── style.css
    └── images/
        └── logo.png
```

## 2. 配置文件及参数配置

### config.py
```python
from pydantic_settings import BaseSettings
from pydantic import SecretStr

class Settings(BaseSettings):
    # 应用配置
    app_name: str = "FastAPI综合示例"
    debug: bool = False
    
    # 安全密钥
    secret_key: SecretStr = SecretStr("your_default_secret_key")
    
    # 静态资源配置
    static_dir: str = "static"
    templates_dir: str = "templates"
    
    # 环境文件配置
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore"
    }
```

### .env
```
APP_NAME="生产环境应用"
DEBUG=True
SECRET_KEY="your_production_secret_key"
STATIC_DIR="static"
TEMPLATES_DIR="templates"
```

## 3. 主应用代码

### main.py
```python
from fastapi import FastAPI, Request, Form, UploadFile, File, Depends, HTTPException
from fastapi.responses import PlainTextResponse, JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
import os
from config import Settings

# 创建配置实例
settings = Settings()

# 创建FastAPI应用
app = FastAPI(
    title=settings.app_name,
    debug=settings.debug
)

# 配置Jinja2模板
templates = Jinja2Templates(directory=settings.templates_dir)

# 配置静态资源
app.mount("/static", StaticFiles(directory=settings.static_dir), name="static")

# 1. 普通字符串响应
@app.get("/")
def read_root():
    return PlainTextResponse("欢迎使用FastAPI综合示例！")

# 2. JSON响应
@app.get("/json")
def get_json():
    return {
        "message": "这是JSON响应示例",
        "app_name": settings.app_name,
        "debug": settings.debug
    }

# 3. Jinja2模板渲染
@app.get("/template", response_class=HTMLResponse)
def get_template(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "app_name": settings.app_name,
            "message": "这是Jinja2模板渲染示例"
        }
    )

# 4. 处理表单提交数据
@app.post("/form")
async def process_form(
    username: str = Form(...),
    email: str = Form(...),
    age: Optional[int] = Form(None)
):
    return {
        "message": "表单数据已接收",
        "username": username,
        "email": email,
        "age": age
    }

# 5. 处理JSON提交数据
class UserCreate(BaseModel):
    username: str
    email: str
    age: Optional[int] = None

@app.post("/json-data")
def process_json_data(user: UserCreate):
    return {
        "message": "JSON数据已接收",
        "user": user
    }

# 6. 处理文件上传
@app.post("/upload")
async def upload_files(
    files: List[UploadFile] = File(...),
    description: Optional[str] = Form(None)
):
    # 确保上传目录存在
    upload_dir = os.path.join(settings.static_dir, "uploads")
    os.makedirs(upload_dir, exist_ok=True)
    
    # 保存文件
    saved_files = []
    for file in files:
        file_path = os.path.join(upload_dir, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())
        saved_files.append(file.filename)
    
    return {
        "message": "文件上传成功",
        "files": saved_files,
        "description": description
    }

# 7. 自定义错误处理
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail}
    )
```

### templates/index.html
```html
<!DOCTYPE html>
<html>
<head>
    <title>{{ app_name }}</title>
    <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>
    <div class="container">
        <h1>{{ message }}</h1>
        <p>应用名称: {{ app_name }}</p>
        <p>调试模式: {{ debug }}</p>
    </div>
</body>
</html>
```

## 4. 功能说明

### 4.1 配置管理
- 使用`pydantic-settings`实现**类型安全**的配置管理
- 支持从`.env`文件加载配置
- **环境变量优先级**：环境变量 > .env文件 > 默认值

### 4.2 响应类型
1. **普通字符串**：使用`PlainTextResponse`返回纯文本
2. **JSON响应**：直接返回Python字典，自动转换为JSON
3. **模板渲染**：使用Jinja2模板引擎渲染HTML

### 4.3 静态资源
- 配置`/static`路由提供静态文件服务
- 支持CSS、JavaScript、图片等资源
- 自动处理MIME类型

### 4.4 表单处理
- 使用`Form`类型声明获取表单字段
- **必填字段**：`Form(...)`
- **可选字段**：`Form(None)`或`Optional[type] = Form(None)`
- 需要安装`python-multipart`包

### 4.5 JSON处理
- 使用Pydantic模型定义数据结构
- 自动验证和转换数据类型
- 提供详细的错误信息

### 4.6 文件上传
- 使用`UploadFile`类型处理文件
- 支持**多文件上传**
- 可同时接收文件和其他表单字段
- 需要使用`await file.read()`异步读取文件内容

## 5. 运行方式

1. 安装依赖：
```bash
pip install "fastapi[standard]"
```

2. 运行应用：
```bash
uvicorn main:app --reload
```

3. 访问以下端点测试功能：
   - `http://localhost:8000/` - 普通字符串响应
   - `http://localhost:8000/json` - JSON响应
   - `http://localhost:8000/template` - 模板渲染
   - `http://localhost:8000/form` - 表单提交（使用Postman测试）
   - `http://localhost:8000/json-data` - JSON提交（使用Postman测试）
   - `http://localhost:8000/upload` - 文件上传（使用Postman测试）

## 6. 重要提示

- **生产环境**：务必设置`DEBUG=False`并配置安全的`SECRET_KEY`
- **文件上传**：生产环境中应添加文件类型验证和大小限制
- **表单处理**：所有表单字段获取必须使用`async`和`await`
- **配置优先级**：环境变量 > .env文件 > 默认值