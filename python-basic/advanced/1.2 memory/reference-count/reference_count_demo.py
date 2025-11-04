import sys

def demonstrate_reference_counting():
    # 创建对象
    my_list = [1, 2, 3, 4, 5]
    print(f"🔢 初始引用计数: {sys.getrefcount(my_list) - 1}")
    
    # 增加引用
    another_ref = my_list
    print(f"📈 增加引用后: {sys.getrefcount(my_list) - 1}")
    
    # 减少引用
    del another_ref
    print(f"📉 删除引用后: {sys.getrefcount(my_list) - 1}")
    
    return my_list

# 让我们看看引用计数的变化
result = demonstrate_reference_counting()
print(result)