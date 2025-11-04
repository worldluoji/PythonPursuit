import multiprocessing
import asyncio
from typing import List

class HybridConcurrencySystem:
    def __init__(self, num_processes: int = None):
        self.num_processes = num_processes or multiprocessing.cpu_count()
        self.process_pool = None
        self.thread_pool = None
    
    async def process_io_operations(self, tasks: List) -> List:
        """处理I/O密集型任务 - 使用异步"""
        async def single_io_task(task):
            # 模拟数据库查询、文件读写等
            await asyncio.sleep(0.1)  # I/O等待
            return f"IO_result_{task}"
        
        return await asyncio.gather(*[single_io_task(task) for task in tasks])
    
    def process_cpu_intensive(self, data_chunk):
        """处理CPU密集型任务 - 使用多进程"""
        # 模拟复杂计算
        result = sum(i*i for i in range(data_chunk))
        return result
    
    async def orchestrate_workflow(self, io_tasks: List, cpu_data: List):
        """编排混合工作流"""
        
        # 阶段1: 并行处理I/O操作
        io_results = await self.process_io_operations(io_tasks)
        
        # 阶段2: 使用进程池处理CPU密集型计算
        with multiprocessing.Pool(self.num_processes) as pool:
            cpu_results = pool.map(self.process_cpu_intensive, cpu_data)
        
        # 阶段3: 整合结果
        final_results = self.combine_results(io_results, cpu_results)
        return final_results
    

# 场景：实时数据分析系统
async def data_processing_pipeline():
    system = HybridConcurrencySystem()
    
    # I/O部分：从多个数据源获取数据
    data_sources = ["api_1", "api_2", "database", "file_system"]
    
    # CPU部分：对获取的数据进行复杂计算
    computation_tasks = [1000000, 1000000]
    
    results = await system.orchestrate_workflow(data_sources, computation_tasks)
    return results


asyncio.run(data_processing_pipeline())