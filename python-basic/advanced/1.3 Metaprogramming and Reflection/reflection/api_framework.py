from typing import Dict, List, Type
import sys,os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.insert(0, project_root)

from metaclass.orm_demo import Field,Model

# 假设我们使用Flask-like的API（简化演示）
class APIFramework:
    """模拟Web框架基类"""
    _routes = {}
    
    @classmethod
    def route(cls, path: str, methods: List[str] = None):
        def decorator(func):
            cls._routes[path] = {'func': func, 'methods': methods or ['GET']}
            return func
        return decorator
    
    @classmethod
    def run(cls):
        print("🚀 启动API服务器...")
        for path, route_info in cls._routes.items():
            print(f"📍 注册路由: {path} -> {route_info['func'].__name__}")

class DynamicAPIMeta(type):
    """API框架元类 - 自动生成CRUD端点"""
    
    def __new__(cls, name, bases, namespace):
        # 先执行ORM的元类逻辑
        new_class = super().__new__(cls, name, bases, namespace)
        
        if name != 'RESTModel':  # 避免对基类生成API
            cls._generate_crud_methods(new_class)
            cls._register_api_routes(new_class)
        
        return new_class
    
    @classmethod
    def _generate_crud_sql(cls, model_class: Type['Model']) -> Dict[str, str]:
        """生成CRUD SQL模板"""
        table_name = model_class._table_name
        fields = list(model_class._fields.keys())
        primary_key = model_class._primary_key
        
        return {
            'select_all': f"SELECT {', '.join(fields)} FROM {table_name}",
            'select_by_id': f"SELECT {', '.join(fields)} FROM {table_name} WHERE {primary_key} = ?",
            'insert': f"INSERT INTO {table_name} ({', '.join(fields)}) VALUES ({', '.join(['?' for _ in fields])})",
            'update': f"UPDATE {table_name} SET {', '.join([f'{f} = ?' for f in fields if f != primary_key])} WHERE {primary_key} = ?",
            'delete': f"DELETE FROM {table_name} WHERE {primary_key} = ?"
        }
    
    @classmethod
    def _generate_crud_methods(cls, model_class: Type['Model']):
        """动态生成CRUD方法"""
        sql_templates = cls._generate_crud_sql(model_class)
        
        # 生成GET方法（获取所有记录）
        @APIFramework.route(f"/api/{model_class._table_name}", methods=['GET'])
        @classmethod
        def get_all(cls):
            """获取所有记录"""
            print(f"📋 执行SQL: {sql_templates['select_all']}")
            # 模拟数据库查询结果
            return {"data": [], "sql": sql_templates['select_all']}
        
        # 生成GET方法（根据ID获取）
        @APIFramework.route(f"/api/{model_class._table_name}/<id>", methods=['GET'])
        @classmethod
        def get_by_id(cls, id):
            """根据ID获取记录"""
            sql = sql_templates['select_by_id']
            print(f"🔍 执行SQL: {sql} 参数: {id}")
            return {"data": {"id": id}, "sql": sql}
        
        # 生成POST方法（创建记录）
        @APIFramework.route(f"/api/{model_class._table_name}", methods=['POST'])
        @classmethod
        def create(cls):
            """创建新记录"""
            sql = sql_templates['insert']
            print(f"➕ 执行SQL: {sql}")
            return {"message": "创建成功", "sql": sql}
        
        # 生成PUT方法（更新记录）
        @APIFramework.route(f"/api/{model_class._table_name}/<id>", methods=['PUT'])
        @classmethod
        def update(cls, id):
            """更新记录"""
            sql = sql_templates['update']
            print(f"✏️ 执行SQL: {sql} 参数: {id}")
            return {"message": "更新成功", "sql": sql}
        
        # 生成DELETE方法（删除记录）
        @APIFramework.route(f"/api/{model_class._table_name}/<id>", methods=['DELETE'])
        @classmethod
        def delete(cls, id):
            """删除记录"""
            sql = sql_templates['delete']
            print(f"🗑️ 执行SQL: {sql} 参数: {id}")
            return {"message": "删除成功", "sql": sql}
        
        # 将方法动态添加到类中
        model_class.get_all = get_all
        model_class.get_by_id = get_by_id
        model_class.create = create
        model_class.update = update
        model_class.delete = delete
    
    @classmethod
    def _register_api_routes(cls, model_class: Type['Model']):
        """注册API路由到框架"""
        print(f"🔄 为 {model_class.__name__} 注册API路由...")

# 更新Model基类使用新的元类
class RESTModel(Model, metaclass=DynamicAPIMeta):
    """支持RESTful API的模型基类"""
    pass

# 使用动态API框架定义模型
class UserAPI(RESTModel):
    id = Field(field_type=int, primary_key=True)
    name = Field(field_type=str, nullable=False)
    age = Field(field_type=int, nullable=True)

class ProductAPI(RESTModel):
    id = Field(field_type=int, primary_key=True)
    title = Field(field_type=str, nullable=False)
    price = Field(field_type=float, nullable=False)