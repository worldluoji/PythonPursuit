class SQLQuery:
    """复杂SQL查询对象"""
    def __init__(self):
        self.select = "*"
        self.table = ""
        self.where_conditions = []
        self.limit_value = None
    
    def __str__(self):
        query = f"SELECT {self.select} FROM {self.table}"
        if self.where_conditions:
            query += f" WHERE {' AND '.join(self.where_conditions)}"
        if self.limit_value:
            query += f" LIMIT {self.limit_value}"
        return query

class SQLQueryBuilder:
    """SQL查询建造者"""
    def __init__(self):
        self.query = SQLQuery()
    
    def select(self, columns: str) -> 'SQLQueryBuilder':
        self.query.select = columns
        return self  # 返回self支持链式调用
    
    def from_table(self, table: str) -> 'SQLQueryBuilder':
        self.query.table = table
        return self
    
    def where(self, condition: str) -> 'SQLQueryBuilder':
        self.query.where_conditions.append(condition)
        return self
    
    def limit(self, limit: int) -> 'SQLQueryBuilder':
        self.query.limit_value = limit
        return self
    
    def build(self) -> SQLQuery:
        return self.query

# Pythonic的替代方案：使用@dataclass和流畅接口
from dataclasses import dataclass
from typing import List, Optional

'''
@dataclass 是 Python 3.7+ 中引入的一个装饰器，
它能自动为类生成常见的特殊方法，大大简化了类的定义
'''
@dataclass
class PythonicSQLQuery:
    select: str = "*"
    table: str = ""
    where_conditions: List[str] = None
    limit_value: Optional[int] = None
    
    def __post_init__(self):
        if self.where_conditions is None:
            self.where_conditions = []
    
    def __str__(self):
        # 相同的字符串表示逻辑
        pass

# 测试建造者模式
def test_builder_pattern():
    print("=== 建造者模式测试 ===")
    
    # 传统建造者模式
    builder = SQLQueryBuilder()
    query = (builder
        .select("id, name, email")
        .from_table("users")
        .where("age > 18")
        .where("status = 'active'")
        .limit(10)
        .build())
    
    print(f"🛠️ 构建的查询: {query}")
    
    # 更Pythonic的方式：使用字典和**解包
    def create_sql_query(**kwargs):
        query = SQLQuery()
        for key, value in kwargs.items():
            if hasattr(query, key):
                setattr(query, key, value)
        return query
    
    simple_query = create_sql_query(
        select="COUNT(*)",
        table="orders",
        where_conditions=["created_at > '2024-01-01'"]
    )
    print(f"🐍 Pythonic查询: {simple_query}")

test_builder_pattern()