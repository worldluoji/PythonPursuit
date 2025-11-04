import mmap
from typing import Iterator, Callable
import gc
# 监控内存使用
import psutil


class MemorySensitiveDataPipeline:
    def __init__(self, max_memory_mb: int = 100):
        self.max_memory_mb = max_memory_mb
        self.processed_chunks = 0
        
    def stream_large_file(self, file_path: str, chunk_size: int = 1024 * 1024) -> Iterator[str]:
        """流式读取大文件 - 扩展您的分块读取方案"""
        with open(file_path, 'r', encoding='utf-8') as f:
            # 使用内存映射进一步提高效率
            with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mmapped_file:
                while True:
                    chunk = mmapped_file.read(chunk_size).decode('utf-8')
                    if not chunk:
                        break
                    yield chunk
                    # 主动内存管理
                    if self.processed_chunks % 10 == 0:
                        gc.collect()
    
    def process_with_memory_control(self, file_path: str, 
                                  process_func: Callable,
                                  output_path: str):
        """带内存控制的数据处理管道"""
        process = psutil.Process()
        
        with open(output_path, 'w', encoding='utf-8') as output_file:
            for i, chunk in enumerate(self.stream_large_file(file_path)):
                
                # 内存使用检查
                current_memory_mb = process.memory_info().rss / 1024 / 1024
                if current_memory_mb > self.max_memory_mb:
                    print(f"⚠️ 内存警告: {current_memory_mb:.1f}MB > {self.max_memory_mb}MB")
                    # 紧急内存释放策略
                    gc.collect()
                
                # 处理数据块（您的process_chunk函数）
                processed_result = process_func(chunk, i)
                
                # 流式写入结果，不积累内存
                output_file.write(processed_result + '\n')
                output_file.flush()  # 立即写入，释放内存
                
                self.processed_chunks += 1
                print(f"📊 处理进度: {i+1}块, 内存使用: {current_memory_mb:.1f}MB")