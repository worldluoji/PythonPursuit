
from multiprocessing import Pool,Queue
import os

'''
queue 和 pids 为空的原因在于 ​子进程无法直接共享主进程创建的 multiprocessing.Queue。以下是详细分析：

​问题原因
​进程间内存隔离：
multiprocessing.Queue 必须通过特殊机制共享。直接在主进程创建 Queue 后，子进程无法自动访问它。

​Pool 的初始化限制：
使用 Pool 创建子进程时，默认不会将主进程的 Queue 传递给子进程，导致子进程中的 queue 是独立的副本。
'''


# 定义一个队列用于存储进程id
queue = Queue()

# 用于计算平方和将运行函数的进程id写入队列
def f(x):
    queue.put(os.getpid())
    return x * x

if __name__ == '__main__':
    # 逻辑cpu个数
    count = os.cpu_count()
    print(f'My Computer CPU Number is {count}')

    with Pool(count * 2) as p:
        # 并行计算
        res = p.map(f, range(1, 101))
        print(f'计算平方的结果是:{res}')
    
    # 并行计算用到的进程id
    pids = set()
    while not queue.empty():
        pids.add(queue.get())
    
    print(f'用到的进程id是: { pids }')
    queue.close()
    