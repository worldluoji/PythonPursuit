def func1(x, lst):
    lst.append(x)
    return lst

# list is mutable, 传入的是引用
def func2(x, lst):
    lst.append(x)


lst1 = [1, 2, 3]

func1(4, lst1)
print(lst1)

lst2 = [1, 2, 3]
func2(4, lst2)
print(lst2)