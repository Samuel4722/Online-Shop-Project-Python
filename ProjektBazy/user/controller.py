from fastapi import APIRouter, Depends
from passlib.context import CryptContext
from .model import User, Customer, Product, Order, OrderItem
from .schemas import (
    UserCreate, UserRead, CustomerCreate, CustomerRead,
    ProductCreate, ProductRead, OrderCreate, OrderRead,
    OrderItemCreate, OrderItemRead
)
from .auth import get_current_user, admin_required
from .service import calculate_customer_total, customer_order_stats, iterate_customer_orders

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
MAX_BCRYPT_LEN = 72

# Users
@router.post("/users", response_model=UserRead)
async def create_user(user: UserCreate):
    hashed_password = pwd_context.hash(user.password[:MAX_BCRYPT_LEN])
    return await User.create(login=user.login, password=hashed_password)

@router.get("/users", response_model=list[UserRead], dependencies=[Depends(admin_required)])
async def list_users():
    return await User.all()

# Customers
@router.post("/customers", response_model=CustomerRead)
async def create_customer(customer: CustomerCreate, user=Depends(get_current_user)):
    return await Customer.create(**customer.dict())

@router.get("/customers", response_model=list[CustomerRead])
async def list_customers(user=Depends(get_current_user)):
    return await Customer.all()

@router.get("/customers/{customer_id}/orders")
async def customer_orders(customer_id: int, user=Depends(get_current_user)):
    results = []
    async for row in iterate_customer_orders(customer_id):
        results.append(row)
    return results

@router.get("/customers/{customer_id}/stats")
async def customer_stats(customer_id: int, user=Depends(get_current_user)):
    return await customer_order_stats(customer_id)

@router.get("/customers/{customer_id}/total")
async def customer_total(customer_id: int, user=Depends(get_current_user)):
    total = await calculate_customer_total(customer_id)
    return {"customer_id": customer_id, "total": total}

# Products
@router.post("/products", response_model=ProductRead, dependencies=[Depends(admin_required)])
async def create_product(product: ProductCreate):
    return await Product.create(**product.dict())

@router.get("/products", response_model=list[ProductRead])
async def list_products():
    return await Product.all()

# Orders
@router.post("/orders", response_model=OrderRead)
async def create_order(order: OrderCreate, user=Depends(get_current_user)):
    return await Order.create(customer_id=order.customer_id)

@router.get("/orders", response_model=list[OrderRead])
async def list_orders(user=Depends(get_current_user)):
    return await Order.all()

@router.get("/orders/me", response_model=list[OrderRead])
async def my_orders(user=Depends(get_current_user)):
    return await Order.filter(customer_id=user.id).all()

# Order Items
@router.post("/order_items", response_model=OrderItemRead)
async def create_order_item(item: OrderItemCreate, user=Depends(get_current_user)):
    return await OrderItem.create(**item.dict())

@router.get("/order_items", response_model=list[OrderItemRead])
async def list_order_items(user=Depends(get_current_user)):
    return await OrderItem.all()
