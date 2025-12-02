'''
range() 函数详解

range(start, stop, step): 生成一个不可变的数字序列

参数说明：
- start: 起始值（包含，默认为0）
- stop: 结束值（不包含）
- step: 步长（默认为1）

特点：
1. 惰性求值：不立即生成所有元素，节省内存
2. 不可变：创建后不能修改
3. 支持负数步长：可以反向迭代
4. 支持大范围：可以处理非常大的数字

实际应用场景：
1. 循环控制：指定循环次数
2. 序列生成：生成数字序列
3. 索引遍历：遍历列表/字符串的索引
4. 数值计算：生成等差数列
'''

print("=" * 50)
print("基础用法示例")
print("=" * 50)

# 基础示例
print("1. 基本 range() 用法：")
print(f"   range(5): {list(range(5))}")           # [0, 1, 2, 3, 4]
print(f"   range(2, 8): {list(range(2, 8))}")     # [2, 3, 4, 5, 6, 7]
print(f"   range(0, 10, 2): {list(range(0, 10, 2))}")  # [0, 2, 4, 6, 8]
print(f"   range(10, 0, -2): {list(range(10, 0, -2))}")  # [10, 8, 6, 4, 2]

print("\n2. 不同步长示例：")
print("   步长为3:")
for i in range(0, 10, 3):
    print(f"      {i}", end=' ')
print()

print("\n   负步长（反向）:")
for i in range(10, 0, -1):
    print(f"      {i}", end=' ')
print()

print("\n" + "=" * 50)
print("实际应用场景示例")
print("=" * 50)

# 场景1：生成乘法表
def print_multiplication_table(n=9):
    """打印乘法表"""
    print("1. 乘法表生成：")
    print("-" * 30)

    # 表头
    print("   ", end='')
    for i in range(1, n + 1):
        print(f"{i:4}", end='')
    print()
    print("   " + "-" * (4 * n))

    # 表格内容
    for i in range(1, n + 1):
        print(f"{i:2} |", end='')
        for j in range(1, n + 1):
            print(f"{i * j:4}", end='')
        print()

print_multiplication_table(5)

# 场景2：列表/字符串索引遍历
def process_with_indices(data):
    """使用索引处理数据"""
    print("\n2. 带索引的数据处理：")
    print("-" * 30)

    print(f"   数据: {data}")
    print(f"   索引和值:")

    # 方法1：使用 range(len())
    for i in range(len(data)):
        print(f"      [{i}] = {data[i]}")

    # 方法2：使用 enumerate()（更Pythonic）
    print(f"\n   使用 enumerate():")
    for i, value in enumerate(data):
        print(f"      [{i}] = {value}")

process_with_indices(["苹果", "香蕉", "橙子", "葡萄"])

# 场景3：生成等差数列
def generate_arithmetic_sequence(start, end, step):
    """生成等差数列"""
    sequence = list(range(start, end, step))
    return sequence

def analyze_sequence(sequence):
    """分析数列特性"""
    if len(sequence) < 2:
        return "序列太短"

    differences = [sequence[i+1] - sequence[i] for i in range(len(sequence)-1)]
    is_arithmetic = all(diff == differences[0] for diff in differences)

    return {
        'length': len(sequence),
        'first': sequence[0],
        'last': sequence[-1],
        'step': differences[0] if is_arithmetic else None,
        'is_arithmetic': is_arithmetic,
        'sum': sum(sequence)
    }

print("\n3. 等差数列生成和分析：")
print("-" * 30)

sequences = [
    (0, 20, 2),   # 偶数序列
    (1, 20, 2),   # 奇数序列
    (5, 50, 5),   # 5的倍数
    (10, 0, -1),  # 反向序列
]

for start, end, step in sequences:
    seq = generate_arithmetic_sequence(start, end, step)
    analysis = analyze_sequence(seq)

    print(f"\n   参数: range({start}, {end}, {step})")
    print(f"   生成的序列: {seq}")
    if analysis['is_arithmetic']:
        print(f"   特性: 等差数列，步长={analysis['step']}，长度={analysis['length']}")
        print(f"   求和: {analysis['sum']}")

# 场景4：时间序列生成
def generate_time_slots(start_hour, end_hour, interval_minutes):
    """生成时间槽"""
    print("\n4. 时间序列生成：")
    print("-" * 30)

    total_minutes = (end_hour - start_hour) * 60
    slots = []

    for minutes in range(0, total_minutes, interval_minutes):
        hour = start_hour + minutes // 60
        minute = minutes % 60
        time_str = f"{hour:02d}:{minute:02d}"
        slots.append(time_str)

    print(f"   时间范围: {start_hour:02d}:00 - {end_hour:02d}:00")
    print(f"   间隔: {interval_minutes}分钟")
    print(f"   生成的时间槽: {slots}")

