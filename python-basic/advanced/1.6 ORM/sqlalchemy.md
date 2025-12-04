# 数据库和ORM高级用法

## SQLAlchemy深度探索

---

### 🔍 **回顾：基础ORM用法**

```python
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import func, and_, or_
from datetime import datetime
import json

# 数据库配置
DATABASE_URL = "sqlite:///advanced_orm.db"  # 生产环境使用PostgreSQL/MySQL

# 创建引擎和会话
engine = create_engine(DATABASE_URL, echo=True)  # echo=True显示SQL语句
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    """用户模型 - 基础示例"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # 关系定义
    orders = relationship("Order", back_populates="user")
    profiles = relationship("UserProfile", back_populates="user", uselist=False)
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"

class UserProfile(Base):
    """用户详情模型 - 一对一关系"""
    __tablename__ = "user_profiles"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    full_name = Column(String(100))
    bio = Column(Text)
    avatar_url = Column(String(255))
    
    # 关系
    user = relationship("User", back_populates="profiles")
    
    def __repr__(self):
        return f"<UserProfile(user_id={self.user_id}, full_name='{self.full_name}')>"

# 创建表
Base.metadata.create_all(bind=engine)

def test_basic_orm():
    """测试基础ORM功能"""
    print("=== 基础ORM功能测试 ===")
    
    with SessionLocal() as session:
        # 创建用户
        new_user = User(
            username="alice_dev",
            email="alice@example.com",
            hashed_password="hashed_password_123"
        )
        
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        
        print(f"✅ 创建用户: {new_user}")
        
        # 查询用户
        user = session.query(User).filter(User.username == "alice_dev").first()
        print(f"🔍 查询结果: {user}")

# test_basic_orm()
```

❓ **思考问题**：基础的CRUD操作很简单，但在复杂业务场景中会遇到哪些挑战？

---

## 🏗️ **高级模型设计模式**

### **1. 混合类：代码复用利器**

```python
from sqlalchemy.ext.declarative import declared_attr

class TimestampMixin:
    """时间戳混合类"""
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

class SoftDeleteMixin:
    """软删除混合类"""
    is_deleted = Column(Integer, default=0, nullable=False)  # 0: 正常, 1: 删除
    
    def soft_delete(self):
        """软删除方法"""
        self.is_deleted = 1
        self.updated_at = datetime.now()

class AuditMixin:
    """审计混合类"""
    created_by = Column(Integer, ForeignKey("users.id"))
    updated_by = Column(Integer, ForeignKey("users.id"))
    
    # 关系
    creator = relationship("User", foreign_keys=[created_by], backref="created_items")
    updater = relationship("User", foreign_keys=[updated_by], backref="updated_items")

class Product(Base, TimestampMixin, SoftDeleteMixin):
    """产品模型 - 使用混合类"""
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, index=True)
    description = Column(Text)
    price = Column(Float, nullable=False)
    stock_quantity = Column(Integer, default=0)
    
    # 分类关系
    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category", back_populates="products")
    
    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', price={self.price})>"

class Category(Base, TimestampMixin):
    """分类模型"""
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text)
    
    # 关系
    products = relationship("Product", back_populates="category")
    
    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}')>"
```

### **2. 多态继承：灵活的继承策略**

