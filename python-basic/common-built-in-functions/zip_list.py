'''
zip() 函数详解

zip(*iterables): 将多个可迭代对象中对应的元素打包成元组

特点：
1. 惰性求值：返回迭代器，节省内存
2. 长度取最短：以最短的可迭代对象为准
3. 支持任意数量：可以打包两个或多个可迭代对象
4. 可逆操作：使用 zip(*zipped) 可以解压

实际应用场景：
1. 数据配对：将相关数据组合在一起
2. 矩阵转置：行列转换
3. 并行迭代：同时遍历多个序列
4. 字典构建：从键列表和值列表构建字典
'''

print("=" * 50)
print("基础用法示例")
print("=" * 50)

# 基础示例
print("1. 基本 zip() 用法：")
list1 = [1, 2, 3, 4]
list2 = ['a', 'b', 'c', 'd']
list3 = [10.5, 20.5, 30.5, 40.5]

zipped = zip(list1, list2, list3)
print(f"   list1: {list1}")
print(f"   list2: {list2}")
print(f"   list3: {list3}")
print(f"   zip(list1, list2, list3): {list(zipped)}")

print("\n2. 不同长度的可迭代对象：")
short_list = [1, 2, 3]
long_list = ['a', 'b', 'c', 'd', 'e']

zipped_unequal = zip(short_list, long_list)
print(f"   short_list: {short_list}")
print(f"   long_list: {long_list}")
print(f"   zip(short_list, long_list): {list(zipped_unequal)}")
print(f"   注意: 以最短的列表长度为准")

print("\n3. 解压（使用 zip(*zipped)）：")
pairs = [(1, 'a'), (2, 'b'), (3, 'c')]
unzipped = zip(*pairs)
numbers, letters = unzipped
print(f"   原始数据: {pairs}")
print(f"   解压后 numbers: {list(numbers)}")
print(f"   解压后 letters: {list(letters)}")

print("\n" + "=" * 50)
print("实际应用场景示例")
print("=" * 50)

# 场景1：学生成绩管理
def process_student_grades(names, scores, subjects):
    """处理学生成绩数据"""
    print("1. 学生成绩管理：")
    print("-" * 30)

    # 使用 zip 组合数据
    student_records = []
    for name, score, subject in zip(names, scores, subjects):
        grade = 'A' if score >= 90 else 'B' if score >= 80 else 'C' if score >= 70 else 'D' if score >= 60 else 'F'
        student_records.append({
            'name': name,
            'subject': subject,
            'score': score,
            'grade': grade
        })

    # 显示结果
    print("   学生成绩记录:")
    for record in student_records:
        print(f"     {record['name']} - {record['subject']}: {record['score']}分 ({record['grade']})")

    # 计算平均分
    avg_score = sum(scores) / len(scores)
    print(f"\n   平均分: {avg_score:.1f}")

    return student_records

names = ["Alice", "Bob", "Charlie", "Diana"]
scores = [85, 92, 78, 95]
subjects = ["数学", "英语", "物理", "化学"]

process_student_grades(names, scores, subjects)

# 场景2：矩阵转置
def transpose_matrix(matrix):
    """矩阵转置"""
    return [list(row) for row in zip(*matrix)]

def print_matrix(matrix, title="矩阵"):
    """打印矩阵"""
    print(f"\n   {title}:")
    for row in matrix:
        print(f"     {row}")

print("\n2. 矩阵转置：")
print("-" * 30)

matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
    [10, 11, 12]
]

print_matrix(matrix, "原始矩阵")
transposed = transpose_matrix(matrix)
print_matrix(transposed, "转置后矩阵")

# 场景3：数据配对和分组
def group_data_by_category(categories, values):
    """按类别分组数据"""
    print("\n3. 数据分组：")
    print("-" * 30)

    # 使用字典分组
    grouped = {}
    for category, value in zip(categories, values):
        if category not in grouped:
            grouped[category] = []
        grouped[category].append(value)

    print("   分组结果:")
    for category, items in grouped.items():
        avg = sum(items) / len(items)
        print(f"     {category}: {items} (平均值: {avg:.1f})")

    return grouped

categories = ["水果", "蔬菜", "水果", "肉类", "蔬菜", "水果", "肉类"]
prices = [5.5, 3.2, 6.0, 25.0, 2.8, 4.5, 30.0]

grouped_data = group_data_by_category(categories, prices)