generate_time_slots(9, 17, 30)  # 9点到17点，每30分钟

# 场景5：网格坐标生成
def generate_grid_coordinates(rows, cols):
    """生成网格坐标"""
    print("\n5. 网格坐标生成：")
    print("-" * 30)

    coordinates = []
    for row in range(rows):
        for col in range(cols):
            coordinates.append((row, col))

    print(f"   网格大小: {rows}行 × {cols}列")
    print(f"   总坐标数: {len(coordinates)}")
    print(f"   前10个坐标: {coordinates[:10]}")

    # 可视化显示
    print(f"\n   网格可视化:")
    for row in range(rows):
        row_display = []
        for col in range(cols):
            row_display.append(f"({row},{col})")
        print(f"   {' '.join(row_display)}")

generate_grid_coordinates(3, 4)

print("\n" + "=" * 50)
print("进阶技巧")
print("=" * 50)

# 技巧1：range() 的内存效率
print("1. range() 的内存效率：")
print("   比较 range() 和 list 的内存使用:")

import sys

# 大范围的 range 对象
large_range = range(1_000_000)
large_list = list(range(1_000_000))

print(f"   range(1,000,000) 内存大小: {sys.getsizeof(large_range)} 字节")
print(f"   list(range(1,000,000)) 内存大小: {sys.getsizeof(large_list):,} 字节")
print(f"   内存节省: {(sys.getsizeof(large_list) - sys.getsizeof(large_range)) / sys.getsizeof(large_list) * 100:.1f}%")

# 技巧2：range() 的切片操作
print("\n2. range() 的切片操作：")
r = range(0, 20, 2)
print(f"   原始 range: {list(r)}")
print(f"   切片 r[2:6]: {list(r[2:6])}")
print(f"   切片 r[-3:]: {list(r[-3:])}")
print(f"   切片 r[::-1]: {list(r[::-1])}")  # 反转

# 技巧3：range() 与 zip() 结合
print("\n3. range() 与 zip() 结合：")
names = ["Alice", "Bob", "Charlie", "David"]
scores = [85, 92, 78, 95]

print("   学生成绩表:")
for i, (name, score) in zip(range(1, len(names) + 1), zip(names, scores)):
    print(f"     {i}. {name}: {score}分")

# 技巧4：生成特定模式的序列
print("\n4. 生成特定模式的序列：")

# 生成斐波那契数列索引
fib_indices = list(range(0, 10))
print(f"   斐波那契数列索引: {fib_indices}")

# 生成对称序列
symmetric = list(range(-5, 6))
print(f"   对称序列: {symmetric}")

# 生成交替序列
alternating = []
for i in range(0, 10, 2):
    alternating.extend([i, i+1])
print(f"   交替序列: {alternating}")

# 技巧5：range() 的参数验证
def safe_range(start, stop=None, step=1):
    """安全的 range() 函数，处理边界情况"""
    if stop is None:
        stop = start
        start = 0

    if step == 0:
        raise ValueError("range() step cannot be zero")

    # 处理浮点数（转换为整数）
    start = int(start)
    stop = int(stop)
    step = int(step)

    return range(start, stop, step)

print("\n5. 安全的 range() 函数：")
try:
    # 正常情况
    print(f"   safe_range(5): {list(safe_range(5))}")
    # 浮点数输入
    print(f"   safe_range(2.5, 7.8): {list(safe_range(2.5, 7.8))}")
    # 错误情况
    # print(f"   safe_range(1, 10, 0): {list(safe_range(1, 10, 0))}")  # 会抛出异常
except ValueError as e:
    print(f"   错误: {e}")

print("\n" + "=" * 50)
print("交互式示例")
print("=" * 50)

try:
    print("生成自定义 range 序列")
    start = int(input("请输入起始值: "))
    stop = int(input("请输入结束值（不包含）: "))
    step = int(input("请输入步长: "))

    if step == 0:
        print("❌ 步长不能为0！")
    else:
        r = range(start, stop, step)
        sequence = list(r)

        print(f"\n生成的序列: {sequence}")
        print(f"序列长度: {len(sequence)}")

        if len(sequence) > 0:
            print(f"第一个元素: {sequence[0]}")
            print(f"最后一个元素: {sequence[-1]}")
            print(f"序列总和: {sum(sequence)}")

            if len(sequence) > 1:
                step_actual = sequence[1] - sequence[0]
                print(f"实际步长: {step_actual}")

except ValueError:
    print("❌ 请输入有效的整数！")