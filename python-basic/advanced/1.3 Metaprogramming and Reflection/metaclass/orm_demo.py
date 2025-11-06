class Field:
    """字段描述符 - 负责数据库字段映射"""
    def __init__(self, name=None, field_type=str, primary_key=False, nullable=True):
        self.name = name
        self.field_type = field_type
        self.primary_key = primary_key
        self.nullable = nullable
        self._value = None
    
    def __set_name__(self, owner, name):
        if self.name is None:
            self.name = name  # 自动设置字段名
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self._value
    
    def __set__(self, instance, value):
        # 类型验证
        if not isinstance(value, self.field_type) and value is not None:
            raise TypeError(f"字段 {self.name} 需要 {self.field_type} 类型")
        # 空值验证
        if value is None and not self.nullable:
            raise ValueError(f"字段 {self.name} 不能为空")
        
        self._value = value

class ModelMeta(type):
    """模型元类 - 自动收集字段并生成表结构"""
    def __new__(cls, name, bases, namespace):
        # 收集所有Field实例
        fields = {}
        primary_key = None
        
        for key, value in namespace.items():
            if isinstance(value, Field):
                if value.name is None:
                    value.name = key
                fields[key] = value
                
                # 标识主键
                if value.primary_key:
                    if primary_key is not None:
                        raise ValueError("只能有一个主键字段")
                    primary_key = value.name
        
        namespace['_fields'] = fields
        namespace['_table_name'] = name.lower()  # 表名默认为类名小写
        namespace['_primary_key'] = primary_key
        
        # 自动生成SQL表创建语句
        namespace['_create_table_sql'] = cls._generate_create_sql(name, fields)
        
        return super().__new__(cls, name, bases, namespace)
    
    @staticmethod
    def _generate_create_sql(class_name, fields):
        """生成CREATE TABLE SQL语句"""
        columns = []
        for field_name, field in fields.items():
            column_def = f"{field.name} {field.field_type.__name__.upper()}"
            if field.primary_key:
                column_def += " PRIMARY KEY"
            if not field.nullable:
                column_def += " NOT NULL"
            columns.append(column_def)
        
        return f"CREATE TABLE {class_name.lower()} ({', '.join(columns)})"

class Model(metaclass=ModelMeta):
    """模型基类"""
    
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if key in self._fields:
                setattr(self, key, value)
    
    def save(self):
        """模拟保存到数据库"""
        field_values = {}
        for field_name in self._fields:
            field_values[field_name] = getattr(self, field_name)
        
        print(f"💾 保存到表 {self._table_name}: {field_values}")
        return True
    
    @classmethod
    def create_table(cls):
        """创建数据库表"""
        print(f"🛠️ 执行SQL: {cls._create_table_sql}")
        return True
    
    def __repr__(self):
        fields_repr = ', '.join(f"{k}={getattr(self, k)}" for k in self._fields)
        return f"{self.__class__.__name__}({fields_repr})"

# 使用ORM框架定义数据模型
class User(Model):
    id = Field(field_type=int, primary_key=True)
    name = Field(field_type=str, nullable=False)
    age = Field(field_type=int, nullable=True)
    email = Field(field_type=str, nullable=True)

class Product(Model):
    id = Field(field_type=int, primary_key=True)
    title = Field(field_type=str, nullable=False)
    price = Field(field_type=float, nullable=False)


# 测试元类自动生成的功能
def test_orm_framework():
    print("=== ORM框架测试 ===")
    
    # 查看自动生成的元数据
    print(f"📋 User模型字段: {list(User._fields.keys())}")
    print(f"🔑 User主键字段: {User._primary_key}")
    print(f"🗂️ User表名: {User._table_name}")
    print(f"📜 User建表SQL: {User._create_table_sql}")
    
    # 创建表
    User.create_table()
    
    # 创建实例并保存
    user = User(id=1, name="张三", age=25, email="zhangsan@example.com")
    print(f"👤 创建用户: {user}")
    user.save()
    
    # 类型验证测试
    try:
        invalid_user = User(id="not_a_number", name="李四")  # 应该报错
    except TypeError as e:
        print(f"❌ 类型验证生效: {e}")

test_orm_framework()