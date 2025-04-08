# pythonic

## 1. 变量交换
Bad
```python
tmp = a
a = b
b = tmp
```

Pythonic
```python
a,b = b,a
```

## 2.  列表推导
Bad
```python
my_list = []
for i in range(10):
    my_list.append(i*2)
Pythonic
```
```python
my_list = [i*2 for i in range(10)]
```

## 3.  单行表达式
虽然列表推导式由于其简洁性及表达性，被广受推崇。

但是有许多可以写成单行的表达式，并不是好的做法。

Bad
```python
print('one'); print('two')

if x == 1: print('one')

if <complex comparison> and <other complex comparison>:
    # do something
```

Pythonic
```python
print('one')
print('two')

if x == 1:
    print('one')

cond1 = <complex comparison>
cond2 = <other complex comparison>
if cond1 and cond2:
    # do something
```

## 4. 带索引遍历
Bad
```python
for i in range(len(my_list)):
    print(i, "-->", my_list[i])
```

Pythonic
```python
for i,item in enumerate(my_list):
    print(i, "-->", item)
```

## 5. 序列解包
Pythonic
```python
a, *rest = [1, 2, 3]
# a = 1, rest = [2, 3]

a, *middle, c = [1, 2, 3, 4]
# a = 1, middle = [2, 3], c = 4
```

## 6. 字符串拼接
Bad
```python
letters = ['s', 'p', 'a', 'm']
s=""
for let in letters:
    s += let
```

Pythonic
```python
letters = ['s', 'p', 'a', 'm']
word = ''.join(letters)
```

## 7. 真假判断
Bad
```python
if attr == True:
    print('True!')

if attr == None:
    print('attr is None!')
```

Pythonic
```python
if attr:
    print('attr is truthy!')

if not attr:
    print('attr is falsey!')

if attr is None:
    print('attr is None!')
```

## 8. 访问字典元素
Bad
```python
d = {'hello': 'world'}
if d.has_key('hello'):
    print(d['hello'])    # prints 'world'
else:
    print('default_value')
```

Pythonic
```python
d = {'hello': 'world'}

print(d.get('hello', 'default_value')) # prints 'world'
print(d.get('thingy', 'default_value')) # prints 'default_value'
```
Or:
```python
if 'hello' in d:
    print d['hello']
```

## 9. 操作列表
Bad
```python
a = [3, 4, 5]
b = []
for i in a:
    if i > 4:
        b.append(i)
```
Pythonic
```python
a = [3, 4, 5]
b = [i for i in a if i > 4]
```
Or:
```python
b = filter(lambda x: x > 4, a)
```

Bad
```python
a = [3, 4, 5]
for i in range(len(a)):
    a[i] += 3
```
Pythonic
```python
a = [3, 4, 5]
a = [i + 3 for i in a]
```
Or:
```python
a = map(lambda i: i + 3, a)
```

## 10. 文件读取
Bad
```python
f = open('file.txt')
a = f.read()
print a
f.close()
```
Pythonic
```python
with open('file.txt', 'r', encoding='utf-8') as f:
    for line in f:
        print line
```
这里需要注意，使用open()函数，file.txt文件需要在当前执行文件所在的目录。否则我们应该用os.path.join() 用于安全地拼接路径。

## 11. 代码续行
Bad
```python
my_very_big_string = """For a long time I used to go to bed early. Sometimes, \
    when I had put out my candle, my eyes would close so quickly that I had not even \
    time to say “I’m going to sleep.”"""

from some.deep.module.inside.a.module import a_nice_function, another_nice_function, \
    yet_another_nice_function
```

Pythonic
```python
my_very_big_string = (
    "For a long time I used to go to bed early. Sometimes, "
    "when I had put out my candle, my eyes would close so quickly "
    "that I had not even time to say “I’m going to sleep.”"
)

from some.deep.module.inside.a.module import (
    a_nice_function, another_nice_function, yet_another_nice_function)
```

## 12. 显式代码
Bad
```python
def make_complex(*args):
    x, y = args
    return dict(**locals())
```
Pythonic
```python
def make_complex(x, y):
    return {'x': x, 'y': y}
```

## 13. 使用占位符
Pythonic
```python
filename = 'foobar.txt'
basename, _, ext = filename.rpartition('.')
```

## 14. 链式比较
Bad
```python
if age > 18 and age < 60:
    print("young man")
```
Pythonic
```python
if 18 < age < 60:
    print("young man")
```
理解了链式比较操作，那么你应该知道为什么下面这行代码输出的结果是 False
```python
>>> False == False == True 
False
```

## 15. 三目运算
这个保留意见。随使用习惯就好。
Bad
```python
if a > 2:
    b = 2
else:
    b = 1
#b = 2
```
Pythonic
```python
a = 3   
b = 2 if a > 2 else 1
#b = 2
```