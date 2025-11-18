from abc import ABC, abstractmethod
from typing import Type, Dict, List, Callable
import asyncio
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

import sys,os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.insert(0, project_root)

from DDD.ddd_demo import OrderConfirmedEvent, Money, DomainEvent

class EventBus:
    """事件总线 - 领域事件的发布/订阅机制"""
    
    def __init__(self):
        self._subscribers: Dict[Type[DomainEvent], List[Callable]] = {}
        self._executor = ThreadPoolExecutor(max_workers=10)
    
    def subscribe(self, event_type: Type[DomainEvent], handler: Callable):
        """订阅事件"""
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(handler)
    
    def publish(self, event: DomainEvent):
        """发布事件 - 异步处理"""
        event_type = type(event)
        
        if event_type in self._subscribers:
            for handler in self._subscribers[event_type]:
                # 异步执行事件处理
                self._executor.submit(handler, event)
    
    async def publish_async(self, event: DomainEvent):
        """异步发布事件"""
        event_type = type(event)
        
        if event_type in self._subscribers:
            tasks = []
            for handler in self._subscribers[event_type]:
                # 创建异步任务
                task = asyncio.create_task(self._run_handler_async(handler, event))
                tasks.append(task)
            
            await asyncio.gather(*tasks)
    
    async def _run_handler_async(self, handler: Callable, event: DomainEvent):
        """异步运行事件处理器"""
        try:
            #  if the handler is an async function
            if asyncio.iscoroutinefunction(handler):
                await handler(event)
            else:
                # 同步函数在线程池中运行
                await asyncio.get_event_loop().run_in_executor(
                    self._executor, handler, event
                )
        except Exception as e:
            print(f"❌ 事件处理错误: {e}")

# 事件处理器
class EmailNotificationHandler:
    """邮件通知事件处理器"""
    
    def handle_order_confirmed(self, event: OrderConfirmedEvent):
        """处理订单确认事件"""
        print(f"📧 发送订单确认邮件给客户 {event.customer_id}")
        print(f"   订单号: {event.order_id}, 金额: {event.total_amount.amount}")
        # 实际发送邮件逻辑...

class InventoryUpdateHandler:
    """库存更新事件处理器"""
    
    def handle_order_confirmed(self, event: OrderConfirmedEvent):
        """处理订单确认事件 - 更新库存"""
        print(f"📦 更新库存系统，订单: {event.order_id}")
        # 实际库存更新逻辑...

class AnalyticsHandler:
    """数据分析事件处理器"""
    
    async def handle_order_confirmed_async(self, event: OrderConfirmedEvent):
        """异步处理订单确认事件 - 数据分析"""
        print(f"📊 异步分析订单数据: {event.order_id}")
        await asyncio.sleep(0.1)  # 模拟异步操作
        print(f"📈 订单分析完成: {event.order_id}")

# 测试事件驱动架构
def test_event_driven_architecture():
    print("=== 事件驱动架构测试 ===")
    
    # 创建事件总线
    event_bus = EventBus()
    
    # 创建事件处理器
    email_handler = EmailNotificationHandler()
    inventory_handler = InventoryUpdateHandler()
    analytics_handler = AnalyticsHandler()
    
    # 订阅事件
    event_bus.subscribe(OrderConfirmedEvent, email_handler.handle_order_confirmed)
    event_bus.subscribe(OrderConfirmedEvent, inventory_handler.handle_order_confirmed)
    event_bus.subscribe(OrderConfirmedEvent, analytics_handler.handle_order_confirmed_async)
    
    # 创建并发布事件
    order_event = OrderConfirmedEvent(
        order_id="order_123",
        customer_id="customer_456",
        total_amount=Money(299.7),
        confirmed_at=datetime.now()
    )
    
    print("🚀 发布订单确认事件...")
    event_bus.publish(order_event)
    
    # 异步发布
    async def async_publish():
        await event_bus.publish_async(order_event)
        print("✅ 异步事件发布完成")
    
    # 运行异步测试
    asyncio.run(async_publish())


if __name__ == "__main__":
    test_event_driven_architecture()