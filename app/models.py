from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, Text, DateTime
from .database import Base


class MenuItem(Base):
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    category = Column(String, index=True)
    price = Column(Float)
    description = Column(Text, nullable=True)
    is_available = Column(Boolean, default=True)


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_phone = Column(String, index=True)
    customer_name = Column(String, nullable=True)
    order_type = Column(String, default="دليفري")  # دليفري / استلام من الفرع
    delivery_address = Column(Text, nullable=True)
    items_summary = Column(Text, nullable=False)
    total_price = Column(Float, default=0.0)
    status = Column(String, default="Confirmed")  # Confirmed, In_Preparation, Out_For_Delivery, Delivered, Cancelled
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class CustomerSession(Base):
    __tablename__ = "customer_sessions"

    customer_phone = Column(String, primary_key=True, index=True)
    state = Column(String, default="idle")  # idle, ordering, awaiting_address, awaiting_confirmation
    current_cart = Column(Text, default="[]")  # JSON representation of current items
    order_type = Column(String, default="دليفري")
    delivery_address = Column(Text, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
