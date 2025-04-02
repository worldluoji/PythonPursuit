from multiprocessing import Pool, Manager
import os

def f(x, q):
    q.put(os.getpid())
    return x * x

if __name__ == '__main__':
    with Manager() as manager:  # 使用上下文管理器确保资源释放
        shared_queue = manager.Queue()  # 使用 Manager 创建队列：确保所有子进程操作同一个队列

        count = os.cpu_count()
        print(f'My Computer CPU Number is {count}')

        with Pool(count * 2) as p:
            # 使用starmap传递队列参数
            res = p.starmap(f, [(i, shared_queue) for i in range(1, 101)])
            print(f'计算平方的结果是:{res}')
        
        pids = set()
        while not shared_queue.empty():
            pids.add(shared_queue.get())
        
        print(f'用到的进程id是: { pids }')