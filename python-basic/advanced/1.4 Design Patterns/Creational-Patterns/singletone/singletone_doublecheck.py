import threading

class Singleton:
    _instance = None
    _lock = threading.Lock() # threading.Lock() 是 Python 标准库中提供的一个线程同步原语，用于实现线程间的互斥锁机制。

    def __new__(cls):
        if not cls._instance:  # 第一次检查（无锁）, 避免了当单例实例已经存在时不必要的同步开销
            with cls._lock:
                if not cls._instance:  # 第二次检查（持锁状态）,确保只有一个线程能够创建实例, 可能别的线程创建完，锁已经释放了，这时候再进来如果不再判断就会重复创建
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