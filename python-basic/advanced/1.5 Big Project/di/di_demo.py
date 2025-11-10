from abc import ABC, abstractmethod
from typing import Type, TypeVar, Generic
from dataclasses import dataclass

T = TypeVar('T')

class DependencyContainer:
    """简单的依赖注入容器"""
    def __init__(self):
        self._dependencies = {}
        self._singletons = {}
    
    def register(self, interface: Type, implementation: Type):
        """注册依赖关系"""
        self._dependencies[interface] = implementation
    
    def register_singleton(self, interface: Type, implementation: Type):
        """注册单例依赖"""
        self._dependencies[interface] = implementation
        # 立即创建单例实例
        self._singletons[interface] = implementation()
    
    def resolve(self, interface: Type) -> object:
        """解析依赖"""
        if interface in self._singletons:
            return self._singletons[interface]
        
        if interface in self._dependencies:
            implementation = self._dependencies[interface]
            return implementation()
        
        raise ValueError(f"未注册的依赖: {interface}")

# 定义抽象接口
class EmailService(ABC):
    @abstractmethod
    def send_email(self, to: str, subject: str, body: str) -> bool:
        pass

class DatabaseService(ABC):
    @abstractmethod
    def get_connection(self):
        pass

# 具体实现
class SMTPEmailService(EmailService):
    def send_email(self, to: str, subject: str, body: str) -> bool:
        print(f"📧 通过SMTP发送邮件到 {to}: {subject}")
        return True

class PostgreSQLService(DatabaseService):
    def get_connection(self):
        print("🔗 获取PostgreSQL连接")
        return "postgresql_connection"

# 业务服务使用依赖注入
class UserRegistrationService:
    def __init__(self, email_service: EmailService, db_service: DatabaseService):
        self.email_service = email_service
        self.db_service = db_service
    
    def register_user(self, username: str, email: str) -> bool:
        print(f"👤 注册用户: {username}")
        
        # 使用注入的服务
        connection = self.db_service.get_connection()
        # 保存用户到数据库...
        
        # 发送欢迎邮件
        self.email_service.send_email(
            to=email,
            subject="欢迎注册",
            body=f"您好 {username}，欢迎使用我们的服务！"
        )
        
        return True

# 配置依赖注入容器
def configure_dependencies():
    container = DependencyContainer()
    
    # 注册依赖
    container.register(EmailService, SMTPEmailService)
    container.register_singleton(DatabaseService, PostgreSQLService)
    
    return container

# 测试依赖注入
def test_dependency_injection():
    print("=== 依赖注入测试 ===")
    
    container = configure_dependencies()
    
    # 手动创建服务（演示依赖解析）
    email_service = container.resolve(EmailService)
    db_service = container.resolve(DatabaseService)
    
    # 创建业务服务
    registration_service = UserRegistrationService(email_service, db_service)
    registration_service.register_user("张三", "zhangsan@example.com")
    
    # 验证单例模式
    db_service2 = container.resolve(DatabaseService)
    print(f"🔍 数据库服务单例验证: {db_service is db_service2}")

test_dependency_injection()