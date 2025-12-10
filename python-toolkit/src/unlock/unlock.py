import pyautogui
import time
import threading
import random
from datetime import datetime

class AdvancedAntiLock:
    def __init__(self, interval=90, mode='auto'):
        """
        高级防锁屏方案
        
        参数:
        interval: 基本间隔（秒）
        mode: 'mouse'=只移动鼠标, 'keyboard'=只按键, 'auto'=自动选择
        """
        self.interval = interval
        self.mode = mode
        self.is_running = False
        self.thread = None
        self.last_method = None
        
    def _mouse_method(self):
        """鼠标方案"""
        try:
            current_x, current_y = pyautogui.position()
            screen_width, screen_height = pyautogui.size()
            
            # 轻微移动鼠标
            move_x = current_x + random.choice([-1, 0, 1])
            move_y = current_y + random.choice([-1, 0, 1])
            
            # 确保不超出屏幕
            move_x = max(0, min(screen_width - 1, move_x))
            move_y = max(0, min(screen_height - 1, move_y))
            
            pyautogui.moveTo(move_x, move_y, duration=0.05)
            time.sleep(0.05)
            pyautogui.moveTo(current_x, current_y, duration=0.05)
            
            return True
        except:
            return False
    
    def _keyboard_method(self):
        """键盘方案"""
        try:
            # 使用不常用的组合键
            keys_to_press = [
                lambda: pyautogui.press('volumemute'),  # 静音键（通常无害）
                lambda: (pyautogui.keyDown('shift'), pyautogui.press('f13'), pyautogui.keyUp('shift')),
                lambda: (pyautogui.keyDown('ctrl'), pyautogui.keyDown('shift'), 
                        pyautogui.press('f12'), pyautogui.keyUp('shift'), pyautogui.keyUp('ctrl'))
            ]
            
            random.choice(keys_to_press)()
            return True
        except:
            return False
    
    def _run(self):
        """主循环"""
        print(f"高级防锁屏已启动，模式: {self.mode}")
        
        while self.is_running:
            success = False
            
            if self.mode == 'mouse':
                success = self._mouse_method()
            elif self.mode == 'keyboard':
                success = self._keyboard_method()
            else:  # auto模式
                # 随机选择方法
                if random.random() > 0.5:
                    success = self._mouse_method()
                    if not success:
                        success = self._keyboard_method()
                else:
                    success = self._keyboard_method()
                    if not success:
                        success = self._mouse_method()
            
            if success:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] 防锁屏操作成功")
            else:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] 防锁屏操作失败")
            
            # 随机化间隔时间，避免被检测
            wait_time = self.interval + random.randint(-20, 20)
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

def main_advanced():
    anti_lock = AdvancedAntiLock(interval=90, mode='auto')
    
    try:
        anti_lock.start()
        
        # 显示控制菜单
        print("\n" + "="*50)
        print("高级防锁屏控制")
        print("="*50)
        print("1. 鼠标模式 (最不影响工作)")
        print("2. 键盘模式 (无鼠标干扰)")
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
    main_advanced()