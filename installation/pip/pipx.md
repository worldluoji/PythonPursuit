# pipx
pipx 是一个专为 Python 命令行工具设计的包管理工具。它的核心功能是将 Python 应用（CLI 工具）隔离安装在独立虚拟环境中，避免全局安装导致的依赖冲突，同时确保这些工具可以在系统的任何位置直接调用。

## 为什么需要 pipx？
- ​隔离环境: 当你用 pip install <工具名> 全局安装一个工具（如 black, pytest, poetry）时，它会被安装到系统的 Python 环境中。如果多个工具依赖不同版本的库，可能引发冲突。而 pipx 为每个工具单独创建虚拟环境，彼此隔离。
- ​安全卸载: 用 pipx uninstall 可以彻底删除工具及其关联的虚拟环境，而传统 pip uninstall 可能残留依赖。​
- 全局可用性: pipx 安装的工具会添加到系统路径（如 ~/.local/bin），可以直接在终端中调用，无需手动激活虚拟环境

目前，高版本的python，比如python3.13.3，已经不支持pip了，推荐使用pipx.
```shell
brew install pipx
```

---

## pipx镜像源配置
```shell
echo 'export PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple' >> ~/.zshrc
source ~/.zshrc  # 立即生效
```

---

## 总结
- ​用 pipx：安装需要在命令行全局调用的 Python 工具（如 uv, black, poetry）。
- ​用 uv/poetry：管理项目级别的虚拟环境和依赖。