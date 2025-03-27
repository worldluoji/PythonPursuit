# Poetry
Poetry 是一个用于 Python 项目依赖管理和打包的现代化工具，它结合了 `pip`、`virtualenv`、`setuptools` 和 `pipenv` 的功能，提供更简洁高效的工作流。以下是 Poetry 的核心使用场景和常用方法详解：

---

### 一、使用场景
1. **依赖管理**  
   • 自动解析和安装依赖的兼容版本，避免版本冲突。
   • 生成 `poetry.lock` 文件锁定依赖版本，确保环境一致性。
   • 区分生产依赖（`dependencies`）和开发依赖（`dev-dependencies`）。

2. **虚拟环境管理**  
   • 自动创建和管理项目的独立虚拟环境，避免全局污染。

3. **打包与发布**  
   • 支持将项目打包为 `wheel` 或 `sdist` 格式。
   • 直接发布到 PyPI 或其他私有仓库。

4. **项目初始化与配置**  
   • 通过交互式命令快速生成 `pyproject.toml` 文件（替代 `setup.py` 和 `requirements.txt`）。

---

### 二、常用方法详解

#### 1. 安装 Poetry
```bash
# 官方推荐安装方式（Linux/macOS）
curl -sSL https://install.python-poetry.org | python3 -

# Windows（PowerShell）
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -

# 验证安装
poetry --version
```

配置国内镜像源：
```shell
poetry source add --priority=primary mirrors https://mirror.sjtu.edu.cn/pypi/web/simple
```

#### 2. 初始化项目
```bash
# 创建新项目
poetry new my-project

# 在现有项目初始化（生成 pyproject.toml）
cd existing-project
poetry init
```
• 交互式填写项目信息（如名称、版本、依赖等）。

#### 3. 管理依赖
```bash
# 添加生产依赖
poetry add requests

# 添加开发依赖（如 pytest）
poetry add pytest --group dev

# 安装所有依赖（生产+开发）
poetry install

# 仅安装生产依赖
poetry install --only main

# 更新依赖
poetry update          # 更新所有依赖
poetry update requests  # 更新指定依赖

# 移除依赖
poetry remove requests
```

#### 4. 虚拟环境管理
```bash
# 激活虚拟环境
poetry shell

# 在虚拟环境中运行命令（不激活）
poetry run python script.py

# 查看虚拟环境路径
poetry env info

# 删除虚拟环境
poetry env remove python3.11
```

#### 5. 打包与发布
```bash
# 构建项目（生成 dist/ 目录）
poetry build

# 发布到 PyPI
poetry publish

# 发布到私有仓库
poetry publish -r my-private-repo
```

#### 6. 其他常用命令
```bash
# 查看依赖树
poetry show --tree

# 检查依赖冲突
poetry check

# 导出为 requirements.txt（兼容传统工具）
poetry export -f requirements.txt --output requirements.txt

# 配置 PyPI 镜像源
poetry config repositories.my-private-repo https://example.com/pypi/
```

---

### 三、`pyproject.toml` 文件示例
```toml
[tool.poetry]
name = "my-project"
version = "0.1.0"
description = "A sample project"
authors = ["Your Name <you@example.com>"]

[tool.poetry.dependencies]
python = "^3.8"
requests = "^2.28.0"

[tool.poetry.group.dev.dependencies]
pytest = "^7.2.0"

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"
```

---

### 四、最佳实践
1. **版本约束语法**  
   • `^1.2.3`：允许 1.x.x，但不低于 1.2.3（如 1.3.0 允许，2.0.0 不允许）。
   • `~1.2.3`：允许 1.2.x，但不低于 1.2.3（如 1.2.4 允许，1.3.0 不允许）。

2. **锁定依赖版本**  
   • 始终提交 `poetry.lock` 到版本控制，确保团队环境一致。

3. **多环境管理**  
   • 使用 `--group <group-name>` 管理测试、文档等不同环境依赖。

4. **与 IDE 集成**  
   • 在 VS Code、PyCharm 等 IDE 中配置 Poetry 虚拟环境路径。

---

### 五、常见问题
1. **依赖冲突**  
   • 运行 `poetry update` 或手动调整版本约束。

2. **兼容性问题**  
   • 检查 Python 版本约束（如 `python = "^3.8"`）。

3. **离线使用**  
   • 通过 `poetry install --no-cache` 避免缓存问题。

---

通过 Poetry，开发者可以告别繁琐的手动配置，实现从依赖管理到打包发布的全流程自动化，显著提升 Python 项目的可维护性和协作效率。