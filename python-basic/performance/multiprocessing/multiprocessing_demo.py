import multiprocessing
import math
import time

def calculate_primes(n):
    """计算前n个质数 - CPU密集型任务"""
    primes = []
    num = 2
    while len(primes) < n:
        if all(num % i != 0 for i in range(2, int(math.sqrt(num)) + 1)):
            primes.append(num)
        num += 1
    return primes

def run_multiprocess_demo():
    start_time = time.time()
    
    with multiprocessing.Pool(processes=4) as pool:
        results = pool.map(calculate_primes, [10000, 10000, 10000, 10000])
    
    multiprocess_time = time.time() - start_time
    
    # 对比单进程
    start_time = time.time()
    single_results = [calculate_primes(10000) for _ in range(4)]
    single_process_time = time.time() - start_time
    
    print(f"🔄 多进程时间: {multiprocess_time:.2f}秒")
    print(f"🔢 单进程时间: {single_process_time:.2f}秒")
    print(f"⚡ 性能提升: {single_process_time/multiprocess_time:.2f}x")


if __name__ == '__main__':
    run_multiprocess_demo()