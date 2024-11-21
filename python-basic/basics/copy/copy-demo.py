
import copy

original_list = [1, 2, [3, 4]]
shallow_copied_list = copy.copy(original_list)
deep_copied_list = copy.deepcopy(original_list)
slice_copied_list = original_list[:]

print("origin")
print(shallow_copied_list)
print("*" * 16)
print(deep_copied_list)
print("*" * 16)
print(slice_copied_list)

print("*" * 16)
print("changed")

# 浅拷贝里面引用的对象还是原来的
shallow_copied_list[2][1] = 5
print(original_list, shallow_copied_list)
print("*" * 16)

# 深拷贝里面引用的对象也是复制的
deep_copied_list[2][1] = 6
print(original_list, deep_copied_list)
print("*" * 16)

# slice修改列表的方式，是一个浅拷贝
slice_copied_list[2][1] = 7
print(original_list, slice_copied_list)
