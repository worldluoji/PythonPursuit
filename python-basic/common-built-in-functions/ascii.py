'''
ord() 和 chr() 函数详解

ord(char): 返回单个字符的 Unicode 码点（整数）
chr(code): 返回 Unicode 码点对应的字符

实际应用场景：
1. 字符编码转换
2. 密码学中的简单加密
3. 文本处理和分析
4. 生成特殊字符
'''

print("=" * 50)
print("基础用法示例")
print("=" * 50)

# 基础示例
print("1. 获取字符的 Unicode 码点：")
print(f"   ord('A') = {ord('A')}")
print(f"   ord('中') = {ord('中')}")  # 中文字符
print(f"   ord('😊') = {ord('😊')}")  # 表情符号

print("\n2. 通过码点获取字符：")
print(f"   chr(65) = '{chr(65)}'")
print(f"   chr(20013) = '{chr(20013)}'")  # 中文字符
print(f"   chr(128522) = '{chr(128522)}'")  # 表情符号

print("\n" + "=" * 50)
print("实际应用场景示例")
print("=" * 50)

# 场景1：简单加密解密（凯撒密码）
def caesar_cipher(text, shift):
    """凯撒密码：将文本中的每个字母移动 shift 个位置"""
    result = []
    for char in text:
        if 'A' <= char <= 'Z':
            # 大写字母：A=65, Z=90
            shifted = (ord(char) - 65 + shift) % 26 + 65
            result.append(chr(shifted))
        elif 'a' <= char <= 'z':
            # 小写字母：a=97, z=122
            shifted = (ord(char) - 97 + shift) % 26 + 97
            result.append(chr(shifted))
        else:
            # 非字母字符保持不变
            result.append(char)
    return ''.join(result)

print("1. 凯撒密码加密解密：")
print("-" * 30)
original = "Hello, World! 2025"
encrypted = caesar_cipher(original, 3)
decrypted = caesar_cipher(encrypted, -3)

print(f"   原始文本: {original}")
print(f"   加密后(位移3): {encrypted}")
print(f"   解密后: {decrypted}")

# 场景2：字符频率分析
def analyze_text_frequency(text):
    """分析文本中字母的出现频率"""
    frequency = {}
    for char in text.lower():
        if 'a' <= char <= 'z':
            frequency[char] = frequency.get(char, 0) + 1

    # 按频率排序
    sorted_freq = sorted(frequency.items(), key=lambda x: x[1], reverse=True)

    print(f"\n2. 文本字符频率分析：")
    print(f"   文本: '{text}'")
    print(f"   字符频率统计:")
    for char, count in sorted_freq[:5]:  # 只显示前5个
        print(f"     '{char}': {count}次 (Unicode: {ord(char)})")

analyze_text_frequency("Python Programming is fun!")

# 场景3：生成特殊字符和图案
print("\n3. 生成特殊字符和图案：")
print("-" * 30)

# 生成字母表
alphabet = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
print(f"   大写字母表: {''.join(alphabet)}")

# 生成数字字符
digits = [chr(i) for i in range(ord('0'), ord('9') + 1)]
print(f"   数字字符: {''.join(digits)}")

# 生成简单图案
print("\n   简单图案示例（三角形）：")
for i in range(1, 6):
    stars = chr(9733) * i  # 9733 是 ★ 的 Unicode
    print(f"   {stars:^10}")

# 场景4：检查字符类型
def classify_characters(text):
    """分类文本中的字符类型"""
    categories = {
        '大写字母': 0,
        '小写字母': 0,
        '数字': 0,
        '标点符号': 0,
        '其他字符': 0
    }

    for char in text:
        code = ord(char)
        if 65 <= code <= 90:
            categories['大写字母'] += 1
        elif 97 <= code <= 122:
            categories['小写字母'] += 1
        elif 48 <= code <= 57:
            categories['数字'] += 1
        elif 33 <= code <= 47 or 58 <= code <= 64 or 91 <= code <= 96 or 123 <= code <= 126:
            categories['标点符号'] += 1
        else:
            categories['其他字符'] += 1

    print(f"\n4. 字符分类统计：")
    print(f"   文本: '{text}'")
    for category, count in categories.items():
        if count > 0:
            print(f"   {category}: {count}个")

classify_characters("Hello, 世界! 2025年。")

print("\n" + "=" * 50)
print("进阶技巧")
print("=" * 50)

# 技巧1：字符范围遍历
print("1. 遍历字符范围：")
print("   英文字母表:")
for code in range(ord('A'), ord('Z') + 1):
    print(f"   {chr(code)}", end=' ')
print()

# 技巧2：特殊字符生成
print("\n2. 特殊字符生成：")
special_chars = {
    '版权符号': chr(169),
    '注册商标': chr(174),
    '欧元符号': chr(8364),
    '摄氏度': chr(8451),
    '平方': chr(178),
    '立方': chr(179)
}
for name, char in special_chars.items():
    print(f"   {name}: {char} (Unicode: {ord(char)})")

# 技巧3：检查字符是否在特定范围内
def is_printable_ascii(char):
    """检查字符是否在可打印ASCII范围内（32-126）"""
    code = ord(char)
    return 32 <= code <= 126

print("\n3. 检查字符是否为可打印ASCII：")
test_chars = ['A', ' ', '\n', '中', '😊']
for char in test_chars:
    printable = is_printable_ascii(char)
    print(f"   '{char}' (U+{ord(char):04X}): {'可打印' if printable else '不可打印'}")