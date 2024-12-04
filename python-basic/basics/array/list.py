
l = [1,2,3,4]

for (index, val) in enumerate(l):
    print(l)

l.remove(1)

print(l)
print(l.index(2))

try:
    print(l.index(1))
except ValueError as e:
    print("not found")
finally:
    print("always implement")


l = [1,1,2,2]
l.remove(1)
print(l, l.count(1))

l.pop()
print(l)

l.append(0)

l.sort(reverse=True)
print(l)

a1 = [1,2]
a2 = [1,2]
print(a1 == a2)
# True

tl = tuple(l)
print(tl)
# t1[0] = 3 error tuple value can not change

newl = list(tl)
newl[0] = 6
print(newl)