import threading
import time

class Singleton:
    _instance = None
    _lock = threading.Lock()  # 添加锁

    def __new__(cls):
        with cls._lock:  # 确保原子性
            if not cls._instance:
                # 模拟耗时操作，放大竞态窗口
                time.sleep(0.001)  # 关键点：让线程在此处切换
                cls._instance = super().__new__(cls)
        return cls._instance
    

def create_singleton():
    obj = Singleton()
    print(f"实例ID: {id(obj)}") # 不同线程可能打印不同的实例ID，证明单例失效。

# 启动10个线程并发创建实例
threads = []
for _ in range(10):
    t = threading.Thread(target=create_singleton)
    threads.append(t)
    t.start()

for t in threads:
    t.join()