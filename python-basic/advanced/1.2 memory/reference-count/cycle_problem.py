import gc

class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
    
    def __del__(self):
        print(f"🗑️  Node {self.value} 被销毁")

def create_cycle():
    """创建循环引用"""
    node1 = Node(1)
    node2 = Node(2)
    node3 = Node(3)
    
    node1.next = node2
    node2.next = node3  
    node3.next = node1  # 循环引用！
    
    print("🔄 循环引用创建完成")
    return node1

# 测试循环引用
cycle_head = create_cycle()

def analyze_memory_behavior():
    # 启用调试
    gc.set_debug(gc.DEBUG_SAVEALL)

    # 创建循环引用
    cycle_head = create_cycle()

    # 手动触发垃圾回收
    print("🚀 触发垃圾回收...")
    collected = gc.collect()

    print(f"🗑️ 回收的对象数量: {collected}")
    print(f"📊 垃圾回收器统计: {gc.get_stats()}")

    # 检查对象是否还存在
    print(f"🔍 cycle_head 仍然存在: {cycle_head is not None}")

analyze_memory_behavior()