# 场景4：并行文件处理
def process_files_in_parallel(file_names, file_contents):
    """并行处理多个文件"""
    print("\n4. 并行文件处理：")
    print("-" * 30)

    results = []
    for filename, content in zip(file_names, file_contents):
        # 模拟文件处理：计算行数和字符数
        lines = content.split('\n')
        line_count = len(lines)
        char_count = sum(len(line) for line in lines)

        results.append({
            'filename': filename,
            'line_count': line_count,
            'char_count': char_count,
            'avg_line_length': char_count / line_count if line_count > 0 else 0
        })

    print("   文件处理结果:")
    for result in results:
        print(f"     {result['filename']}: {result['line_count']}行, {result['char_count']}字符, 平均行长: {result['avg_line_length']:.1f}")

    return results

# 模拟文件内容
file_names = ["document1.txt", "document2.txt", "document3.txt"]
file_contents = [
    "Hello World\nThis is a test\nPython is great",
    "Data analysis\nMachine learning\nDeep learning",
    "Simple text\nShort file"
]

process_files_in_parallel(file_names, file_contents)

# 场景5：字典操作
def create_dictionary_from_lists(keys, values):
    """从键列表和值列表创建字典"""
    return dict(zip(keys, values))

def invert_dictionary(dictionary):
    """反转字典（键值互换）"""
    return dict(zip(dictionary.values(), dictionary.keys()))

print("\n5. 字典操作：")
print("-" * 30)

keys = ["name", "age", "city", "occupation"]
values = ["Alice", 30, "New York", "Engineer"]

# 创建字典
person_dict = create_dictionary_from_lists(keys, values)
print(f"   从列表创建的字典: {person_dict}")

# 反转字典
inverted_dict = invert_dictionary(person_dict)
print(f"   反转后的字典: {inverted_dict}")

# 场景6：数据验证和清洗
def validate_and_clean_data(ids, names, ages):
    """验证和清洗数据"""
    print("\n6. 数据验证和清洗：")
    print("-" * 30)

    clean_data = []
    invalid_records = []

    for id_val, name, age in zip(ids, names, ages):
        # 验证规则
        is_valid = True
        issues = []

        if not isinstance(id_val, int) or id_val <= 0:
            is_valid = False
            issues.append("ID必须为正整数")

        if not isinstance(name, str) or len(name.strip()) == 0:
            is_valid = False
            issues.append("姓名不能为空")

        if not isinstance(age, int) or age < 0 or age > 150:
            is_valid = False
            issues.append("年龄必须在0-150之间")

        if is_valid:
            clean_data.append({
                'id': id_val,
                'name': name.strip(),
                'age': age
            })
        else:
            invalid_records.append({
                'id': id_val,
                'name': name,
                'age': age,
                'issues': issues
            })

    print(f"   有效记录: {len(clean_data)}条")
    print(f"   无效记录: {len(invalid_records)}条")

    if invalid_records:
        print("\n   无效记录详情:")
        for record in invalid_records[:3]:  # 只显示前3条
            print(f"     ID:{record['id']}, 姓名:'{record['name']}', 年龄:{record['age']}")
            print(f"       问题: {', '.join(record['issues'])}")

    return clean_data, invalid_records

# 测试数据（包含一些无效数据）
test_ids = [1, 2, -3, 4, 5]
test_names = ["Alice", "Bob", "", "David", "Eve  "]
test_ages = [25, 30, 20, 200, 35]

clean, invalid = validate_and_clean_data(test_ids, test_names, test_ages)

print("\n" + "=" * 50)
print("进阶技巧")
print("=" * 50)

# 技巧1：zip() 与 enumerate() 结合
print("1. zip() 与 enumerate() 结合：")
names = ["Alice", "Bob", "Charlie"]
scores = [85, 92, 78]

print("   带索引的配对:")
for i, (name, score) in enumerate(zip(names, scores)):
    print(f"     {i+1}. {name}: {score}分")

# 技巧2：处理不等长列表的优雅方式
print("\n2. 处理不等长列表：")
from itertools import zip_longest

list_a = [1, 2, 3]
list_b = ['a', 'b', 'c', 'd', 'e']

print("   使用 zip_longest（填充默认值）:")
for a, b in zip_longest(list_a, list_b, fillvalue='N/A'):
    print(f"     {a} - {b}")

# 技巧3：嵌套 zip()
print("\n3. 嵌套 zip()：")
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

# 获取所有对角线元素
main_diagonal = [row[i] for i, row in enumerate(matrix)]
anti_diagonal = [row[-i-1] for i, row in enumerate(matrix)]

