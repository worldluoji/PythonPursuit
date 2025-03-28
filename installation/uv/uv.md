# uv
以下是关于如何使用 `uv` 来管理 Python 项目的分步指南：

---

### 什么是 `uv`？
`uv` 是一个由 Astral 公司（Rust 生态中 `Ruff` 和 `Black` 的开发者）开发的 Python 包和虚拟环境管理工具。它旨在替代传统的 `pip` 和 `venv`，提供更快的安装速度和现代化的功能。

---

### 1. 安装 `uv`

#### 通过 `curl` 安装（推荐）
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
安装完成后，根据提示将 `uv` 添加到系统路径（可能需要重启终端）。

#### 通过 `pipx` 安装（可选）
```bash
pipx install uv
```

---

### 2. 创建虚拟环境

#### 初始化虚拟环境
```bash
uv venv .venv  # 在当前目录创建名为 `.venv` 的虚拟环境
```

#### 激活虚拟环境
• **Linux/macOS**:
  ```bash
  source .venv/bin/activate
  ```
• **Windows**:
  ```cmd
  .venv\Scripts\activate.bat
  ```

---

### 3. 安装依赖包

#### 从 `requirements.txt` 安装
```bash
uv pip install -r requirements.txt
```

#### 直接安装单个包
```bash
uv pip install requests
```

#### 安装开发依赖（例如 `black`）
```bash
uv pip install black --group dev
```

---

### 4. 管理依赖

#### 生成 `requirements.txt`
```bash
uv pip freeze > requirements.txt
```

#### 同步依赖到 `pyproject.toml`
```bash
uv pip sync pyproject.toml
```

---

### 5. 升级和卸载

#### 升级所有包
```bash
uv pip upgrade --all
```

#### 卸载包
```bash
uv pip uninstall requests
```

---

### 6. 项目迁移（从 `venv`/`pip` 切换）

1. 删除旧的虚拟环境：
   ```bash
   rm -rf .venv  # 或者删除其他旧环境目录
   ```

2. 用 `uv` 创建新环境并安装依赖：
   ```bash
   uv venv .venv
   source .venv/bin/activate  # 激活环境
   uv pip install -r requirements.txt
   ```

---

### 常见问题

#### 1. 虚拟环境路径问题
• 如果遇到路径错误，确保激活命令与操作系统匹配（Windows 使用反斜杠 `\`，Linux/macOS 使用正斜杠 `/`）。

#### 2. 替代 `pip` 命令
• 所有 `pip` 命令均可替换为 `uv pip`，例如：
  ```bash
  uv pip list
  uv pip show requests
  ```

#### 3. 性能优势
• `uv` 使用 Rust 实现，安装速度通常比传统 `pip` 快 10-100 倍，尤其在大型项目中优势明显。

---

### 高级用法

#### 依赖组管理
在 `pyproject.toml` 中定义依赖组：
```toml
[tool.uv]
dependencies = ["requests"]
dev = ["black", "pytest"]
```

安装所有依赖组：
```bash
uv pip install . --all-groups
```

---

通过 `uv`，你可以更高效地管理 Python 项目依赖和虚拟环境。如果需要更详细的文档，请参考 [uv 官方文档](https://github.com/astral-sh/uv)。