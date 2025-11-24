#!/usr/bin/env python3
"""
增强版自动打开工具：支持文件、网站和软件应用
"""

import os
import webbrowser
import configparser
import platform
import subprocess
import time
from pathlib import Path
from typing import List, Dict, Any, Optional

class EnhancedFileOpener:
    def __init__(self, config_file: str = "config.ini"):
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        self.system = platform.system().lower()
        self.is_windows = self.system == "windows"
        self.is_macos = self.system == "darwin"
        self.is_linux = self.system == "linux"
        
        # 设置默认配置
        self.config['files'] = {}
        self.config['websites'] = {}
        self.config['software'] = {}
        self.config['settings'] = {
            'open_delay': '1',
            'confirm_before_open': 'False',
            'software_timeout': '10'
        }
        
        # 常用软件路径映射（跨平台支持）
        self.software_aliases = {
            'notepad': 'notepad.exe' if self.is_windows else 'gedit' if self.is_linux else 'TextEdit',
            'calculator': 'calc.exe' if self.is_windows else 'gnome-calculator' if self.is_linux else 'Calculator',
            'browser': 'msedge.exe' if self.is_windows else 'firefox' if self.is_linux else 'Safari',
            'texteditor': 'notepad.exe' if self.is_windows else 'nano' if self.is_linux else 'TextEdit',
        }
    
    def load_config(self) -> bool:
        """加载配置文件"""
        if not os.path.exists(self.config_file):
            print(f"❌ 配置文件 {self.config_file} 不存在，将创建默认配置")
            self.save_config()
            return False
        
        try:
            self.config.read(self.config_file, encoding='utf-8')
            print("✅ 配置文件加载成功")
            return True
        except Exception as e:
            print(f"❌ 配置文件加载失败: {e}")
            return False
    
    def save_config(self) -> None:
        """保存配置文件"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                self.config.write(f)
            print(f"✅ 默认配置文件已保存: {self.config_file}")
        except Exception as e:
            print(f"❌ 配置文件保存失败: {e}")
    
    def find_software_path(self, software_name: str) -> Optional[str]:
        """查找软件的可执行文件路径"""
        # 如果是完整路径且存在，直接返回
        if os.path.exists(software_name):
            return software_name
        
        # 处理带引号的路径
        if software_name.startswith('"') and software_name.endswith('"'):
            path = software_name[1:-1]
            if os.path.exists(path):
                return path
        
        # 检查别名映射
        if software_name in self.software_aliases:
            software_name = self.software_aliases[software_name]
        
        # 在系统PATH中查找
        if self.is_windows:
            # Windows: 检查常见安装目录
            common_paths = [
                os.path.join(os.environ.get('ProgramFiles', 'C:\\Program Files'), software_name),
                os.path.join(os.environ.get('ProgramFiles(x86)', 'C:\\Program Files (x86)'), software_name),
                os.path.join(os.environ.get('SystemRoot', 'C:\\Windows'), 'System32', software_name),
            ]
            
            # 添加.exe扩展名如果还没有的话
            if not software_name.lower().endswith(('.exe', '.com', '.bat')):
                software_name_exe = software_name + '.exe'
                common_paths.insert(0, software_name_exe)
            
            for path in common_paths:
                if os.path.exists(path):
                    return path
        else:
            # Unix-like 系统：使用 which 命令查找
            try:
                result = subprocess.run(['which', software_name], 
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    return result.stdout.strip()
            except:
                pass
        
        return None
    
    def open_software(self, software_spec: str) -> bool:
        """打开软件应用"""
        try:
            # 查找软件路径
            software_path = self.find_software_path(software_spec)
            
            if not software_path:
                print(f"❌ 找不到软件: {software_spec}")
                return False
            
            print(f"🔧 正在启动软件: {software_spec}")
            
            if self.is_windows:
                # Windows系统
                if software_path.endswith('.exe'):
                    subprocess.Popen([software_path], shell=True)
                else:
                    os.startfile(software_path)
            elif self.is_macos:
                # macOS系统
                if software_path.endswith('.app'):
                    subprocess.Popen(['open', '-a', software_path])
                else:
                    subprocess.Popen([software_path])
            else:
                # Linux系统
                subprocess.Popen([software_path])
            
            print(f"✅ 已启动软件: {software_spec}")
            return True
            
        except Exception as e:
            print(f"❌ 启动软件失败 {software_spec}: {e}")
            return False
    
    def open_file(self, file_path: str) -> bool:
        """打开文件"""
        try:
            if file_path.startswith(('http://', 'https://')):
                return self.open_website(file_path)
            
            path_obj = Path(file_path)
            if not path_obj.exists():
                # 尝试当前目录下的相对路径
                path_obj = Path.cwd() / file_path
                if not path_obj.exists():
                    print(f"❌ 文件不存在: {file_path}")
                    return False
            
            if self.is_windows:
                os.startfile(str(path_obj))
            elif self.is_macos:
                subprocess.Popen(['open', str(path_obj)])
            else:
                subprocess.Popen(['xdg-open', str(path_obj)])
            
            print(f"✅ 已打开文件: {file_path}")
            return True
        except Exception as e:
            print(f"❌ 打开文件失败 {file_path}: {e}")
            return False
    
    def open_website(self, url: str) -> bool:
        """打开网站"""
        try:
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            webbrowser.open(url)
            print(f"🌐 已打开网站: {url}")
            return True
        except Exception as e:
            print(f"❌ 打开网站失败 {url}: {e}")
            return False
    
    def get_open_delay(self) -> int:
        """获取打开延迟时间"""
        try:
            return int(self.config.get('settings', 'open_delay', fallback=1))
        except:
            return 1
    
    def get_software_timeout(self) -> int:
        """获取软件启动超时时间"""
        try:
            return int(self.config.get('settings', 'software_timeout', fallback=10))
        except:
            return 10
    
    def get_confirm_setting(self) -> bool:
        """获取确认设置"""
        try:
            return self.config.getboolean('settings', 'confirm_before_open', fallback=False)
        except:
            return False
    
    def display_category_menu(self, items: Dict[str, str], title: str) -> List[str]:
        """显示分类菜单并返回选择项"""
        if not items:
            print(f"⚠️  {title}配置为空")
            return []
        
        print(f"\n{'='*50}")
        print(f"📁 {title}")
        print(f"{'='*50}")
        
        items_list = list(items.items())
        for i, (key, value) in enumerate(items_list, 1):
            status = "✅" if self.validate_item(value, title) else "❌"
            print(f"{i:2d}. {status} {key}: {value}")
        
        print(f"{len(items_list)+1:2d}. 打开全部有效项")
        print(f"{len(items_list)+2:2d}. 打开全部（包括可能无效的）")
        print(f" 0. 跳过")
        
        while True:
            try:
                choice = input(f"\n请选择要打开的{title} (多个选择用逗号分隔): ").strip()
                if choice == '0':
                    return []
                
                if choice == str(len(items_list)+1):  # 打开全部有效项
                    return [item[1] for item in items_list if self.validate_item(item[1], title)]
                
                if choice == str(len(items_list)+2):  # 打开全部
                    return [item[1] for item in items_list]
                
                choices = [int(x.strip()) for x in choice.split(',') if x.strip()]
                selected = []
                for c in choices:
                    if 1 <= c <= len(items_list):
                        selected.append(items_list[c-1][1])
                    else:
                        print(f"⚠️  无效选择: {c}")
                
                return selected
            except ValueError:
                print("❌ 请输入有效的数字")
            except KeyboardInterrupt:
                print("\n👋 用户中断操作")
                return []
    
    def validate_item(self, item: str, category: str) -> bool:
        """验证项目是否有效"""
        if category == "文件":
            path_obj = Path(item)
            return path_obj.exists() or (Path.cwd() / item).exists()
        elif category == "软件":
            return self.find_software_path(item) is not None
        elif category == "网站":
            return item.startswith(('http://', 'https://')) or '.' in item
        return True
    
    def run(self) -> None:
        """运行主程序"""
        print("🚀 增强版打开工具 - 支持文件、网站和软件")
        print("="*50)
        print(f"💻 操作系统: {platform.system()} {platform.release()}")
        
        # 加载配置
        if not self.load_config():
            print("请先编辑配置文件，然后重新运行程序")
            return
        
        # 获取配置项
        files = dict(self.config.items('files'))
        websites = dict(self.config.items('websites'))
        software = dict(self.config.items('software'))
        open_delay = self.get_open_delay()
        need_confirm = self.get_confirm_setting()
        
        if not files and not websites and not software:
            print("⚠️  配置文件中没有配置任何项目")
            return
        
        try:
            # 选择要打开的项目
            selected_files = self.display_category_menu(files, "文件")
            selected_websites = self.display_category_menu(websites, "网站") 
            selected_software = self.display_category_menu(software, "软件")
            
            # 合并所有选择
            all_selected = []
            all_selected.extend((path, 'file') for path in selected_files)
            all_selected.extend((url, 'website') for url in selected_websites)
            all_selected.extend((soft, 'software') for soft in selected_software)
            
            # 确认打开
            if need_confirm and all_selected:
                print(f"\n即将打开 {len(all_selected)} 个项目:")
                for item, item_type in all_selected:
                    type_icon = "📄" if item_type == 'file' else "🌐" if item_type == 'website' else "🔧"
                    print(f"  {type_icon} {item}")
                
                confirm = input(f"\n确定要打开吗? (y/N): ")
                if confirm.lower() != 'y':
                    print("操作已取消")
                    return
            
            # 打开选中的项目
            total_opened = 0
            
            for item, item_type in all_selected:
                success = False
                if item_type == 'file':
                    success = self.open_file(item)
                elif item_type == 'website':
                    success = self.open_website(item)
                elif item_type == 'software':
                    success = self.open_software(item)
                
                if success:
                    total_opened += 1
                
                if open_delay > 0 and len(all_selected) > 1:
                    time.sleep(open_delay)
            
            print(f"\n✅ 完成! 共成功打开 {total_opened} 个项目")
            
        except KeyboardInterrupt:
            print("\n\n👋 程序被用户中断")
        except Exception as e:
            print(f"\n❌ 程序运行出错: {e}")

def main():
    """主函数"""
    opener = EnhancedFileOpener()
    opener.run()

if __name__ == "__main__":
    main()