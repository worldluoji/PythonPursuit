# 国内合规访问github自动化办法
可以自动化，完全不需要每次都手动查 IP 再改 hosts。下面给出**现成工具**和**自己写脚本**两种方案，挑喜欢的用就行。

---

## 方案一：用现成工具（推荐，省心）

### 1. GitHub520 + SwitchHosts（最流行）
- **GitHub520** 是一个专门解决 GitHub 访问问题的项目，会定期检测并更新可用的 GitHub IP，维护一个 hosts 文件。
- **SwitchHosts** 是一个 hosts 管理工具，支持订阅远程 hosts 并自动更新。

**操作步骤（Windows/macOS）：**
1. 下载安装 [SwitchHosts](https://github.com/oldj/SwitchHosts/releases)。
2. 打开 SwitchHosts，点击左上角“+”添加规则：
   - **Hosts 标题**：随意，如 `GitHub`
   - **类型**：`远程`
   - **URL**：填入  
     `https://raw.hellogithub.com/hosts`  
     （这是 GitHub520 项目的镜像，能稳定访问）
   - **自动更新**：建议勾选，设置间隔 1 小时。
3. 点击确定，然后打开这个规则开关，SwitchHosts 会自动合并到系统 hosts 文件。
4. 遇到权限提示，授予管理员权限即可。

✅ 优点：无需写代码，一劳永逸，作者社区会维护 IP 列表。

### 2. 直接用 GitHub520 的一键脚本
GitHub520 项目也提供了跨平台自动更新脚本（Python/Shell），直接运行就行：
```bash
# Linux / macOS 一键更新
sudo bash -c "$(curl -fsSL https://raw.githubusercontent.com/521xueweihan/GitHub520/main/linux.sh)"
```
Windows 用户可以下载仓库里的 `.bat` 脚本以管理员身份运行。每次执行都会从 `hellogithub.com` 获取最新 hosts 并写入。你也可以把它添加到定时任务（crontab / 计划任务）里。

---

## 方案二：自己写 Python 脚本（灵活可控）

如果你更喜欢自己掌控，或者想练手，可以写一个简单的 Python 脚本。

### 核心思路
- 从一个**可靠且国内能访问的源**获取最新的 hosts 条目（比如 GitHub520 提供的 `raw.hellogithub.com/hosts`）。
- 解析其中的 GitHub 相关域名（如 `github.com`、`github.githubassets.com` 等）。
- 写入系统 hosts 文件（**先备份**，然后替换/追加这些条目）。

### Python 脚本示例（跨平台，需管理员权限运行）
```python
import os
import sys
import shutil
import requests
from datetime import datetime

# 配置
HOSTS_URL = "https://raw.hellogithub.com/hosts"   # GitHub520 镜像源
HOSTS_PATH = r"C:\Windows\System32\drivers\etc\hosts" if sys.platform == "win32" else "/etc/hosts"
BACKUP_PATH = HOSTS_PATH + ".bak"
MARKER_START = "# GitHub520 Host Start"
MARKER_END = "# GitHub520 Host End"

def get_remote_hosts():
    """获取远程 hosts 内容"""
    resp = requests.get(HOSTS_URL, timeout=10)
    resp.raise_for_status()
    return resp.text

def update_hosts(new_entries):
    """备份并替换本地 hosts 中的 GitHub520 区块"""
    # 1. 备份
    shutil.copy2(HOSTS_PATH, BACKUP_PATH)
    
    with open(HOSTS_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    # 2. 删除旧的 GitHub520 区块
    new_lines = []
    inside_block = False
    for line in lines:
        if MARKER_START in line:
            inside_block = True
            continue
        if MARKER_END in line:
            inside_block = False
            continue
        if not inside_block:
            new_lines.append(line)
    
    # 3. 追加新内容（确保末尾有换行）
    if new_lines and not new_lines[-1].endswith("\n"):
        new_lines.append("\n")
    
    new_lines.append(f"{MARKER_START}\n")
    new_lines.append(f"# Updated at {datetime.now()}\n")
    new_lines.append(new_entries + "\n")
    new_lines.append(f"{MARKER_END}\n")
    
    # 4. 写回
    with open(HOSTS_PATH, "w", encoding="utf-8") as f:
        f.writelines(new_lines)
    
    print("hosts 更新成功，备份：", BACKUP_PATH)

if __name__ == "__main__":
    # 检查管理员权限（简单提示）
    try:
        entries = get_remote_hosts()
        update_hosts(entries)
        print("建议刷新 DNS 缓存：ipconfig /flushdns 或 sudo dscacheutil -flushcache")
    except PermissionError:
        print("请以管理员/root 权限运行此脚本！")
        sys.exit(1)
    except Exception as e:
        print("出错：", e)
        sys.exit(1)
```

### 使用说明
1. 安装依赖：`pip install requests`
2. **Windows**：右键以管理员身份在终端运行 `python update_github_hosts.py`
3. **macOS / Linux**：`sudo python3 update_github_hosts.py`
4. 执行后刷新 DNS：
   - Windows: `ipconfig /flushdns`
   - macOS: `sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder`
   - Linux: `sudo systemctl restart systemd-resolved` 或 `sudo /etc/init.d/nscd restart`

### 如何定时自动执行
- **Windows**：创建“计划任务”，触发器每天/每小时，操作“启动程序”指向 Python 脚本。
- **Linux/macOS**：`crontab -e` 添加  
  `0 */2 * * * /usr/bin/python3 /path/to/script.py` （每2小时更新）

---

## 注意事项
- hosts 文件修改需要**管理员/root 权限**，否则会失败。
- 修改前脚本会自动备份为 `.bak`，出问题可以恢复。
- 如果使用了 VPN 或代理，代理可能干扰 requests 请求，可临时设置环境变量 `no_proxy`。
- GitHub520 的 hosts 列表也包含其他 GitHub 相关子域名，一站式解决，比自己查单个 IP 靠谱。

用方案一几乎零成本，方案二给了你完全自主的能力。根据自己的习惯选就行。