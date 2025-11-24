#!/usr/bin/env python3
"""
增强版一键打开脚本：一键打开配置中的所有文件、网站和软件
"""

import time
from file_opener import EnhancedFileOpener

def quick_open_all():
    """一键打开所有配置项"""
    opener = EnhancedFileOpener()
    
    if not opener.load_config():
        print("❌ 配置文件加载失败，请检查配置文件")
        return
    
    # 获取所有配置项
    files = dict(opener.config.items('files'))
    websites = dict(opener.config.items('websites'))
    software = dict(opener.config.items('software'))
    open_delay = opener.get_open_delay()
    
    if not files and not websites and not software:
        print("⚠️ 配置文件中没有配置任何项目")
        return
    
    print("🚀 开始一键打开所有配置项...")
    print("=" * 50)
    
    total_count = len(files) + len(websites) + len(software)
    print(f"📊 总计: {len(files)} 个文件, {len(websites)} 个网站, {len(software)} 个软件")
    print(f"⏱️  打开间隔: {open_delay} 秒")
    print("=" * 50)
    
    # 确认操作
    confirm = input("确定要一键打开所有项目吗? (y/N): ")
    if confirm.lower() != 'y':
        print("操作已取消")
        return
    
    total_opened = 0
    failed_items = []
    
    try:
        # 1. 先打开所有软件（通常启动较慢）
        if software:
            print("\n🔧 正在打开软件应用...")
            for name, soft_path in software.items():
                print(f"  启动: {name} -> {soft_path}")
                if opener.open_software(soft_path):
                    total_opened += 1
                else:
                    failed_items.append(("软件", name, soft_path))
                
                if open_delay > 0:
                    time.sleep(open_delay)
        
        # 2. 打开所有文件
        if files:
            print("\n📄 正在打开文件...")
            for name, file_path in files.items():
                print(f"  打开: {name} -> {file_path}")
                if opener.open_file(file_path):
                    total_opened += 1
                else:
                    failed_items.append(("文件", name, file_path))
                
                if open_delay > 0:
                    time.sleep(open_delay)
        
        # 3. 最后打开网站（通常最快）
        if websites:
            print("\n🌐 正在打开网站...")
            for name, url in websites.items():
                print(f"  访问: {name} -> {url}")
                if opener.open_website(url):
                    total_opened += 1
                else:
                    failed_items.append(("网站", name, url))
                
                if open_delay > 0:
                    time.sleep(open_delay)
        
        # 显示结果统计
        print("\n" + "=" * 50)
        print("✅ 一键打开完成!")
        print(f"📊 成功打开: {total_opened}/{total_count} 个项目")
        
        if failed_items:
            print(f"❌ 失败项目: {len(failed_items)} 个")
            for item_type, name, path in failed_items:
                print(f"  - {item_type}: {name} -> {path}")
        
        # 如果有软件被打开，提示用户可能需要等待完全启动
        if software and total_opened > 0:
            print("\n💡 提示: 软件应用可能需要一些时间才能完全启动")
            
    except KeyboardInterrupt:
        print("\n\n👋 程序被用户中断")
        print(f"已成功打开 {total_opened} 个项目")
    except Exception as e:
        print(f"\n❌ 程序运行出错: {e}")

def quick_open_selective():
    """选择性一键打开：按类别选择"""
    opener = EnhancedFileOpener()
    
    if not opener.load_config():
        print("❌ 配置文件加载失败，请检查配置文件")
        return
    
    # 获取所有配置项
    files = dict(opener.config.items('files'))
    websites = dict(opener.config.items('websites'))
    software = dict(opener.config.items('software'))
    open_delay = opener.get_open_delay()
    
    if not files and not websites and not software:
        print("⚠️ 配置文件中没有配置任何项目")
        return
    
    print("🚀 选择性一键打开")
    print("=" * 50)
    
    # 让用户选择要打开的类别
    selections = []
    
    if files:
        choice = input(f"是否打开所有 {len(files)} 个文件? (y/N): ")
        if choice.lower() == 'y':
            selections.extend([(path, 'file') for path in files.values()])
    
    if websites:
        choice = input(f"是否打开所有 {len(websites)} 个网站? (y/N): ")
        if choice.lower() == 'y':
            selections.extend([(url, 'website') for url in websites.values()])
    
    if software:
        choice = input(f"是否打开所有 {len(software)} 个软件? (y/N): ")
        if choice.lower() == 'y':
            selections.extend([(soft, 'software') for soft in software.values()])
    
    if not selections:
        print("❌ 未选择任何项目")
        return
    
    print(f"\n📊 即将打开 {len(selections)} 个项目")
    confirm = input("确定要继续吗? (y/N): ")
    if confirm.lower() != 'y':
        print("操作已取消")
        return
    
    total_opened = 0
    failed_items = []
    
    try:
        for item, item_type in selections:
            success = False
            
            if item_type == 'file':
                success = opener.open_file(item)
            elif item_type == 'website':
                success = opener.open_website(item)
            elif item_type == 'software':
                success = opener.open_software(item)
            
            if success:
                total_opened += 1
                print(f"✅ 成功打开: {item}")
            else:
                failed_items.append((item_type, item))
                print(f"❌ 打开失败: {item}")
            
            if open_delay > 0 and len(selections) > 1:
                time.sleep(open_delay)
        
        # 显示结果
        print("\n" + "=" * 50)
        print(f"✅ 完成! 成功打开 {total_opened}/{len(selections)} 个项目")
        
        if failed_items:
            print(f"❌ 失败项目: {len(failed_items)} 个")
            for item_type, item in failed_items:
                print(f"  - {item_type}: {item}")
                
    except KeyboardInterrupt:
        print("\n\n👋 程序被用户中断")
        print(f"已成功打开 {total_opened} 个项目")
    except Exception as e:
        print(f"\n❌ 程序运行出错: {e}")

def show_menu():
    """显示菜单"""
    print("🚀 增强版一键打开工具")
    print("=" * 50)
    print("1. 一键打开所有配置项")
    print("2. 选择性一键打开（按类别）")
    print("3. 使用交互式选择模式")
    print("0. 退出")
    print("=" * 50)

def main():
    """主函数"""
    while True:
        show_menu()
        choice = input("请选择操作 (0-3): ").strip()
        
        if choice == "1":
            quick_open_all()
        elif choice == "2":
            quick_open_selective()
        elif choice == "3":
            # 使用原来的交互式模式
            opener = EnhancedFileOpener()
            opener.run()
        elif choice == "0":
            print("👋 再见!")
            break
        else:
            print("❌ 无效选择，请重新输入")
        
        # 询问是否继续
        if choice != "0":
            continue_choice = input("\n是否继续使用工具? (y/N): ")
            if continue_choice.lower() != 'y':
                print("👋 再见!")
                break
        print()

if __name__ == "__main__":
    main()