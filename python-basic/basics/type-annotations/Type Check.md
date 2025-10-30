isinstance可以用于在python中判断类型
```py
a =1
isinstance(a, int)
# True
lst = [1]
isinstance(lst,list)
# True
isinstance(lst,tuple)
# False
```

对比js:
```js
a = [1,2,3]
(3) [1, 2, 3]
a instanceof Array
true
a instanceof Object
true
Array.isArray(a)
true
```