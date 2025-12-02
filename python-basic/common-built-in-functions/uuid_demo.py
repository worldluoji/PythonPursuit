'''
UUID（通用唯一识别码）详解

UUID（Universally Unique Identifier）是一个128位的标识符，用于在分布式系统中唯一标识信息。

UUID版本：
1. uuid1(): 基于时间戳和MAC地址
2. uuid3(): 基于MD5哈希和命名空间
3. uuid4(): 基于随机数（最常用）
4. uuid5(): 基于SHA-1哈希和命名空间

特点：
1. 全球唯一性：几乎不可能重复
2. 标准化：遵循RFC 4122标准
3. 多种版本：适应不同需求
4. 字符串表示：32位十六进制数字，用连字符分隔

实际应用场景：
1. 数据库主键：替代自增ID
2. 分布式系统：唯一标识请求/会话
3. 文件命名：避免文件名冲突
4. 安全令牌：生成临时访问令牌
'''

import uuid
import hashlib

print("=" * 50)
print("基础用法示例")
print("=" * 50)

# 基础示例
print("1. 不同版本的UUID：")
print(f"   uuid1() (基于时间戳和MAC地址): {uuid.uuid1()}")
print(f"   uuid4() (基于随机数): {uuid.uuid4()}")
print(f"   uuid4() 另一个: {uuid.uuid4()}")

# 命名空间UUID
print("\n2. 命名空间UUID（uuid3和uuid5）：")
# 预定义的命名空间
DNS_NAMESPACE = uuid.NAMESPACE_DNS
URL_NAMESPACE = uuid.NAMESPACE_URL

name = "example.com"
uuid3_dns = uuid.uuid3(DNS_NAMESPACE, name)
uuid5_dns = uuid.uuid5(DNS_NAMESPACE, name)

print(f"   域名: {name}")
print(f"   uuid3(DNS, '{name}'): {uuid3_dns}")
print(f"   uuid5(DNS, '{name}'): {uuid5_dns}")
print(f"   注意: 相同输入总是生成相同的UUID")

print("\n" + "=" * 50)
print("实际应用场景示例")
print("=" * 50)

# 场景1：数据库记录唯一标识
class DatabaseRecord:
    """使用UUID作为数据库记录的唯一标识"""

    def __init__(self, data):
        self.id = uuid.uuid4()  # 使用uuid4作为主键
        self.data = data
        self.created_at = uuid.uuid1().time  # 使用uuid1的时间部分

    def __str__(self):
        return f"Record(id={self.id}, data={self.data}, created_at={self.created_at})"

print("1. 数据库记录唯一标识：")
print("-" * 30)

records = [
    DatabaseRecord({"name": "Alice", "age": 30}),
    DatabaseRecord({"name": "Bob", "age": 25}),
    DatabaseRecord({"name": "Charlie", "age": 35})
]

for i, record in enumerate(records, 1):
    print(f"   记录{i}: {record}")

# 场景2：分布式请求跟踪
class RequestTracker:
    """分布式系统中的请求跟踪"""

    def __init__(self):
        self.request_id = uuid.uuid4()
        self.correlation_id = uuid.uuid4()  # 用于关联多个请求
        self.trace_id = self._generate_trace_id()

    def _generate_trace_id(self):
        """生成跟踪ID（结合时间戳和随机数）"""
        timestamp = uuid.uuid1().time
        random_part = uuid.uuid4().hex[:16]
        return f"{timestamp:x}-{random_part}"

    def get_headers(self):
        """获取用于HTTP头的跟踪信息"""
        return {
            'X-Request-ID': str(self.request_id),
            'X-Correlation-ID': str(self.correlation_id),
            'X-Trace-ID': self.trace_id
        }

print("\n2. 分布式请求跟踪：")
print("-" * 30)
tracker = RequestTracker()
headers = tracker.get_headers()

print("   生成的跟踪头信息:")
for key, value in headers.items():
    print(f"     {key}: {value}")

# 场景3：安全文件命名
def generate_unique_filename(original_filename, user_id=None):
    """生成唯一的文件名，避免冲突"""
    import os
    import time

    # 获取文件扩展名
    name, ext = os.path.splitext(original_filename)

    # 生成唯一部分
    if user_id:
        # 基于用户ID和时间的UUID
        namespace = uuid.NAMESPACE_URL
        unique_string = f"{user_id}-{time.time()}"
        unique_id = uuid.uuid5(namespace, unique_string).hex[:8]
    else:
        # 完全随机的UUID
        unique_id = uuid.uuid4().hex[:8]

    # 组合新文件名
    timestamp = int(time.time())
    new_filename = f"{name}_{timestamp}_{unique_id}{ext}"

    return new_filename

