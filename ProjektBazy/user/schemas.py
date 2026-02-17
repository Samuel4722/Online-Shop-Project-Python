from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal

class UserCreate(BaseModel):
    login: str
    password: str

class UserRead(BaseModel):
    id: int
    login: str
    role: str

    class Config:
        from_attributes = True


class CustomerCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str | None = None

class CustomerRead(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    phone: str | None
    registered_at: datetime

    class Config:
        from_attributes = True


class ProductCreate(BaseModel):
    name: str
    description: str | None = None
    price: Decimal
    stock: int = 0

class ProductRead(BaseModel):
    id: int
    name: str
    description: str | None
    price: Decimal
    stock: int

    class Config:
        from_attributes = True


class OrderCreate(BaseModel):
    customer_id: int

class OrderRead(BaseModel):
    id: int
    customer_id: int
    date: datetime
    status: str

    class Config:
        from_attributes = True


class OrderItemCreate(BaseModel):
    order_id: int
    product_id: int
    quantity: int
    unit_price: Decimal

class OrderItemRead(BaseModel):
    id: int
    order_id: int
    product_id: int
    quantity: int
    unit_price: Decimal

    class Config:
        from_attributes = True