```python
class Payment(Base):
    """支付基类 - 多态继承"""
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True)
    amount = Column(Float, nullable=False)
    status = Column(String(20), default="pending")  # pending, completed, failed
    created_at = Column(DateTime, default=datetime.now)
    
    # 多态配置
    type = Column(String(20))
    
    __mapper_args__ = {
        'polymorphic_identity': 'payment',
        'polymorphic_on': type
    }

class CreditCardPayment(Payment):
    """信用卡支付"""
    __tablename__ = "credit_card_payments"
    
    id = Column(Integer, ForeignKey('payments.id'), primary_key=True)
    card_number = Column(String(20))
    card_holder = Column(String(100))
    expiry_date = Column(String(10))
    
    __mapper_args__ = {
        'polymorphic_identity': 'credit_card',
    }

class AlipayPayment(Payment):
    """支付宝支付"""
    __tablename__ = "alipay_payments"
    
    id = Column(Integer, ForeignKey('payments.id'), primary_key=True)
    alipay_account = Column(String(100))
    transaction_id = Column(String(100))
    
    __mapper_args__ = {
        'polymorphic_identity': 'alipay',
    }

def test_polymorphic_inheritance():
    """测试多态继承"""
    print("=== 多态继承测试 ===")
    
    with SessionLocal() as session:
        # 创建不同类型的支付
        credit_payment = CreditCardPayment(
            amount=199.9,
            card_number="**** **** **** 1234",
            card_holder="Alice",
            expiry_date="12/25"
        )
        
        alipay_payment = AlipayPayment(
            amount=299.9,
            alipay_account="alice@alipay.com",
            transaction_id="2023123456789"
        )
        
        session.add_all([credit_payment, alipay_payment])
        session.commit()
        
        # 查询所有支付
        payments = session.query(Payment).all()
        print(f"💰 所有支付方式: {len(payments)} 个")
        
        for payment in payments:
            print(f"  - {payment.type}: 金额 {payment.amount}")

# test_polymorphic_inheritance()
```

---

## 🚀 **高级查询技巧**

### **1. 复杂连接查询**

```python
def advanced_join_queries():
    """高级连接查询示例"""
    print("=== 高级连接查询 ===")
    
    with SessionLocal() as session:
        # 1. 多表连接查询
        query = (session.query(User.username, Product.name, Product.price)
                .join(User.orders)
                .join(Order.order_items)
                .join(OrderItem.product))
        
        print("🔗 多表连接查询:")
        for username, product_name, price in query.limit(5):
            print(f"  👤 {username} → 🛍️ {product_name} (¥{price})")
        
        # 2. 子查询
        subquery = (session.query(func.avg(Product.price).label('avg_price'))
                   .subquery())
        
        expensive_products = (session.query(Product.name, Product.price)
                            .filter(Product.price > subquery.c.avg_price)
                            .all())
        
        print(f"\n💰 高价商品（高于平均价）:")
        for product in expensive_products:
            print(f"  💎 {product.name}: ¥{product.price}")
        
        # 3. 窗口函数（高级分析）
        from sqlalchemy import over, func
        
        ranked_products = (session.query(
            Product.name,
            Product.price,
            func.rank().over(
                order_by=Product.price.desc()
            ).label('price_rank')
        ).limit(10))
        
        print(f"\n🏆 价格排名:")
        for product in ranked_products:
            print(f"  #{product.price_rank} {product.name}: ¥{product.price}")

# advanced_join_queries()
```

### **2. 动态查询构建**

```python
class ProductQueryBuilder:
    """产品查询构建器 - 动态查询模式"""
    
    def __init__(self, session):
        self.session = session
        self.query = session.query(Product)
        self.filters = []
    
    def filter_by_name(self, name: str):
        """按名称过滤"""
        if name:
            self.filters.append(Product.name.like(f"%{name}%"))
        return self
    
    def filter_by_price_range(self, min_price: float = None, max_price: float = None):
        """按价格范围过滤"""
        if min_price is not None:
            self.filters.append(Product.price >= min_price)
        if max_price is not None:
            self.filters.append(Product.price <= max_price)
        return self
    
    def filter_by_category(self, category_id: int = None):
        """按分类过滤"""
        if category_id:
            self.filters.append(Product.category_id == category_id)
        return self
    
    def order_by_price(self, descending: bool = False):
        """价格排序"""
        if descending:
            self.query = self.query.order_by(Product.price.desc())
        else:
            self.query = self.query.order_by(Product.price.asc())
        return self
    
    def paginate(self, page: int = 1, per_page: int = 20):
        """分页"""
        self.page = page
        self.per_page = per_page
        return self
    
    def execute(self):
        """执行查询"""
        if self.filters:
            self.query = self.query.filter(and_(*self.filters))
        
        if hasattr(self, 'page') and hasattr(self, 'per_page'):
            offset = (self.page - 1) * self.per_page
            return self.query.offset(offset).limit(self.per_page).all()
        
        return self.query.all()

def test_dynamic_query():
    """测试动态查询构建器"""
    print("=== 动态查询构建器测试 ===")
    
    with SessionLocal() as session:
        builder = ProductQueryBuilder(session)
        
        products = (builder
                   .filter_by_name("Python")
                   .filter_by_price_range(min_price=50, max_price=200)
                   .order_by_price(descending=True)
                   .paginate(page=1, per_page=5)
                   .execute())
        
        print("🔍 动态查询结果:")
        for product in products:
            print(f"  📚 {product.name}: ¥{product.price}")

# test_dynamic_query()
```

