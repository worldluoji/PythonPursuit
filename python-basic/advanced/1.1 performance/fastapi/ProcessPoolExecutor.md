# ProcessPoolExecutor
选择 ProcessPoolExecutor​ 来处理纯粹的CPU密集型任务，是理论指导下的最佳实践。这确保了繁重的计算不会阻塞您的主事件循环，从而保障了API整体的响应能力。

在FastAPI中使用ProcessPoolExecutor需要**避免在每个请求中创建新实例**，而应通过**lifespan管理单例进程池**，以确保高效执行CPU密集型任务并防止资源耗尽。

## 1. 正确使用方法

### 1.1 使用lifespan管理进程池生命周期

**最佳实践**是利用FastAPI的lifespan机制管理进程池，确保进程池在应用启动时创建、运行时复用、关闭时销毁：

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
import concurrent.futures
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 根据CPU核心数设置工作进程数（通常为CPU核心数）
    nworkers = os.cpu_count() or 4
    # 创建进程池
    app.state.executor = concurrent.futures.ProcessPoolExecutor(
        max_workers=nworkers
    )
    yield
    # 关闭进程池
    app.state.executor.shutdown()

app = FastAPI(lifespan=lifespan)
```

这种管理方式确保了：
- **进程池作为单例资源**在整个应用生命周期中复用
- **避免重复创建进程**带来的高开销（进程创建比线程创建开销大得多）
- **应用关闭时正确清理**资源，防止资源泄漏

### 1.2 在路由中使用进程池

在路由函数中，通过`asyncio.run_in_executor`将CPU密集型任务提交到进程池：

```python
import asyncio
from fastapi import FastAPI

@app.get("/cpu-intensive-task")
async def cpu_intensive_task():
    # 定义CPU密集型任务
    def heavy_calculation(n):
        return sum(i * i for i in range(n))
    
    # 将任务提交到进程池
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        app.state.executor, 
        heavy_calculation, 
        10_000_000
    )
    return {"result": result}
```

这种方式**不会阻塞主事件循环**，保持了FastAPI的异步特性。

## 2. 常见错误与解决方案

### 2.1 错误：在每个请求中创建新进程池

```python
@app.get("/bad-example")
async def bad_example():
    # 错误！在每个请求中创建新进程池
    with concurrent.futures.ProcessPoolExecutor() as executor:
        # ...执行任务...
```

**问题**：
- 每次请求都会创建新的进程，导致**高资源开销**（进程创建比函数调用慢得多）
- 在高并发场景下（如每秒30-100个请求），系统资源会**迅速耗尽**
- **完全违背了"池"的设计初衷**，失去了复用进程的优势

**解决方案**：使用lifespan管理单例进程池（如上所示）

### 2.2 错误：未正确处理异常

```python
@app.get("/error-prone-task")
async def error_prone_task():
    try:
        result = await asyncio.get_event_loop().run_in_executor(
            app.state.executor, faulty_function
        )
    except Exception as e:
        # 仅捕获异常但不处理
        return {"error": str(e)}
```

**问题**：未区分不同类型的异常，可能导致**任务失败但进程池无法恢复**

**解决方案**：实现**健壮的异常处理机制**，包括重试逻辑和错误记录

## 3. 性能优化建议

### 3.1 合理设置max_workers

- **CPU密集型任务**：`max_workers`应接近CPU核心数（通常为`os.cpu_count()`）
- **混合型任务**：可适当增加（如`os.cpu_count() * 2`），但需监控性能
- **避免过高值**：超过CPU核心数的进程会导致**上下文切换开销**增加

### 3.2 任务分割策略

对于大型CPU密集型任务，可采用**分块处理**策略：

```python
def process_large_data(data):
    # 将大数据分割为小块
    chunks = [data[i:i+1000] for i in range(0, len(data), 1000)]
    # 并行处理各块
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(process_chunk, chunks))
    # 合并结果
    return combine_results(results)
```

这种方式能**更好地利用多核CPU**，避免单个任务占用过多资源

### 3.3 避免数据传输开销

- **减少进程间数据传输**：避免传递大型对象（如几GB的数组）
- **使用共享内存**：对于需要共享的数据，可使用`multiprocessing.Array`或`numpy.memmap`
- **序列化优化**：确保传递的数据可高效序列化

## 4. 适用场景与替代方案

### 4.1 适用场景

ProcessPoolExecutor特别适合以下场景：
- **CPU密集型任务**：如数学计算、图像处理、加密解密
- **需要突破GIL限制**的任务：Python的全局解释器锁(GIL)会限制多线程并行
- **长时间运行的计算任务**：可避免阻塞主事件循环

### 4.2 替代方案

根据任务特性，可考虑以下替代方案：
- **I/O密集型任务**：使用`ThreadPoolExecutor`（更轻量，线程切换开销小）
- **超大规模任务**：考虑使用**分布式任务队列系统**（如Celery）
- **需要持久化和重试**：专业任务队列系统提供更完善的错误恢复机制

## 5. 完整示例

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
import concurrent.futures
import os
import asyncio
import re

@asynccontextmanager
async def lifespan(app: FastAPI):
    nworkers = os.cpu_count() or 4
    app.state.executor = concurrent.futures.ProcessPoolExecutor(
        max_workers=nworkers
    )
    yield
    app.state.executor.shutdown()

app = FastAPI(lifespan=lifespan)

# 示例：在内容块上运行正则表达式（CPU密集型）
def run_regex_on_content_chunk(content: str):
    domains = []
    domain_patt = re.compile(r'([a-zA-Z0-9\-_]+\.){1,}[a-zA-Z0-9\-_]+')
    for match in domain_patt.finditer(content):
        domains.append(match.group(0))
    return domains

@app.post("/process-content")
async def process_content(content: str):
    # 将内容分割为块
    chunks = [content[i:i+1000] for i in range(0, len(content), 1000)]
    # 并行处理各块
    loop = asyncio.get_event_loop()
    tasks = [
        loop.run_in_executor(app.state.executor, run_regex_on_content_chunk, chunk)
        for chunk in chunks
    ]
    results = await asyncio.gather(*tasks)
    # 合并结果
    return {"domains": [domain for sublist in results for domain in sublist]}
```

此示例展示了如何在FastAPI中**高效管理进程池**，处理CPU密集型任务，同时保持应用的**响应性和可扩展性**。通过遵循这些最佳实践，可以显著提升FastAPI应用在处理计算密集型任务时的性能和稳定性。