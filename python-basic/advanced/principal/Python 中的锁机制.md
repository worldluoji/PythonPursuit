# Python 中的锁机制

Python 提供了多种锁机制用于线程同步，主要位于 `threading` 模块中。以下是主要的锁类型：

## 1. 互斥锁 (Lock)
最基本的锁，一次只允许一个线程访问共享资源。

```python
import threading

lock = threading.Lock()
counter = 0

def increment():
    global counter
    with lock:  # 自动获取和释放锁
        counter += 1
```

## 2. 可重入锁 (RLock)
允许同一个线程多次获取同一个锁，避免死锁。

```python
rlock = threading.RLock()

def recursive_function(count):
    with rlock:
        if count > 0:
            recursive_function(count - 1)
```

## 3. 信号量 (Semaphore)
控制同时访问资源的线程数量。

```python
semaphore = threading.Semaphore(3)  # 允许3个线程同时访问

def access_resource():
    with semaphore:
        # 访问受保护的资源
        pass
```

## 4. 有界信号量 (BoundedSemaphore)
与信号量类似，但确保计数值不会超过初始值。

```python
bounded_sem = threading.BoundedSemaphore(3)
```

## 5. 事件 (Event)
用于线程间的简单通信，一个线程发出事件信号，其他线程等待该事件。

```python
event = threading.Event()

def waiter():
    event.wait()  # 等待事件
    # 事件发生后执行

def setter():
    # 做一些工作后设置事件
    event.set()
```

## 6. 条件变量 (Condition)
用于复杂的线程同步，允许线程等待特定条件成立。

```python
condition = threading.Condition()
items = []

def consumer():
    with condition:
        while not items:
            condition.wait()  # 等待条件满足
        items.pop()

def producer():
    with condition:
        items.append("item")
        condition.notify()  # 通知等待的线程
```

## 7. 屏障 (Barrier)
让多个线程等待，直到所有线程都到达某个点后再继续执行。

```python
barrier = threading.Barrier(3)  # 等待3个线程

def worker():
    # 执行一些工作
    barrier.wait()  # 等待所有线程到达
    # 继续执行后续工作
```

## 使用建议

1. 优先使用 `with` 语句管理锁，确保锁的正确释放
2. 尽量避免嵌套锁，防止死锁
3. 使用超时机制避免永久阻塞：`lock.acquire(timeout=5)`
4. 对于简单的计数器保护，考虑使用 `threading.Local()` 存储线程本地数据

这些锁机制为Python多线程编程提供了灵活的同步选项，应根据具体场景选择合适的同步原语。