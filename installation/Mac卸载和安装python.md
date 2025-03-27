# Mac卸载和安装python
在Mac上卸载Python 3.9并安装Python 3.10的步骤如下：

---

### **1. 确定Python 3.9的安装方式**
首先确认Python 3.9的安装方式，常见的有：
• **官方安装包**（从Python官网下载的.pkg文件）
• **Homebrew**（通过`brew install python`安装）
• **pyenv**（版本管理工具）

运行以下命令查看Python 3.9的路径：
```bash
which python3
```
• 如果路径是 `/usr/local/bin/python3`，可能是Homebrew安装的, 里面可能有多个python3版本，可以通过 ls -l python3* 查看。
• 如果路径是 `/Library/Frameworks/Python.framework/Versions/3.9/bin/python3`，则是官方安装包安装的。

---

### **2. 卸载Python 3.9**

#### **如果是通过官方安装包安装**
1. 删除Python 3.9文件：
   ```bash
   sudo rm -rf /Library/Frameworks/Python.framework/Versions/3.9
   ```
2. 删除应用程序目录中的Python 3.9：
   ```bash
   sudo rm -rf "/Applications/Python 3.9"
   ```
3. 删除符号链接（如果有）：
   ```bash
   sudo rm -f /usr/local/bin/python3
   sudo rm -f /usr/local/bin/pip3
   ```

#### **如果是通过Homebrew安装**
1. 卸载Python 3.9：
   ```bash
   brew uninstall python@3.9
   ```
2. 清理残留：
   ```bash
   brew cleanup
   ```

---

### **3. 清理残留配置**
• 删除Python 3.9的第三方库（如果有）：
  ```bash
  rm -rf ~/Library/Python/3.9
  ```
• 检查环境变量文件（`~/.bash_profile`、`~/.zshrc`等），移除对Python 3.9的路径引用。

---

### **4. 安装Python 3.10**

#### **推荐使用Homebrew安装**
1. 更新Homebrew：
   ```bash
   brew update
   ```
2. 安装Python 3.10：
   ```bash
   brew install python@3.10
   ```
3. 链接Python 3.10（如果提示需要）：
   ```bash
   brew link --overwrite python@3.10
   ```

#### **或通过官方安装包**
1. 访问 [Python官网](https://www.python.org/downloads/macos/) 下载3.10的.pkg文件。
2. 双击安装，按提示操作。

---

### **5. 验证安装**
1. 检查Python版本：
   ```bash
   python3 --version  # 应显示 "Python 3.10.x"
   ```
2. 检查pip版本：
   ```bash
   pip3 --version  # 应指向Python 3.10
   ```

---

### **6. 修复路径问题（如有必要）**
如果系统仍指向旧版本，调整环境变量：
1. 打开 `~/.zshrc`（或 `~/.bash_profile`）：
   ```bash
   nano ~/.zshrc
   ```
2. 确保Homebrew的路径优先：
   ```bash
   export PATH="/usr/local/bin:$PATH"
   ```
3. 生效配置：
   ```bash
   source ~/.zshrc
   ```

---

### **注意事项**
• 不要删除系统自带的Python 2.7（路径为 `/usr/bin/python`），以免影响系统工具。
• 使用虚拟环境（如`venv`或`virtualenv`）隔离项目依赖。

完成以上步骤后，Python 3.10即可正常使用！