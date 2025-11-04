import concurrent.futures
from functools import partial
import gc

# import sys
# import os

# # Add the parent directory to sys.path to enable import
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from memory_sensitive_data_pipline import MemorySensitiveDataPipeline

class AdvancedDataPipeline(MemorySensitiveDataPipeline):
    def parallel_chunk_processing(self, file_path: str, num_workers: int = 4):
        """并行分块处理 - 兼顾速度和内存效率"""
        
        def process_chunk_worker(chunk_data: tuple) -> str:
            """工作进程处理函数"""
            chunk, chunk_id = chunk_data
            # 模拟复杂处理
            processed = f"Chunk_{chunk_id}_Processed: {len(chunk)}"
            return processed
        
        # 创建处理任务
        chunks = [(chunk, i) for i, chunk in enumerate(self.stream_large_file(file_path))]
        
        # 使用进程池并行处理，但控制并发数量避免内存爆炸
        results = []
        with concurrent.futures.ProcessPoolExecutor(max_workers=num_workers) as executor:
            # 分批次提交任务，控制内存使用
            batch_size = num_workers * 2  # 避免同时处理太多数据
            
            for i in range(0, len(chunks), batch_size):
                batch = chunks[i:i + batch_size]
                batch_results = list(executor.map(process_chunk_worker, batch))
                results.extend(batch_results)
                
                # 批次间内存清理
                gc.collect()
        
        return results