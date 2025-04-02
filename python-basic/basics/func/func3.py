def func1(x, s) -> str:
    s = s + x

def func2(x, s) -> str:
    s = s + x
    return s

s = 'abc'

func1('d', s)
print(s)

snew = func2('e', s)
print(snew)
# 字符串是不可变对象，func2中返回的s是一个新的字符串对象，所以snew和s不是同一个对象
print(id(snew) == id(s))
    