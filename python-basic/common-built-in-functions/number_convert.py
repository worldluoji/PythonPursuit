'''
Python 进制转换函数详解

bin(x): 将整数转换为二进制字符串（前缀 '0b'）
oct(x): 将整数转换为八进制字符串（前缀 '0o'）
hex(x): 将整数转换为十六进制字符串（前缀 '0x'）
int(x, base): 将字符串转换为整数，可指定进制

实际应用场景：
1. 计算机底层数据处理
2. 网络协议和地址转换
3. 颜色表示（RGB/HEX）
4. 权限位运算
'''

print("=" * 50)
print("基础用法示例")
print("=" * 50)

# 基础示例
print("1. 十进制转其他进制：")
number = 255
print(f"   十进制 {number} 转换为：")
print(f"   二进制: {bin(number)}")   # 0b11111111
print(f"   八进制: {oct(number)}")   # 0o377
print(f"   十六进制: {hex(number)}") # 0xff

print("\n2. 其他进制转十进制：")
print(f"   二进制 '1010' 转十进制: {int('1010', 2)}")      # 10
print(f"   八进制 '77' 转十进制: {int('77', 8)}")         # 63
print(f"   十六进制 'FF' 转十进制: {int('FF', 16)}")      # 255
print(f"   带前缀的二进制转十进制: {int('0b1010', 2)}")   # 10

print("\n" + "=" * 50)
print("实际应用场景示例")
print("=" * 50)

# 场景1：IP地址转换
def ip_to_binary(ip_address):
    """将IP地址转换为二进制表示"""
    parts = ip_address.split('.')
    binary_parts = []

    for part in parts:
        decimal = int(part)
        binary = bin(decimal)[2:].zfill(8)  # 去掉'0b'前缀，补齐8位
        binary_parts.append(binary)

    return '.'.join(binary_parts)

print("1. IP地址转换：")
print("-" * 30)
ip = "192.168.1.1"
binary_ip = ip_to_binary(ip)
print(f"   IP地址: {ip}")
print(f"   二进制表示: {binary_ip}")
print(f"   验证（转换回来）:")
for binary in binary_ip.split('.'):
    decimal = int(binary, 2)
    print(f"      {binary} -> {decimal}")

# 场景2：颜色表示转换（RGB <-> HEX）
def rgb_to_hex(r, g, b):
    """将RGB颜色值转换为十六进制表示"""
    return f"#{r:02X}{g:02X}{b:02X}"

def hex_to_rgb(hex_color):
    """将十六进制颜色值转换为RGB"""
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return r, g, b

print("\n2. 颜色表示转换：")
print("-" * 30)
rgb_color = (255, 128, 0)  # 橙色
hex_color = rgb_to_hex(*rgb_color)
converted_rgb = hex_to_rgb(hex_color)

print(f"   RGB颜色: {rgb_color}")
print(f"   十六进制: {hex_color}")
print(f"   转换回RGB: {converted_rgb}")

# 场景3：权限位运算
class FilePermissions:
    """使用位运算表示文件权限"""
    READ = 0b100  # 4
    WRITE = 0b010 # 2
    EXECUTE = 0b001 # 1

    def __init__(self):
        self.permissions = 0

    def add_permission(self, permission):
        """添加权限"""
        self.permissions |= permission

    def remove_permission(self, permission):
        """移除权限"""
        self.permissions &= ~permission

    def has_permission(self, permission):
        """检查是否有权限"""
        return (self.permissions & permission) != 0

    def get_permissions_string(self):
        """获取权限字符串表示（类似Linux的rwx）"""
        read = 'r' if self.has_permission(self.READ) else '-'
        write = 'w' if self.has_permission(self.WRITE) else '-'
        execute = 'x' if self.has_permission(self.EXECUTE) else '-'
        return f"{read}{write}{execute} (二进制: {bin(self.permissions)})"

print("\n3. 文件权限位运算：")
print("-" * 30)
perms = FilePermissions()
perms.add_permission(FilePermissions.READ)
perms.add_permission(FilePermissions.WRITE)

