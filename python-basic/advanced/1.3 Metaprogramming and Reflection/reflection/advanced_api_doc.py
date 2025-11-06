import sys,os

current_dir = os.path.dirname(os.path.abspath(__file__))

from api_framework import APIFramework, DynamicAPIMeta,UserAPI

project_root = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.insert(0, project_root)

from metaclass.orm_demo import Model

from typing import Dict, Type


class AdvancedAPIMeta(DynamicAPIMeta):
    """增强的API元类 - 自动生成OpenAPI文档"""
    
    @classmethod
    def _generate_swagger_docs(cls, model_class: Type['Model']):
        """自动生成OpenAPI文档"""
        schema = {
            model_class.__name__: {
                "type": "object",
                "properties": {
                    field_name: {"type": cls._python_type_to_swagger(field.field_type)}
                    for field_name, field in model_class._fields.items()
                }
            }
        }
        
        print(f"📚 生成OpenAPI文档: {schema}")
        return schema
    
    @staticmethod
    def _python_type_to_swagger(py_type):
        """Python类型到Swagger类型映射"""
        type_map = {
            int: "integer",
            str: "string", 
            float: "number",
            bool: "boolean"
        }
        return type_map.get(py_type, "string")
    
    @classmethod
    def _generate_serialization(cls, model_class: Type['Model']):
        """自动生成序列化方法"""
        
        def to_dict(self):
            """将对象序列化为字典"""
            return {
                field_name: getattr(self, field_name)
                for field_name in model_class._fields
            }
        
        @classmethod
        def from_dict(cls, data: Dict):
            """从字典反序列化对象"""
            return cls(**data)
        
        # 添加序列化方法
        model_class.to_dict = to_dict
        model_class.from_dict = from_dict

# 测试完整的动态API框架
def test_dynamic_api_framework():
    print("=== 动态API框架测试 ===")
    
    # 查看自动生成的API端点
    print("🌐 自动生成的API端点:")
    for path, route_info in APIFramework._routes.items():
        print(f"  {path} -> {route_info['func'].__name__}")
    
    # 模拟API请求
    print("\n🔧 模拟API调用:")
    UserAPI.get_all()
    UserAPI.get_by_id(1)
    UserAPI.create()
    UserAPI.update(1)
    UserAPI.delete(1)
    
    # 启动API服务器
    print("\n🚀 启动服务器:")
    APIFramework.run()

test_dynamic_api_framework()