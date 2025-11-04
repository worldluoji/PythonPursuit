# multiprocessing
在 Python3 中，`multiprocessing` 模块用于实现真正的并行计算，通过创建多个进程来绕过全局解释器锁（GIL）的限制，尤其适合 **CPU 密集型任务**。以下是其核心概念、使用方法及实际场景的详细解析：

---

### **一、为什么需要多进程？**
- **GIL 的限制**：Python 的线程（`threading`）受 GIL 约束，同一时刻只能有一个线程执行字节码，无法利用多核 CPU。
- **多进程的优势**：
  - 每个进程有独立的 Python 解释器和内存空间，可真正并行执行任务。
  - 适用于计算密集型场景（如数值计算、图像处理）。

---

### **二、核心组件与用法**

#### 1. **`Process` 类：创建子进程**
- **基本流程**：
  1. 定义任务函数。
  2. 创建 `Process` 实例并启动。
  3. 等待子进程结束。

```python
from multiprocessing import Process
import os

def task(name):
    print(f"子进程 {name} (PID: {os.getpid()}) 执行")

if __name__ == "__main__":
    # 创建进程
    p = Process(target=task, args=("A",))
    p.start()  # 启动进程
    p.join()   # 等待进程结束
    print("主进程结束")
```

#### 2. **进程间通信（IPC）**
由于进程间内存隔离，需通过特定机制共享数据：

##### **`Queue`：安全队列**
```python
from multiprocessing import Process, Queue

def producer(q):
    q.put("数据")

def consumer(q):
    print(q.get())

if __name__ == "__main__":
    q = Queue()
    p1 = Process(target=producer, args=(q,))
    p2 = Process(target=consumer, args=(q,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
```

##### **`Pipe`：双向通道**
```python
from multiprocessing import Process, Pipe

def worker(conn):
    conn.send("消息")
    print(conn.recv())

if __name__ == "__main__":
    parent_conn, child_conn = Pipe()
    p = Process(target=worker, args=(child_conn,))
    p.start()
    print(parent_conn.recv())  # 输出 "消息"
    parent_conn.send("响应")
    p.join()
```

##### **共享内存（`Value`/`Array`）**
```python
from multiprocessing import Process, Value, Array

def increment(n):
    n.value += 1

if __name__ == "__main__":
    num = Value("i", 0)  # 整数类型
    procs = [Process(target=increment, args=(num,)) for _ in range(4)]
    for p in procs:
        p.start()
    for p in procs:
        p.join()
    print(num.value)  # 输出 4
```

#### 3. **进程池（`Pool`）**
管理多个工作进程，复用资源减少开销：
```python
from multiprocessing import Pool

def square(x):
    return x * x

if __name__ == "__main__":
    with Pool(4) as pool:  # 4个工作进程
        results = pool.map(square, [1, 2, 3, 4])
    print(results)  # 输出 [1, 4, 9, 16]
```

---

### **三、进程间数据共享的进阶方法**

#### 1. **`Manager`：托管共享对象**
通过 `Manager` 创建共享的复杂数据结构（如字典、列表）：
```python
from multiprocessing import Process, Manager

def update_dict(d, key, value):
    d[key] = value

if __name__ == "__main__":
    with Manager() as manager:
        shared_dict = manager.dict()
        procs = [Process(target=update_dict, args=(shared_dict, i, i*2)) for i in range(3)]
        for p in procs:
            p.start()
        for p in procs:
            p.join()
        print(shared_dict)  # 输出 {0: 0, 1: 2, 2: 4}
```

#### 2. **`shared_memory`（Python 3.8+）**
直接共享内存块，高性能但需手动同步：
```python
from multiprocessing import shared_memory

# 创建共享内存
shm = shared_memory.SharedMemory(create=True, size=1024)
# 写入数据
buffer = shm.buf
buffer[0:4] = b"data"
# 其他进程通过名称访问
other_shm = shared_memory.SharedMemory(name=shm.name)
```

---

### **四、多进程 vs 多线程**
| **特性**               | **多进程 (`multiprocessing`)**          | **多线程 (`threading`)**          |
|------------------------|----------------------------------------|----------------------------------|
| **内存隔离**            | 独立内存空间                          | 共享内存                        |
| **GIL 影响**           | 无影响                                | 受 GIL 限制                     |
| **适用场景**            | CPU 密集型任务（计算、数据处理）       | I/O 密集型任务（网络、文件读写） |
| **创建开销**            | 高（需复制内存）                      | 低                              |
| **数据共享难度**        | 需 IPC 机制                           | 可直接共享变量（需线程安全）     |

---

### **五、注意事项**
1. **跨平台兼容性**：
   - Windows 使用 `spawn` 启动方法（默认），需将主代码放在 `if __name__ == "__main__":` 下。
   - Unix 系统支持 `fork`（更快但有潜在隐患）。

2. **避免死锁**：
   - 确保所有进程正确调用 `join()` 或 `terminate()`。

3. **资源消耗**：
   - 进程数不应超过 CPU 核心数过多，否则导致调度开销上升。

4. **调试技巧**：
   - 使用 `logging` 模块替代 `print`，避免输出混乱。
   - 捕获子进程异常：
     ```python
     try:
         p.start()
     except Exception as e:
         print(f"进程启动失败: {e}")
     ```

---

### **六、实战示例：并行计算圆周率**
```python
from multiprocessing import Pool
import random

def monte_carlo(n):
    inside = 0
    for _ in range(n):
        x, y = random.random(), random.random()
        if x**2 + y**2 <= 1:
            inside += 1
    return inside

if __name__ == "__main__":
    total_samples = 10_000_000
    with Pool() as pool:
        results = pool.map(monte_carlo, [total_samples//4] * 4)
    pi = 4 * sum(results) / total_samples
    print(f"估算的圆周率: {pi}")
```

---

### **总结**
- **`multiprocessing` 核心价值**：突破 GIL 限制，实现真正并行。
- **适用场景**：CPU 密集型任务（如数值计算、机器学习训练）。
- **关键技巧**：
  - 使用 `Pool` 管理进程池。
  - 通过 `Queue`、`Pipe` 或共享内存实现进程通信。
  - 避免过度创建进程，合理利用 CPU 核心数。