print("\n3. 安全文件命名：")
print("-" * 30)

filenames = ["document.pdf", "image.jpg", "data.csv"]
user_id = "user123"

for filename in filenames:
    unique_name = generate_unique_filename(filename, user_id)
    print(f"   原始: {filename}")
    print(f"   唯一: {unique_name}")
    print()

# 场景4：会话管理
class UserSession:
    """用户会话管理"""

    def __init__(self, username):
        self.username = username
        self.session_id = uuid.uuid4()
        self.created_at = uuid.uuid1().time
        self.expires_at = self.created_at + (3600 * 24 * 7)  # 7天后过期
        self.csrf_token = uuid.uuid4().hex[:32]

    def is_valid(self):
        """检查会话是否有效"""
        current_time = uuid.uuid1().time
        return current_time < self.expires_at

    def refresh(self):
        """刷新会话"""
        self.expires_at = uuid.uuid1().time + (3600 * 24 * 7)

    def __str__(self):
        status = "有效" if self.is_valid() else "已过期"
        return f"Session(username={self.username}, id={self.session_id}, status={status})"

print("4. 用户会话管理：")
print("-" * 30)

session = UserSession("alice@example.com")
print(f"   创建的会话: {session}")
print(f"   CSRF令牌: {session.csrf_token}")

# 模拟时间流逝（这里只是演示，实际中时间会自然流逝）
print(f"   会话是否有效: {session.is_valid()}")

# 场景5：批量生成唯一码
def generate_batch_codes(count, prefix="CODE", version=4):
    """批量生成唯一代码"""
    codes = []
    for i in range(count):
        if version == 1:
            uid = uuid.uuid1()
        elif version == 3:
            uid = uuid.uuid3(uuid.NAMESPACE_DNS, f"{prefix}-{i}")
        elif version == 4:
            uid = uuid.uuid4()
        elif version == 5:
            uid = uuid.uuid5(uuid.NAMESPACE_DNS, f"{prefix}-{i}")
        else:
            raise ValueError("不支持的UUID版本")

        # 取前8位作为短代码
        short_code = uid.hex[:8].upper()
        codes.append(f"{prefix}-{short_code}")

    return codes

print("\n5. 批量生成唯一码：")
print("-" * 30)

batch_codes = generate_batch_codes(5, "INV", version=4)
print("   生成的邀请码:")
for code in batch_codes:
    print(f"     {code}")

print("\n" + "=" * 50)
print("进阶技巧")
print("=" * 50)

# 技巧1：UUID属性访问
print("1. UUID对象属性访问：")
uid = uuid.uuid4()
print(f"   UUID: {uid}")
print(f"   十六进制: {uid.hex}")
print(f"   整数: {uid.int}")
print(f"   字节: {uid.bytes}")
print(f"   变体: {uid.variant}")  # 指定UUID布局
print(f"   版本: {uid.version}")  # UUID版本号

# 技巧2：UUID比较和排序
print("\n2. UUID比较和排序：")
uuids = [uuid.uuid4() for _ in range(5)]
sorted_uuids = sorted(uuids)

print("   生成的UUID（排序前）:")
for u in uuids:
    print(f"     {u}")

print("\n   排序后:")
for u in sorted_uuids:
    print(f"     {u}")

# 技巧3：从字符串创建UUID
print("\n3. 从字符串创建UUID：")
uuid_str = "12345678-1234-5678-1234-567812345678"
try:
    uuid_obj = uuid.UUID(uuid_str)
    print(f"   字符串: {uuid_str}")
    print(f"   创建的UUID对象: {uuid_obj}")
    print(f"   验证: {uuid_obj == uuid.UUID(uuid_str)}")
except ValueError as e:
    print(f"   错误: {e}")

# 无效UUID示例
invalid_str = "not-a-valid-uuid"
try:
    uuid.UUID(invalid_str)
except ValueError as e:
    print(f"\n   无效UUID字符串 '{invalid_str}': {e}")

