import asyncio
import time

async def fetch_data(delay, id):
    """模拟网络请求"""
    print(f"🚀 开始获取数据 {id}")
    await asyncio.sleep(delay)  # 模拟I/O等待
    print(f"✅ 数据 {id} 获取完成")
    return f"data_{id}"

async def run_liner():
    # 传统顺序执行
    start_time = time.time()
    
    # 顺序执行 - 这会很慢！
    result1 = await fetch_data(2, 1)
    result2 = await fetch_data(2, 2)

    elapsed_time = time.time() - start_time
    
    print(f"📊 总执行时间: {elapsed_time:.2f}秒")
    print(result1, result2)
    return elapsed_time

async def run_async_demo():
    print("=== 异步编程演示 ===")
    start_time = time.time()
    
    # 并发执行 - 这才是正确方式！
    task1 = asyncio.create_task(fetch_data(2, 1))
    task2 = asyncio.create_task(fetch_data(2, 2))
    
    results = await asyncio.gather(task1, task2)
    elapsed_time = time.time() - start_time
    
    print(f"📊 总执行时间: {elapsed_time:.2f}秒")
    print(f"🎯 最终结果: {results}")
    return elapsed_time

async def main():
    single_thread_time = await run_liner()
    multi_coroutine_time = await run_async_demo()
    print(f"性能提升: {single_thread_time/multi_coroutine_time:.2f}x")

asyncio.run(main())
