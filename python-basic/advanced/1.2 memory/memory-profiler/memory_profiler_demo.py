from memory_profiler import profile,memory_usage

@profile
def inefficient_memory_usage():
    """低效的内存使用示例"""
    # 创建大量临时对象
    results = []
    for i in range(10000):
        # 每次迭代都创建新列表
        temp_list = [j * 2 for j in range(1000)]
        results.append(sum(temp_list))
    return results

@profile  
def efficient_memory_usage():
    """高效的内存使用示例"""
    results = []
    # 重用对象，减少内存分配
    reusable_list = [0] * 1000
    for i in range(10000):
        for j in range(1000):
            reusable_list[j] = j * 2
        results.append(sum(reusable_list))
    return results


if __name__ == '__main__':
    mem_usage1 = memory_usage((inefficient_memory_usage, ), interval=0.1)
    print(mem_usage1)

    print("*" * 100)

    mem_usage2 = memory_usage((efficient_memory_usage, ), interval=0.1)
    print(mem_usage2)