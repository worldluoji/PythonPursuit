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

### 2. 创建项目
```bash
uv init <your_project_name>
```

---

### 3. 依赖包管理
添加依赖包
```bash
uv add "mcp[cli]"
```

删除依赖包
```bash
uv remove "mcp[cli]"
```

---

### 4. 修改镜像源
```shell
# 临时设置环境变量（仅当前终端生效）
export UV_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple

# 永久生效（写入shell配置文件）
echo 'export UV_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple' >> ~/.zshrc  # zsh用户
source ~/.zshrc
```

--- 

### 5. 安装依赖
```shell
uv pip install -e .
```
这样会根据project.toml中的依赖包安装依赖。