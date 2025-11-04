from typing import List, Any

class ObjectPool:
    """对象池：避免频繁创建销毁对象"""
    def __init__(self, object_factory, pool_size=100):
        self.pool = [object_factory() for _ in range(pool_size)]
        self.available = list(range(pool_size))
        self.in_use = set()
    
    def acquire(self) -> Any:
        if self.available:
            idx = self.available.pop()
            self.in_use.add(idx)
            return self.pool[idx]
        # 池耗尽时的扩展策略
        return self.object_factory()
    
    def release(self, obj: Any):
        idx = self.pool.index(obj)
        if idx in self.in_use:
            self.in_use.remove(idx)
            self.available.append(idx)

# 使用对象池处理大量临时对象
pool = ObjectPool(lambda: [0] * 1000)