# 技巧4：自定义UUID生成
def generate_custom_uuid(namespace, name, hash_func='sha1'):
    """自定义UUID生成（类似uuid3/uuid5）"""
    if hash_func == 'md5':
        hash_obj = hashlib.md5(namespace.bytes + name.encode())
        version = 3
    elif hash_func == 'sha1':
        hash_obj = hashlib.sha1(namespace.bytes + name.encode())
        version = 5
    else:
        raise ValueError("不支持的哈希函数")

    hash_bytes = hash_obj.digest()

    # 设置版本和变体位
    hash_bytes = bytearray(hash_bytes)
    hash_bytes[6] = (hash_bytes[6] & 0x0F) | (version << 4)  # 设置版本
    hash_bytes[8] = (hash_bytes[8] & 0x3F) | 0x80  # 设置变体为RFC 4122

    return uuid.UUID(bytes=bytes(hash_bytes))

print("\n4. 自定义UUID生成：")
namespace = uuid.NAMESPACE_DNS
name = "custom.example.com"

custom_md5 = generate_custom_uuid(namespace, name, 'md5')
custom_sha1 = generate_custom_uuid(namespace, name, 'sha1')

print(f"   命名空间: {namespace}")
print(f"   名称: {name}")
print(f"   自定义MD5 UUID: {custom_md5}")
print(f"   自定义SHA1 UUID: {custom_sha1}")
print(f"   与标准uuid3比较: {custom_md5 == uuid.uuid3(namespace, name)}")
print(f"   与标准uuid5比较: {custom_sha1 == uuid.uuid5(namespace, name)}")

# 技巧5：UUID性能考虑
print("\n5. UUID性能考虑：")
import time

def benchmark_uuid_generation(count=10000):
    """基准测试不同UUID版本的生成速度"""
    versions = [1, 3, 4, 5]
    results = {}

    for version in versions:
        start_time = time.time()

        if version == 1:
            for _ in range(count):
                uuid.uuid1()
        elif version == 3:
            for i in range(count):
                uuid.uuid3(uuid.NAMESPACE_DNS, f"test-{i}")
        elif version == 4:
            for _ in range(count):
                uuid.uuid4()
        elif version == 5:
            for i in range(count):
                uuid.uuid5(uuid.NAMESPACE_DNS, f"test-{i}")

        elapsed = time.time() - start_time
        results[version] = elapsed

    return results

print("   UUID生成性能比较（生成10,000个）:")
# 注意：实际运行可能较慢，这里只显示概念
print("   uuid1(): 基于时间戳，速度中等")
print("   uuid3(): 基于MD5哈希，需要计算哈希")
print("   uuid4(): 基于随机数，速度最快")
print("   uuid5(): 基于SHA-1哈希，需要计算哈希")

print("\n" + "=" * 50)
print("交互式示例")
print("=" * 50)

try:
    print("生成自定义UUID")
    print("1. 随机UUID (uuid4)")
    print("2. 基于时间的UUID (uuid1)")
    print("3. 基于命名的UUID (uuid3/uuid5)")

    choice = input("请选择UUID类型 (1-3): ")

    if choice == "1":
        count = int(input("要生成多少个UUID? (1-10): "))
        count = max(1, min(10, count))
        print(f"\n生成的UUID:")
        for i in range(count):
            print(f"  {i+1}. {uuid.uuid4()}")

    elif choice == "2":
        uid = uuid.uuid1()
        print(f"\n生成的UUID1: {uid}")
        print(f"时间部分: {uid.time}")
        print(f"时钟序列: {uid.clock_seq}")
        print(f"节点(MAC地址): {uid.node:x}")

    elif choice == "3":
        name = input("请输入名称: ")
        version = input("选择哈希版本 (3=MD5, 5=SHA-1): ")

        if version == "3":
            uid = uuid.uuid3(uuid.NAMESPACE_DNS, name)
            print(f"\n生成的UUID3 (MD5): {uid}")
        elif version == "5":
            uid = uuid.uuid5(uuid.NAMESPACE_DNS, name)
            print(f"\n生成的UUID5 (SHA-1): {uid}")
        else:
            print("无效的版本选择")

        print(f"注意: 相同名称 '{name}' 总是生成相同的UUID")

    else:
        print("无效的选择")

except ValueError as e:
    print(f"错误: {e}")
except Exception as e:
    print(f"发生错误: {e}")