print(f"   矩阵: {matrix}")
print(f"   主对角线: {main_diagonal}")
print(f"   反对角线: {anti_diagonal}")

# 技巧4：zip() 与 map() 结合
print("\n4. zip() 与 map() 结合：")
vector1 = [1, 2, 3, 4]
vector2 = [5, 6, 7, 8]

# 计算点积
dot_product = sum(a * b for a, b in zip(vector1, vector2))
print(f"   向量1: {vector1}")
print(f"   向量2: {vector2}")
print(f"   点积: {dot_product}")

# 计算元素 wise 操作
added = list(map(lambda x: x[0] + x[1], zip(vector1, vector2)))
multiplied = list(map(lambda x: x[0] * x[1], zip(vector1, vector2)))

print(f"   元素相加: {added}")
print(f"   元素相乘: {multiplied}")

# 技巧5：自定义 zip 函数
def safe_zip(*iterables, fillvalue=None):
    """安全的 zip 函数，可以处理空迭代对象"""
    if not iterables:
        return []

    # 找到最大长度
    max_len = max(len(iterable) for iterable in iterables)

    result = []
    for i in range(max_len):
        tuple_items = []
        for iterable in iterables:
            if i < len(iterable):
                tuple_items.append(iterable[i])
            else:
                tuple_items.append(fillvalue)
        result.append(tuple(tuple_items))

    return result

print("\n5. 自定义安全的 zip 函数：")
list1 = [1, 2]
list2 = ['a', 'b', 'c']
list3 = [10.5, 20.5, 30.5, 40.5]

print(f"   list1: {list1}")
print(f"   list2: {list2}")
print(f"   list3: {list3}")
print(f"   safe_zip(list1, list2, list3, fillvalue=0):")
for item in safe_zip(list1, list2, list3, fillvalue=0):
    print(f"     {item}")

print("\n" + "=" * 50)
print("交互式示例")
print("=" * 50)

try:
    print("zip() 函数交互演示")
    print("1. 基本 zip 演示")
    print("2. 矩阵转置演示")
    print("3. 字典创建演示")

    choice = input("请选择演示类型 (1-3): ")

    if choice == "1":
        # 用户输入列表
        list1_input = input("请输入第一个列表（用逗号分隔）: ")
        list2_input = input("请输入第二个列表（用逗号分隔）: ")

        list1 = [item.strip() for item in list1_input.split(',')]
        list2 = [item.strip() for item in list2_input.split(',')]

        print(f"\n列表1: {list1}")
        print(f"列表2: {list2}")

        zipped = list(zip(list1, list2))
        print(f"zip() 结果: {zipped}")

        # 解压演示
        if zipped:
            unzipped = zip(*zipped)
            unzipped_lists = [list(item) for item in unzipped]
            print(f"解压后: {unzipped_lists}")

    elif choice == "2":
        rows = int(input("请输入矩阵行数: "))
        cols = int(input("请输入矩阵列数: "))

        print(f"\n请输入 {rows} 行数据，每行 {cols} 个数字（用空格分隔）:")
        matrix = []
        for i in range(rows):
            row_input = input(f"第{i+1}行: ")
            row = [int(x) for x in row_input.split()]
            if len(row) != cols:
                print(f"错误: 需要 {cols} 个数字，但输入了 {len(row)} 个")
                break
            matrix.append(row)

        if len(matrix) == rows:
            print(f"\n原始矩阵:")
            for row in matrix:
                print(f"  {row}")

            transposed = transpose_matrix(matrix)
            print(f"\n转置矩阵:")
            for row in transposed:
                print(f"  {row}")

    elif choice == "3":
        keys_input = input("请输入键列表（用逗号分隔）: ")
        values_input = input("请输入值列表（用逗号分隔）: ")

        keys = [key.strip() for key in keys_input.split(',')]
        values = [value.strip() for value in values_input.split(',')]

        if len(keys) != len(values):
            print(f"错误: 键列表({len(keys)}个)和值列表({len(values)}个)长度不一致")
        else:
            dictionary = dict(zip(keys, values))
            print(f"\n创建的字典: {dictionary}")

            # 反转字典
            try:
                inverted = dict(zip(dictionary.values(), dictionary.keys()))
                print(f"反转后的字典: {inverted}")
            except TypeError:
                print("注意: 值包含不可哈希类型，无法反转字典")

    else:
        print("无效的选择")

except Exception as e:
    print(f"发生错误: {e}")