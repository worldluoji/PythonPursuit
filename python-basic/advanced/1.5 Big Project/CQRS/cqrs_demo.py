from typing import List, Dict, Any
from datetime import datetime
from abc import ABC, abstractmethod
import uuid
import sys,os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.insert(0, project_root)

from DDD.ddd_demo import OrderStatus, Order, OrderConfirmedEvent, Money
from eventbus_demo import EventBus

# 命令 - 写操作
class CreateOrderCommand:
    def __init__(self, customer_id: str, items: List[Dict]):
        self.customer_id = customer_id
        self.items = items
        self.command_id = str(uuid.uuid4())
        self.timestamp = datetime.now()

class UpdateOrderStatusCommand:
    def __init__(self, order_id: str, new_status: OrderStatus):
        self.order_id = order_id
        self.new_status = new_status
        self.command_id = str(uuid.uuid4())
        self.timestamp = datetime.now()

# 查询 - 读操作
class GetOrderQuery:
    def __init__(self, order_id: str):
        self.order_id = order_id

class GetCustomerOrdersQuery:
    def __init__(self, customer_id: str, page: int = 1, size: int = 20):
        self.customer_id = customer_id
        self.page = page
        self.size = size

# 命令处理器 - 写模型
class OrderCommandHandler:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self._orders: Dict[str, Order] = {}  # 简单的内存存储
    
    def handle_create_order(self, command: CreateOrderCommand) -> str:
        """处理创建订单命令"""
        order = Order(customer_id=command.customer_id)
        
        for item in command.items:
            price = Money(item['price'])
            order.add_item(item['product_id'], item['product_name'], price, item['quantity'])
        
        order.confirm()
        
        # 保存到写模型
        self._orders[order.order_id] = order
        
        # 发布领域事件
        for event in order.events:
            self.event_bus.publish(event)
        
        order.clear_events()
        return order.order_id
    
    def handle_update_order_status(self, command: UpdateOrderStatusCommand):
        """处理更新订单状态命令"""
        if command.order_id not in self._orders:
            raise ValueError("订单不存在")
        
        order = self._orders[command.order_id]
        # 实际的状态更新逻辑...
        print(f"🔄 更新订单状态: {command.order_id} -> {command.new_status.value}")

# 查询处理器 - 读模型
class OrderQueryHandler:
    def __init__(self):
        # 读模型优化查询，可能使用不同的数据库或缓存
        self._order_projections: Dict[str, Dict] = {}
    
    def handle_get_order(self, query: GetOrderQuery) -> Dict[str, Any]:
        """处理获取订单查询"""
        if query.order_id in self._order_projections:
            return self._order_projections[query.order_id]
        return {}
    
    def handle_get_customer_orders(self, query: GetCustomerOrdersQuery) -> List[Dict]:
        """处理获取客户订单查询"""
        # 模拟从读模型查询
        customer_orders = [
            order for order in self._order_projections.values() 
            if order.get('customer_id') == query.customer_id
        ]
        
        # 分页逻辑
        start = (query.page - 1) * query.size
        end = start + query.size
        return customer_orders[start:end]
    
    def update_read_model(self, event: OrderConfirmedEvent):
        """根据领域事件更新读模型"""
        projection = {
            'order_id': event.order_id,
            'customer_id': event.customer_id,
            'total_amount': event.total_amount.amount,
            'confirmed_at': event.confirmed_at.isoformat(),
            'status': 'confirmed'
        }
        
        self._order_projections[event.order_id] = projection
        print(f"📊 更新读模型: {event.order_id}")

# 测试CQRS架构
def test_cqrs_architecture():
    print("=== CQRS架构测试 ===")
    
    # 创建事件总线
    event_bus = EventBus()
    
    # 创建命令和查询处理器
    command_handler = OrderCommandHandler(event_bus)
    query_handler = OrderQueryHandler()
    
    # 订阅读模型更新事件
    event_bus.subscribe(OrderConfirmedEvent, query_handler.update_read_model)
    
    # 执行命令
    create_command = CreateOrderCommand(
        customer_id="customer_123",
        items=[
            {"product_id": "prod_1", "product_name": "Python书", "price": 99.9, "quantity": 2},
            {"product_id": "prod_2", "product_name": "架构书", "price": 129.9, "quantity": 1}
        ]
    )
    
    order_id = command_handler.handle_create_order(create_command)
    print(f"✅ 创建的订单ID: {order_id}")
    
    # 执行查询
    get_query = GetOrderQuery(order_id=order_id)
    order_data = query_handler.handle_get_order(get_query)
    print(f"📋 查询到的订单数据: {order_data}")


if __name__ == "__main__":
    test_cqrs_architecture()