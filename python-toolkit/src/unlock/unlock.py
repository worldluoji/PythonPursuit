import pyautogui
import time
import threading
import random
from datetime import datetime

class EnhancedAntiLock:
    def __init__(self, interval=90, mode='auto'):
        """
        增强型防锁屏方案
        
        参数:
        interval: 基本间隔（秒）
        mode: 'mouse'=只移动鼠标/滚轮, 'keyboard'=只按键, 'auto'=自动选择
        """
        self.interval = interval
        self.mode = mode
        self.is_running = False
        self.thread = None
        
        # 定义一系列安全的动作
        self.actions = [
            self._move_mouse,
            self._scroll_wheel,
            self._press_function_key,
            self._press_modifier_function,
            self._double_scroll_lock,
            self._press_media_key  # 如果不需要媒体键可注释掉
        ]
        
    def _move_mouse(self):
        """鼠标移动：较大幅度移动并返回"""
        try:
            x, y = pyautogui.position()
            screen_w, screen_h = pyautogui.size()
            
            # 随机移动 10~30 像素
            dx = random.randint(10, 30) * random.choice([-1, 1])
            dy = random.randint(10, 30) * random.choice([-1, 1])
            new_x = max(0, min(screen_w-1, x + dx))
            new_y = max(0, min(screen_h-1, y + dy))
            
            pyautogui.moveTo(new_x, new_y, duration=0.2)
            time.sleep(0.1)
            pyautogui.moveTo(x, y, duration=0.2)
            return True
        except Exception as e:
            print(f"鼠标移动失败: {e}")
            return False
    
    def _scroll_wheel(self):
        """滚轮滚动：向上滚一下，再向下滚回来"""
        try:
            pyautogui.scroll(5)   # 向上滚动
            time.sleep(0.1)
            pyautogui.scroll(-5)  # 向下滚动
            return True
        except Exception as e:
            print(f"滚轮滚动失败: {e}")
            return False
    
    def _press_function_key(self):
        """按下功能键 F13~F24（通常无实际功能）"""
        try:
            f_key = f'f{random.randint(13, 24)}'
            pyautogui.press(f_key)
            return True
        except Exception as e:
            print(f"功能键失败: {e}")
            return False
    
    def _press_modifier_function(self):
        """按下修饰键 + 功能键（如 Ctrl+Shift+F13）"""
        try:
            modifiers = ['ctrl', 'shift', 'alt']
            # 随机选择1~2个修饰键
            chosen = random.sample(modifiers, random.randint(1, 2))
            f_key = f'f{random.randint(13, 24)}'
            
            # 按下所有修饰键
            for mod in chosen:
                pyautogui.keyDown(mod)
            pyautogui.press(f_key)
            # 释放所有修饰键
            for mod in chosen:
                pyautogui.keyUp(mod)
            return True
        except Exception as e:
            print(f"组合键失败: {e}")
            return False
    
    def _double_scroll_lock(self):
        """双击 Scroll Lock（恢复原状态）"""
        try:
            pyautogui.press('scrolllock')
            time.sleep(0.1)
            pyautogui.press('scrolllock')
            return True
        except Exception as e:
            print(f"Scroll Lock 失败: {e}")
            return False
    
    def _press_media_key(self):
        """媒体键（可选，可能会影响音量/媒体播放）"""
        try:
            keys = ['volumemute', 'volumeup', 'volumedown', 
                    'playpause', 'nexttrack', 'previoustrack']
            key = random.choice(keys)
            pyautogui.press(key)
            return True
        except Exception as e:
            print(f"媒体键失败: {e}")
            return False
    
    def _run(self):
        """主循环"""
        print(f"增强防锁屏已启动，模式: {self.mode}")
        
        while self.is_running:
            success = False
            action_name = ""
            
            if self.mode == 'mouse':
                # 鼠标模式下随机选择鼠标相关动作
                mouse_actions = [self._move_mouse, self._scroll_wheel]
                action = random.choice(mouse_actions)
                action_name = action.__name__
                success = action()
            elif self.mode == 'keyboard':
                # 键盘模式下随机选择键盘相关动作（不含鼠标）
                keyboard_actions = [self._press_function_key, 
                                    self._press_modifier_function,
                                    self._double_scroll_lock,
                                    self._press_media_key]
                action = random.choice(keyboard_actions)
                action_name = action.__name__
                success = action()
            else:  # auto模式
                action = random.choice(self.actions)
                action_name = action.__name__
                success = action()
            
            if success:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] 防锁屏成功 - {action_name}")
            else:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] 防锁屏失败 - {action_name}")
            
            # 随机化间隔，避免规律
            wait_time = self.interval + random.randint(-20, 20)
            wait_time = max(30, wait_time)  # 最小间隔30秒
            for _ in range(wait_time * 10):
                if not self.is_running:
                    break
                time.sleep(0.1)
    
    def start(self):
        """启动"""
        self.is_running = True
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()
    
    def stop(self):
        """停止"""
        self.is_running = False
        if self.thread:
            self.thread.join(timeout=2)
        print("已停止")

def main():
    anti_lock = EnhancedAntiLock(interval=90, mode='auto')
    
    try:
        anti_lock.start()
        
        print("\n" + "="*50)
        print("增强防锁屏控制")
        print("="*50)
        print("1. 鼠标模式 (移动+滚轮)")
        print("2. 键盘模式 (功能键/组合键)")
        print("3. 自动模式 (推荐)")
        print("q. 退出")
        print("="*50)
        
        while True:
            cmd = input("选择模式 (1/2/3/q): ").strip().lower()
            
            if cmd == '1':
                anti_lock.mode = 'mouse'
                print("已切换到鼠标模式")
            elif cmd == '2':
                anti_lock.mode = 'keyboard'
                print("已切换到键盘模式")
            elif cmd == '3':
                anti_lock.mode = 'auto'
                print("已切换到自动模式")
            elif cmd == 'q':
                break
            else:
                print("无效输入")
                
    except KeyboardInterrupt:
        print("\n正在停止...")
    finally:
        anti_lock.stop()

if __name__ == "__main__":
    # 安装依赖: pip install pyautogui
    main()