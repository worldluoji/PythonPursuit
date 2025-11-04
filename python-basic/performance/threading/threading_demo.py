import time
import threading

# 由于GIL的存在，CPU密集型任务在Python多线程中可能无法获得性能提升​

def cpu_intensive_task(n):
    """模拟CPU密集型任务"""
    result = 0
    for i in range(n):
        result += i * i
    return result

# 单线程执行
start_time = time.time()
results = [cpu_intensive_task(10**7) for _ in range(4)]
single_thread_time = time.time() - start_time


def threaded_execution():
    threads = []
    results = [0] * 4
    def task_wrapper(index, n):
        results[index] = cpu_intensive_task(n)

    start_time = time.time()
    for i in range(4):
        thread = threading.Thread(target=task_wrapper, args=(i, 10**7))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return time.time() - start_time, results


multi_thread_time, multi_results = threaded_execution()

print(f"单线程执行时间: {single_thread_time:.2f}秒")
print(f"多线程执行时间: {multi_thread_time:.2f}秒")
print(f"性能提升: {single_thread_time/multi_thread_time:.2f}x")