---

## 💾 **JSON字段和复杂数据类型**

```python
from sqlalchemy.dialects.postgresql import JSONB  # PostgreSQL专用
import sqlalchemy.types as types

class JSONEncodedDict(types.TypeDecorator):
    """JSON字段类型装饰器 - 跨数据库兼容"""
    
    impl = types.Text
    
    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)
        return value
    
    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value

class Order(Base):
    """订单模型 - 包含JSON字段"""
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    total_amount = Column(Float, nullable=False)
    status = Column(String(20), default="pending")
    
    # JSON字段存储扩展信息
    shipping_address = Column(JSONEncodedDict)  # 收货地址
    payment_info = Column(JSONEncodedDict)      # 支付信息
    metadata = Column(JSONEncodedDict)          # 元数据
    
    # 时间戳
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # 关系
    user = relationship("User", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order")
    
    def set_shipping_address(self, address_dict: dict):
        """设置收货地址"""
        required_fields = ['recipient', 'phone', 'province', 'city', 'address']
        if not all(field in address_dict for field in required_fields):
            raise ValueError("收货地址信息不完整")
        
        self.shipping_address = address_dict
    
    def get_shipping_address_str(self) -> str:
        """获取格式化地址字符串"""
        if not self.shipping_address:
            return ""
        
        addr = self.shipping_address
        return f"{addr.get('recipient', '')} {addr.get('phone', '')} {addr.get('province', '')}{addr.get('city', '')}{addr.get('address', '')}"

class OrderItem(Base):
    """订单项"""
    __tablename__ = "order_items"
    
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    
    # JSON字段存储商品快照（防止商品信息变更影响订单）
    product_snapshot = Column(JSONEncodedDict)
    
    # 关系
    order = relationship("Order", back_populates="order_items")
    product = relationship("Product")
    
    @property
    def total_price(self) -> float:
        return self.quantity * self.unit_price
    
    def create_product_snapshot(self, product: Product):
        """创建商品快照"""
        self.product_snapshot = {
            'name': product.name,
            'description': product.description,
            'original_price': product.price,
            'snapshot_time': datetime.now().isoformat()
        }

def test_json_fields():
    """测试JSON字段功能"""
    print("=== JSON字段测试 ===")
    
    with SessionLocal() as session:
        # 创建包含JSON字段的订单
        order = Order(
            user_id=1,
            total_amount=199.9,
            status="completed"
        )
        
        # 设置JSON字段
        order.set_shipping_address({
            'recipient': '张三',
            'phone': '13800138000',
            'province': '广东省',
            'city': '深圳市',
            'address': '南山区科技园123号'
        })
        
        order.payment_info = {
            'method': 'alipay',
            'transaction_id': '2023123456789',
            'paid_at': datetime.now().isoformat()
        }
        
        session.add(order)
        session.commit()
        
        print(f"📦 订单收货地址: {order.get_shipping_address_str()}")
        print(f"💳 支付方式: {order.payment_info.get('method', '')}")

# test_json_fields()
```

---

## 🎯 **最佳实践总结**

### **SQLAlchemy高级特性矩阵**

| 特性 | 适用场景 | 优势 | 注意事项 |
|------|---------|------|----------|
| **混合类** | 多模型共享字段/方法 | 代码复用，维护方便 | 避免过度复杂 |
| **多态继承** | 多种相似但不同的实体 | 灵活的数据模型 | 查询性能考虑 |
| **JSON字段** | 动态数据结构 | 模式灵活性 | 查询复杂度增加 |
| **动态查询** | 复杂筛选条件 | 构建灵活API | SQL注入防护 |

### **性能优化建议**
1. **延迟加载** vs **立即加载**：合理使用`lazy`参数
2. **索引优化**：为查询字段添加合适索引
3. **批量操作**：使用`bulk_insert_mappings`等批量方法
4. **连接池**：配置合适的连接池参数
