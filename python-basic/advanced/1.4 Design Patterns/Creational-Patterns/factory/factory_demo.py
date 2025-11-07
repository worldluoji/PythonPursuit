from abc import ABC, abstractmethod
from enum import Enum

class NotificationType(Enum):
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"

class Notification(ABC):
    """通知抽象类"""
    @abstractmethod
    def send(self, message: str) -> bool:
        pass

class EmailNotification(Notification):
    def send(self, message: str) -> bool:
        print(f"📧 发送邮件: {message}")
        return True

class SMSNotification(Notification):
    def send(self, message: str) -> bool:
        print(f"📱 发送短信: {message}")
        return True

class PushNotification(Notification):
    def send(self, message: str) -> bool:
        print(f"🔔 发送推送: {message}")
        return True

class NotificationFactory:
    """通知工厂 - 简化对象创建"""
    
    @staticmethod
    def create_notification(notification_type: NotificationType) -> Notification:
        creators = {
            NotificationType.EMAIL: EmailNotification,
            NotificationType.SMS: SMSNotification, 
            NotificationType.PUSH: PushNotification
        }
        
        if notification_type in creators:
            return creators[notification_type]()
        else:
            raise ValueError(f"不支持的的通知类型: {notification_type}")
    
    # Pythonic的替代方案：使用函数而不是类
    @staticmethod
    def create_notification_simple(notification_type: str) -> Notification:
        """更Pythonic的工厂函数"""
        notification_map = {
            "email": EmailNotification,
            "sms": SMSNotification,
            "push": PushNotification
        }
        
        notification_class = notification_map.get(notification_type)
        if notification_class:
            return notification_class()
        raise ValueError(f"未知的通知类型: {notification_type}")

# 测试工厂模式
def test_factory_pattern():
    print("=== 工厂模式测试 ===")
    
    # 使用枚举类型
    email_notification = NotificationFactory.create_notification(NotificationType.EMAIL)
    email_notification.send("Hello via Email!")
    
    # 使用字符串（更Pythonic）
    sms_notification = NotificationFactory.create_notification_simple("sms")
    sms_notification.send("Hello via SMS!")
    
    # 动态扩展：添加新的通知类型
    class WechatNotification(Notification):
        def send(self, message: str) -> bool:
            print(f"💬 微信通知: {message}")
            return True
    
    # 动态注册新类型
    NotificationFactory.create_notification_simple = lambda n_type: (
        WechatNotification() if n_type == "wechat" else 
        globals().get(f"{n_type.title()}Notification")()
    )
    
    wechat_notification = NotificationFactory.create_notification_simple("wechat")
    wechat_notification.send("Hello via WeChat!")

test_factory_pattern()