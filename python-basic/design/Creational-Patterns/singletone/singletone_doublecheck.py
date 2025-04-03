import threading

class Singleton:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if not cls._instance:  # 第一次检查（无锁）
            with cls._lock:
                if not cls._instance:  # 第二次检查（持锁状态）
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