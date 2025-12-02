'''
all() 和 any() 函数详解

all(iterable): 当可迭代对象中所有元素都为真时返回 True，否则返回 False
any(iterable): 当可迭代对象中至少有一个元素为真时返回 True，否则返回 False

实际应用场景：
1. 数据验证：检查所有输入是否有效
2. 权限检查：检查用户是否有任意权限
3. 条件判断：简化复杂的逻辑判断
'''

print("=" * 50)
print("基础用法示例")
print("=" * 50)

# 基础示例
list1 = [True, True, False, True]
print(f"all([True, True, False, True]) = {all(list1)}")
# False - 因为有一个 False

list2 = [False, True, False]
print(f"any([False, True, False]) = {any(list2)}")
# True - 因为至少有一个 True

print("\n" + "=" * 50)
print("实际应用场景示例")
print("=" * 50)

# 场景1：用户注册数据验证
def validate_user_data(username, email, password, age):
    """验证用户注册数据是否全部有效"""
    validations = [
        len(username) >= 3,           # 用户名至少3个字符
        '@' in email,                 # 邮箱必须包含@
        len(password) >= 8,           # 密码至少8位
        age >= 18                     # 年龄必须满18岁
    ]

    if all(validations):
        print("✅ 所有数据验证通过！")
        return True
    else:
        print("❌ 数据验证失败，请检查：")
        if not validations[0]: print("  - 用户名至少需要3个字符")
        if not validations[1]: print("  - 邮箱格式不正确")
        if not validations[2]: print("  - 密码至少需要8位")
        if not validations[3]: print("  - 年龄必须满18岁")
        return False

print("\n1. 用户注册数据验证：")
print("-" * 30)
validate_user_data("Tom", "tom@example.com", "12345678", 20)  # 应该通过
validate_user_data("Li", "invalid-email", "123", 16)          # 应该失败

# 场景2：权限检查系统
class User:
    def __init__(self, name, permissions):
        self.name = name
        self.permissions = permissions  # 权限列表

    def has_any_permission(self, required_permissions):
        """检查用户是否有任意所需权限"""
        return any(perm in self.permissions for perm in required_permissions)

    def has_all_permissions(self, required_permissions):
        """检查用户是否有所需的所有权限"""
        return all(perm in self.permissions for perm in required_permissions)

print("\n2. 权限检查系统：")
print("-" * 30)
user = User("Alice", ["read", "write", "delete"])

# 检查是否有任意管理权限
admin_perms = ["admin", "superuser"]
print(f"{user.name} 是否有管理权限: {user.has_any_permission(admin_perms)}")

# 检查是否有所有编辑权限
edit_perms = ["read", "write"]
print(f"{user.name} 是否有所有编辑权限: {user.has_all_permissions(edit_perms)}")

# 场景3：考试成绩分析
def analyze_exam_scores(scores, passing_score=60):
    """分析考试成绩"""
    all_passed = all(score >= passing_score for score in scores)
    anyone_passed = any(score >= passing_score for score in scores)

    print(f"\n3. 考试成绩分析（及格线: {passing_score}分）：")
    print(f"   所有学生都及格: {all_passed}")
    print(f"   至少有一个学生及格: {anyone_passed}")
    print(f"   具体成绩: {scores}")

analyze_exam_scores([85, 92, 78, 45, 90])  # 有人不及格
analyze_exam_scores([75, 82, 68, 71, 80])  # 全部及格

print("\n" + "=" * 50)
print("进阶技巧")
print("=" * 50)

# 技巧1：与生成器表达式结合
numbers = [1, 3, 5, 7, 9]
all_odd = all(n % 2 == 1 for n in numbers)  # 检查是否都是奇数
any_even = any(n % 2 == 0 for n in numbers)  # 检查是否有偶数
print(f"列表 {numbers} 是否都是奇数: {all_odd}")
print(f"列表 {numbers} 是否有偶数: {any_even}")

# 技巧2：空列表的特殊情况
print(f"\n空列表的特殊情况：")
print(f"all([]) = {all([])}")   # True - 空列表没有假元素
print(f"any([]) = {any([])}")   # False - 空列表没有真元素

# 技巧3：与其他内置函数结合
data = ["apple", "banana", "cherry", ""]
all_non_empty = all(data)  # 等价于 all(len(item) > 0 for item in data)
print(f"\n检查列表是否都非空: {all_non_empty}")