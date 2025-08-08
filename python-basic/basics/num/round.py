import math

n1 = 3.1415926
print(round(n1, 2))

n2 = 3.14812
print(round(n2, 2))

print(f"{n1:.2f}")
print(f"{n2:.2f}")

print("{:.2f}".format(n1))
print("{:.2f}".format(n2))


def truncate(number, decimals=0):
    """直接截断指定位数的小数"""
    factor = 10 ** decimals
    return int(number * factor) / factor

# 示例
print(truncate(2.675, 2))  # 输出 2.67（直接丢弃多余部分）
print(truncate(5.999, 2))  # 输出 5.99（不会进位）


def ceil_precision(number, decimals=0):
    """保留小数位并向上进位"""
    factor = 10 ** decimals
    return math.ceil(number * factor) / factor

# 示例
print(ceil_precision(2.111, 2))  # 输出 2.12（有小数就进位）
print(ceil_precision(3.0, 2))    # 输出 3.0（无小数不进位）