print(f"   当前权限: {perms.get_permissions_string()}")
print(f"   是否有读取权限: {perms.has_permission(FilePermissions.READ)}")
print(f"   是否有执行权限: {perms.has_permission(FilePermissions.EXECUTE)}")

# 添加执行权限
perms.add_permission(FilePermissions.EXECUTE)
print(f"   添加执行权限后: {perms.get_permissions_string()}")

# 场景4：网络子网掩码计算
def calculate_network_address(ip, subnet_mask):
    """计算网络地址（IP地址和子网掩码的按位与）"""
    ip_parts = [int(part) for part in ip.split('.')]
    mask_parts = [int(part) for part in subnet_mask.split('.')]

    network_parts = []
    for ip_part, mask_part in zip(ip_parts, mask_parts):
        network_parts.append(ip_part & mask_part)

    return '.'.join(map(str, network_parts))

print("\n4. 网络子网掩码计算：")
print("-" * 30)
ip_address = "192.168.1.100"
subnet_mask = "255.255.255.0"
network_addr = calculate_network_address(ip_address, subnet_mask)

print(f"   IP地址: {ip_address}")
print(f"   子网掩码: {subnet_mask}")
print(f"   网络地址: {network_addr}")

# 显示二进制表示
print(f"\n   二进制表示:")
print(f"   IP地址: {ip_to_binary(ip_address)}")
print(f"   子网掩码: {ip_to_binary(subnet_mask)}")
print(f"   网络地址: {ip_to_binary(network_addr)}")

print("\n" + "=" * 50)
print("进阶技巧")
print("=" * 50)

# 技巧1：格式化输出
print("1. 格式化进制输出：")
num = 42
print(f"   十进制: {num:d}")    # 42
print(f"   二进制: {num:b}")    # 101010
print(f"   八进制: {num:o}")    # 52
print(f"   十六进制(小写): {num:x}")  # 2a
print(f"   十六进制(大写): {num:X}")  # 2A

# 技巧2：处理负数
print("\n2. 负数的进制表示：")
negative = -10
print(f"   -10 的二进制: {bin(negative)}")   # -0b1010
print(f"   -10 的十六进制: {hex(negative)}") # -0xa

# 技巧3：大数处理
print("\n3. 大数处理：")
big_number = 2**32 - 1  # 4294967295
print(f"   2^32 - 1 = {big_number}")
print(f"   二进制: {bin(big_number)}")
print(f"   十六进制: {hex(big_number)}")

# 技巧4：自定义进制转换
def convert_base(number, base):
    """将十进制数转换为任意进制（2-36）"""
    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if number == 0:
        return "0"

    result = ""
    is_negative = number < 0
    number = abs(number)

    while number > 0:
        remainder = number % base
        result = digits[remainder] + result
        number //= base

    if is_negative:
        result = "-" + result

    return result

print("\n4. 自定义进制转换（2-36进制）：")
test_number = 12345
for base in [2, 8, 16, 20, 36]:
    converted = convert_base(test_number, base)
    print(f"   {test_number} 的 {base} 进制: {converted}")

# 交互式示例
print("\n" + "=" * 50)
print("交互式进制转换")
print("=" * 50)

try:
    user_input = input("请输入一个十进制整数（直接回车使用默认值255）: ")
    if user_input.strip() == "":
        user_num = 255
    else:
        user_num = int(user_input)

    print(f"\n您输入的数字: {user_num}")
    print(f"二进制: {bin(user_num)}")
    print(f"八进制: {oct(user_num)}")
    print(f"十六进制: {hex(user_num)}")

    # 显示不同进制的值
    print(f"\n不同进制的值:")
    print(f"二进制值: {int(bin(user_num), 2)}")
    print(f"八进制值: {int(oct(user_num), 8)}")
    print(f"十六进制值: {int(hex(user_num), 16)}")

except ValueError:
    print("❌ 输入无效，请输入一个有效的整数！")