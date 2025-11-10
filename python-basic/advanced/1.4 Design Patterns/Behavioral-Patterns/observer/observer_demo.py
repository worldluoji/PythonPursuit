from abc import ABC, abstractmethod
from typing import List, Dict, Any
from dataclasses import dataclass
from enum import Enum
import time

@dataclass
class UserEvent:
    """用户事件数据类"""
    event_type: str
    user_id: int
    user_data: Dict[str, Any]
    timestamp: float

class EventType(Enum):
    USER_REGISTERED = "user_registered"
    USER_UPDATED = "user_updated"
    USER_DELETED = "user_deleted"

class EventObserver(ABC):
    """事件观察者抽象类"""
    @abstractmethod
    def update(self, event: UserEvent):
        pass

# 具体观察者实现
class EmailNotificationService(EventObserver):
    """邮件通知服务"""
    def update(self, event: UserEvent):
        if event.event_type == EventType.USER_REGISTERED.value:
            print(f"📧 发送欢迎邮件给用户 {event.user_id}")
            # 实际发送邮件逻辑...

class AuditLogService(EventObserver):
    """审计日志服务"""
    def update(self, event: UserEvent):
        print(f"📝 记录审计日志: {event.event_type} - 用户 {event.user_id}")
        # 实际日志记录逻辑...

class AnalyticsService(EventObserver):
    """数据分析服务"""
    def update(self, event: UserEvent):
        if event.event_type == EventType.USER_REGISTERED.value:
            print(f"📊 更新用户注册统计")
        # 实际数据分析逻辑...

class EventPublisher:
    """事件发布者"""
    def __init__(self):
        self._observers: List[EventObserver] = []
        self._event_history: List[UserEvent] = []
    
    def attach(self, observer: EventObserver) -> None:
        """添加观察者"""
        if observer not in self._observers:
            self._observers.append(observer)
    
    def detach(self, observer: EventObserver) -> None:
        """移除观察者"""
        self._observers.remove(observer)
    
    def notify(self, event: UserEvent) -> None:
        """通知所有观察者"""
        self._event_history.append(event)
        print(f"🔔 发布事件: {event.event_type}")
        
        for observer in self._observers:
            try:
                observer.update(event)
            except Exception as e:
                print(f"❌ 观察者处理错误: {e}")
    
    def publish_user_registered(self, user_id: int, user_data: Dict[str, Any]):
        """发布用户注册事件"""
        event = UserEvent(
            event_type=EventType.USER_REGISTERED.value,
            user_id=user_id,
            user_data=user_data,
            timestamp=time.time()
        )
        self.notify(event)

# Pythonic的观察者模式：使用函数和装饰器
def create_event_system():
    """更Pythonic的事件系统"""
    observers = {}
    
    def subscribe(event_type: str, callback):
        """订阅事件"""
        if event_type not in observers:
            observers[event_type] = []
        observers[event_type].append(callback)
    
    def publish(event_type: str, **data):
        """发布事件"""
        if event_type in observers:
            for callback in observers[event_type]:
                callback(**data)
    
    return subscribe, publish

# 测试观察者模式
def test_observer_pattern():
    print("=== 观察者模式测试 ===")
    
    # 传统观察者模式
    publisher = EventPublisher()
    
    # 注册观察者
    publisher.attach(EmailNotificationService())
    publisher.attach(AuditLogService())
    publisher.attach(AnalyticsService())
    
    # 发布用户注册事件
    publisher.publish_user_registered(
        user_id=123,
        user_data={"name": "张三", "email": "zhangsan@example.com"}
    )
    
    print("\n--- Pythonic版本 ---")
    
    # Pythonic事件系统
    subscribe, publish = create_event_system()
    
    # 订阅事件
    @subscribe("user_registered")
    def send_welcome_email(user_id, user_data):
        print(f"🐍 Pythonic: 发送欢迎邮件给 {user_data['name']}")
    
    @subscribe("user_registered") 
    def log_registration(user_id, user_data):
        print(f"🐍 Pythonic: 记录用户注册日志")
    
    # 发布事件
    publish("user_registered", user_id=456, user_data={"name": "李四"})

test_observer_pattern()