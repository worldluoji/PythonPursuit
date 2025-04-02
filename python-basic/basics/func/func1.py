def func1(x, lst=[]):  # 默认参数lst在函数定义时创建空列表
    lst.append(x)
    return lst

print(func1(1), func1(2))
'''
两次调用共享同一个默认列表对象，​后续调用会修改之前的结果。
打印时 func(1) 返回的列表已因第二次调用被修改为 [1, 2]。
'''
print(id(func1(1)) == id(func1(2)))

def func2(x, lst=None):
    lst = [] if lst is None else lst  # 每次调用生成新列表
    lst.append(x)
    return lst

print(func2(1), func2(2))