from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
from enum import Enum
import uuid

# 值对象 - 没有唯一标识，通过属性值定义相等性
@dataclass(frozen=True)
class Money:
    """货币值对象"""
    amount: float
    currency: str = "CNY"
    
    def __post_init__(self):
        if self.amount < 0:
            raise ValueError("金额不能为负数")
    
    def add(self, other: 'Money') -> 'Money':
        if self.currency != other.currency:
            raise ValueError("货币类型不匹配")
        return Money(self.amount + other.amount, self.currency)
    
    def multiply(self, multiplier: float) -> 'Money':
        return Money(self.amount * multiplier, self.currency)

# 实体 - 有唯一标识
class OrderStatus(Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PAID = "paid"
    SHIPPED = "shipped"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class Order:
    """订单聚合根 - 领域驱动设计中的核心概念"""
    
    def __init__(self, order_id: Optional[str] = None, customer_id: str = ""):
        self.order_id = order_id or str(uuid.uuid4())
        self.customer_id = customer_id
        self.status = OrderStatus.PENDING
        self._order_items: List['OrderItem'] = []
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    
    def add_item(self, product_id: str, product_name: str, price: Money, quantity: int):
        """添加订单项 - 业务逻辑封装在聚合根中"""
        if self.status != OrderStatus.PENDING:
            raise ValueError("只能在待处理状态下修改订单")
        
        if quantity <= 0:
            raise ValueError("数量必须大于0")
        
        # 检查是否已存在相同商品
        for item in self._order_items:
            if item.product_id == product_id:
                item.update_quantity(quantity)
                self.updated_at = datetime.now()
                return
        
        # 添加新订单项
        new_item = OrderItem(product_id, product_name, price, quantity)
        self._order_items.append(new_item)
        self.updated_at = datetime.now()
    
    def remove_item(self, product_id: str):
        """移除订单项"""
        if self.status != OrderStatus.PENDING:
            raise ValueError("只能在待处理状态下修改订单")
        
        self._order_items = [item for item in self._order_items if item.product_id != product_id]
        self.updated_at = datetime.now()
    
    def confirm(self):
        """确认订单 - 重要的业务规则"""
        if self.status != OrderStatus.PENDING:
            raise ValueError("只能确认待处理订单")
        
        if not self._order_items:
            raise ValueError("订单不能为空")
        
        self.status = OrderStatus.CONFIRMED
        self.updated_at = datetime.now()
        
        # 发布领域事件
        self._events.append(OrderConfirmedEvent(
            order_id=self.order_id,
            customer_id=self.customer_id,
            total_amount=self.total_amount,
            confirmed_at=datetime.now()
        ))
    
    @property
    def total_amount(self) -> Money:
        """计算总金额 - 业务逻辑"""
        if not self._order_items:
            return Money(0)
        
        total = Money(0)
        for item in self._order_items:
            total = total.add(item.total_price)
        return total
    
    @property
    def order_items(self) -> List['OrderItem']:
        """返回订单项的不可变副本"""
        return self._order_items.copy()
    
    # 领域事件相关
    _events: List['DomainEvent'] = []
    
    @property
    def events(self) -> List['DomainEvent']:
        """获取待处理的领域事件"""
        return self._events.copy()
    
    def clear_events(self):
        """清空已处理的领域事件"""
        self._events.clear()

class OrderItem:
    """订单项实体"""
    def __init__(self, product_id: str, product_name: str, price: Money, quantity: int):
        self.product_id = product_id
        self.product_name = product_name
        self.price = price
        self.quantity = quantity
    
    def update_quantity(self, new_quantity: int):
        """更新数量"""
        if new_quantity <= 0:
            raise ValueError("数量必须大于0")
        self.quantity = new_quantity
    
    @property
    def total_price(self) -> Money:
        """计算单项总价"""
        return self.price.multiply(self.quantity)

# 领域事件
class DomainEvent:
    pass

@dataclass
class OrderConfirmedEvent(DomainEvent):
    order_id: str
    customer_id: str
    total_amount: Money
    confirmed_at: datetime

# 测试领域驱动设计
def test_domain_driven_design():
    print("=== 领域驱动设计测试 ===")
    
    # 创建订单
    order = Order(customer_id="customer_123")
    
    # 添加订单项
    try:
        order.add_item("prod_1", "Python编程书", Money(99.9), 2)
        order.add_item("prod_2", "架构设计书", Money(129.9), 1)
        
        print(f"📦 订单项数量: {len(order.order_items)}")
        print(f"💰 订单总金额: {order.total_amount.amount} {order.total_amount.currency}")
        
        # 确认订单
        order.confirm()
        print(f"✅ 订单状态: {order.status.value}")
        
        # 检查领域事件
        print(f"🔔 生成的领域事件: {len(order.events)} 个")
        for event in order.events:
            if isinstance(event, OrderConfirmedEvent):
                print(f"   - 订单确认事件: {event.order_id}")
        
        # 清空事件
        order.clear_events()
        
    except ValueError as e:
        print(f"❌ 业务规则验证: {e}")

test_domain_driven_design()