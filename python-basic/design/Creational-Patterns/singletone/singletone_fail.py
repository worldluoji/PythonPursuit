import threading
import time

class Singleton:
    _instance = None

    def __new__(cls):
        # 线程A和线程B同时执行到 if not cls._instance，此时 _instance 为 None，两者均通过条件检查。两个线程都会执行 cls._instance = super().__new__(cls)，导致创建多个实例。
        if not cls._instance: # 竞态条件发生点
            # 模拟耗时操作，放大竞态窗口
            time.sleep(0.001)  # 关键点：让线程在此处切换
            cls._instance = super().__new__(cls) # 非原子操作
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