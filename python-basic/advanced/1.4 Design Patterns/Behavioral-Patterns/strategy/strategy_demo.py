from abc import ABC, abstractmethod
from typing import List
from dataclasses import dataclass

@dataclass
class Order:
    """订单数据类"""
    items: List[str]
    total_amount: float
    customer_type: str  # "regular", "vip", "premium"

class PricingStrategy(ABC):
    """定价策略抽象类"""
    @abstractmethod
    def calculate_price(self, order: Order) -> float:
        pass

class RegularPricingStrategy(PricingStrategy):
    """普通客户定价策略"""
    def calculate_price(self, order: Order) -> float:
        return order.total_amount  # 无折扣

class VIPPricingStrategy(PricingStrategy):
    """VIP客户定价策略"""
    def calculate_price(self, order: Order) -> float:
        return order.total_amount * 0.9  # 9折

class PremiumPricingStrategy(PricingStrategy):
    """高级客户定价策略"""
    def calculate_price(self, order: Order) -> float:
        return order.total_amount * 0.8  # 8折

class DiscountPricingStrategy(PricingStrategy):
    """促销折扣策略"""
    def __init__(self, discount_rate: float = 0.7):
        self.discount_rate = discount_rate
    
    def calculate_price(self, order: Order) -> float:
        return order.total_amount * self.discount_rate

class OrderProcessor:
    """订单处理器 - 使用策略模式"""
    def __init__(self):
        self._strategies = {
            "regular": RegularPricingStrategy(),
            "vip": VIPPricingStrategy(),
            "premium": PremiumPricingStrategy()
        }
        self._current_strategy = self._strategies["regular"]
    
    def set_strategy(self, customer_type: str):
        """设置定价策略"""
        if customer_type in self._strategies:
            self._current_strategy = self._strategies[customer_type]
        else:
            self._current_strategy = self._strategies["regular"]
    
    def set_custom_strategy(self, strategy: PricingStrategy):
        """设置自定义策略"""
        self._current_strategy = strategy
    
    def process_order(self, order: Order) -> float:
        """处理订单并返回最终价格"""
        final_price = self._current_strategy.calculate_price(order)
        print(f"💰 原始价格: {order.total_amount}, 最终价格: {final_price}")
        return final_price

# Pythonic的策略模式：使用函数字典
def create_pythonic_pricing():
    """Pythonic的策略模式实现"""
    
    def regular_pricing(order):
        return order.total_amount
    
    def vip_pricing(order):
        return order.total_amount * 0.9
    
    def premium_pricing(order):
        return order.total_amount * 0.8
    
    strategies = {
        "regular": regular_pricing,
        "vip": vip_pricing,
        "premium": premium_pricing
    }
    
    def process_order(order, strategy_key="regular"):
        strategy = strategies.get(strategy_key, regular_pricing)
        return strategy(order)
    
    return process_order

# 测试策略模式
def test_strategy_pattern():
    print("=== 策略模式测试 ===")
    
    # 传统策略模式
    processor = OrderProcessor()
    order = Order(items=["商品A", "商品B"], total_amount=1000.0, customer_type="vip")
    
    # 根据客户类型自动选择策略
    processor.set_strategy(order.customer_type)
    processor.process_order(order)
    
    # 动态切换策略
    processor.set_custom_strategy(DiscountPricingStrategy(0.5))  # 5折促销
    processor.process_order(order)
    
    print("\n--- Pythonic版本 ---")
    
    # Pythonic策略模式
    pythonic_processor = create_pythonic_pricing()
    final_price = pythonic_processor(order, "premium")
    print(f"🐍 Pythonic最终价格: {final_price}")

test_strategy_pattern()