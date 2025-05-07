要设置 UV 中的 Python 镜像源，需根据场景区分「包管理镜像」和「Python 安装镜像」两类配置。以下是具体方法：

---

一、包管理镜像设置（加速第三方包安装）
1. **命令行参数法**
   • 默认镜像（替换 PyPI 官方源）：  

     ```bash
     uv add fastapi --default-index https://pypi.tuna.tsinghua.edu.cn/simple
     ```
   • 多镜像源（适用于混合使用私有源和公共源）：  

     ```bash
     uv add fastapi --index https://mirrors.aliyun.com/pypi/simple https://internal.company.com/simple
     ```
   *适用场景：临时安装时指定镜像，灵活性高。*

2. **环境变量法**
   • 全局镜像（推荐）：  

     设置 `UV_DEFAULT_INDEX` 环境变量（覆盖默认 PyPI 源）：
     ```bash
     # Linux/macOS
     export UV_DEFAULT_INDEX=https://mirrors.aliyun.com/pypi/simple

     # Windows（PowerShell）
     $env:UV_DEFAULT_INDEX = "https://mirrors.aliyun.com/pypi/simple"
     ```
   • 多镜像源：  

     使用 `UV_INDEX` 环境变量（多个 URL 用空格分隔）：
     ```bash
     export UV_INDEX="https://mirrors.aliyun.com/simple https://internal.company.com/simple"
     ```
   *适用场景：长期全局配置，避免重复输入参数。*

3. **配置文件法**
   • 项目级配置：  

     在项目根目录的 `pyproject.toml` 中添加：
     ```toml
     [tool.uv]
     index-url = "https://pypi.tuna.tsinghua.edu.cn/simple"
     ```
   • 用户级配置：  

     在用户目录的 `uv.toml`（如 `~/.config/uv/uv.toml`）中添加：
     ```toml
     [[index]]
     url = "https://mirrors.aliyun.com/pypi/simple"
     default = true
     ```
   *适用场景：团队协作或跨项目统一配置。*

---

二、Python 安装镜像设置（加速 Python 解释器下载）
当使用 `uv python install` 安装 Python 解释器时，需配置专用镜像：
• 环境变量法（CPython 镜像）：

  ```bash
  # Linux/macOS
  export UV_PYTHON_INSTALL_MIRROR=https://mirror.nju.edu.cn/github-release/indygreg/python-build-standalone/

  # Windows
  $env:UV_PYTHON_INSTALL_MIRROR = "https://mirror.nju.edu.cn/github-release/indygreg/python-build-standalone/"
  ```
  *注意：南京大学镜像仅同步最新版本，历史版本需自建代理或使用其他加速服务。*

---

三、常用镜像源推荐
| 镜像名称       | 包管理 URL                              | Python 安装镜像 URL（仅 CPython）            |
|----------------|----------------------------------------|---------------------------------------------|
| 清华大学       | `https://pypi.tuna.tsinghua.edu.cn/simple` | 不支持                                       |
| 阿里云         | `https://mirrors.aliyun.com/pypi/simple`    | 不支持                                       |
| 南京大学       | 不支持                                 | `https://mirror.nju.edu.cn/github-release/indygreg/python-build-standalone/` |

---

四、验证配置是否生效
1. 包管理验证：
   ```bash
   uv add requests -v  # 观察下载日志中的源地址
   ```
2. Python 安装验证：
   ```bash
   uv python install 3.12 --mirror  # 指定镜像下载
   ```

---

总结：推荐优先使用环境变量或配置文件实现全局镜像设置，避免重复操作。若需深度定制（如自建代理镜像），可参考搭建智能代理站方案。