from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from motor.motor_asyncio import AsyncIOMotorClient
import os
from datetime import datetime

# ----------------------------
# Pydantic Models
# ----------------------------
class Customer(BaseModel):
    customerId: str
    name: str
    email: str
    phone: str
    address: str
    membershipId: Optional[str]

class TimeSlot(BaseModel):
    startAt: datetime
    endAt: datetime

class Booking(BaseModel):
    bookingId: str
    customerId: str
    roomId: str
    bookingAt: datetime
    timeSlot: TimeSlot
    status: str

class Membership(BaseModel):
    membershipId: str
    customerId: str
    type: str
    startDate: datetime
    expiryDate: datetime

class OrderItem(BaseModel):
    productId: str
    quantity: int
    unitPrice: float

class Order(BaseModel):
    orderId: str
    customerId: str
    orderDate: datetime
    status: str
    orderItems: List[OrderItem]

class Payment(BaseModel):
    paymentId: str
    customerId: str
    amount: float
    paymentDate: datetime
    method: str
    
class Product(BaseModel):
    productId: str
    name: str
    price: float
    category: str
    description: Optional[str] = None

class Room(BaseModel):
    roomId: str
    name: str
    type: str
    pricePerHour: float
    description: Optional[str] = None
    available: bool = True

# ----------------------------
# FastAPI App
# ----------------------------
app = FastAPI()

# MongoDB Setup
MONGO_DETAILS = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGO_DETAILS)
db = client["KTV-Family"]  # ✅ correct db name

# ----------------------------
# Utility Function
# ----------------------------
def customers_util(customer) -> dict:
    return {
        "customerId": customer["customerId"],
        "name": customer["name"],
        "email": customer["email"],
        "phone": customer["phone"],
        "address": customer["address"],
        "membershipId": customer["membershipId"]
    }

def bookings_util(booking) -> dict:
    return {
        "bookingId": booking["bookingId"],
        "customerId": booking["customerId"],
        "roomId": booking["roomId"],
        "bookingAt": booking["bookingAt"],
        "timeSlot": {
            "startAt": booking["timeSlot"]["startAt"],
            "endAt": booking["timeSlot"]["endAt"]
        },
        "status": booking["status"]
    }

def memberships_util(membership) -> dict:
    return {
        "membershipId": membership["membershipId"],
        "customerId": membership["customerId"],
        "type": membership["type"],
        "startDate": membership["startDate"],
        "expiryDate": membership["expiryDate"]
    }

def orders_util(order) -> dict:
    return {
        "orderId": order["orderId"],
        "customerId": order["customerId"],
        "orderDate": order["orderDate"],
        "status": order["status"],
        "orderItems": [
            {
                "productId": item["productId"],
                "quantity": item["quantity"],
                "unitPrice": item["unitPrice"]
            } for item in order["orderItems"]
        ]
    }

def payments_util(payment) -> dict:
    return {
        "paymentId": payment["paymentId"],
        "customerId": payment["customerId"],
        "amount": payment["amount"],
        "paymentDate": payment["paymentDate"],
        "method": payment["method"]
    }

def products_util(product) -> dict:
    return {
        "productId": product["productId"],
        "name": product["name"],
        "price": product["price"],
        "category": product["category"],
        "description": product.get("description", None)
    }


def rooms_util(room) -> dict:
    return {
        "roomId": room["roomId"],
        "name": room["name"],
        "type": room["type"],
        "pricePerHour": room["pricePerHour"],
        "description": room.get("description", None),
        "available": room.get("available", True)
    }

# ----------------------------
# API Routes
# ----------------------------


# Customer Routes

@app.get("/customers", response_model=List[Customer])
async def get_all_customers():
    customers_cursor = db["customers"].find()
    customers_list = []
    async for customer in customers_cursor:
        customers_list.append(customers_util(customer))
    return customers_list

@app.get("/customers/{customer_id}", response_model=Customer)
async def get_customer(customer_id: str):
    customer = await db["customers"].find_one({"customerId": customer_id})
    if customer:
        return customers_util(customer)
    raise HTTPException(status_code=404, detail="Customer not found")


# Booking Routes

@app.get("/bookings", response_model=List[Booking])
async def get_all_bookings():
    bookings_cursor = db["bookings"].find()
    bookings_list = []
    async for booking in bookings_cursor:
        bookings_list.append(bookings_util(booking))
    return bookings_list

@app.get("/bookings/{booking_id}", response_model=Booking)
async def get_booking(booking_id: str):
    booking = await db["bookings"].find_one({"bookingId": booking_id})
    if booking:
        return bookings_util(booking)
    raise HTTPException(status_code=404, detail="Booking not found")


# Membership Routes

@app.get("/memberships", response_model=List[Membership])
async def get_all_memberships():
    memberships_cursor = db["memberships"].find()
    memberships_list = []
    async for membership in memberships_cursor:
        memberships_list.append(memberships_util(membership))
    return memberships_list

@app.get("/memberships/{membership_id}", response_model=Membership)
async def get_membership(membership_id: str):
    membership = await db["memberships"].find_one({"membershipId": membership_id})
    if membership:
        return memberships_util(membership)
    raise HTTPException(status_code=404, detail="Membership not found")


# Order Routes

@app.get("/orders", response_model=List[dict])
async def get_all_orders():
    orders_cursor = db["orders"].find()
    orders_list = []
    async for order in orders_cursor:
        orders_list.append(orders_util(order))
    return orders_list

@app.get("/orders/{order_id}", response_model=Order)
async def get_order(order_id: str):
    order = await db["orders"].find_one({"orderId": order_id})
    if order:
        return orders_util(order)
    raise HTTPException(status_code=404, detail="Order not found")


# Payment Routes

@app.get("/payments", response_model=List[dict])
async def get_all_payments():
    payments_cursor = db["payments"].find()
    payments_list = []
    async for payment in payments_cursor:
        payments_list.append(payments_util(payment))
    return payments_list

@app.get("/payments/{payment_id}", response_model=Payment)
async def get_payment(payment_id: str):
    payment = await db["payments"].find_one({"paymentId": payment_id})
    if payment:
        return payments_util(payment)
    raise HTTPException(status_code=404, detail="Payment not found")

# Products Routes

@app.get("/products", response_model=List[Product])
async def get_all_products():
    products_cursor = db["products"].find()
    products_list = []
    async for product in products_cursor:
        products_list.append(products_util(product))
    return products_list

@app.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: str):
    product = await db["products"].find_one({"productId": product_id})
    if product:
        return products_util(product)
    raise HTTPException(status_code=404, detail="Product not found")


# Rooms Routes

@app.get("/rooms", response_model=List[dict])
async def get_all_rooms():
    rooms_cursor = db["rooms"].find()
    rooms_list = []
    async for room in rooms_cursor:
        rooms_list.append(rooms_util(room))
    return rooms_list

@app.get("/rooms/{room_id}", response_model=Room)
async def get_room(room_id: str):
    room = await db["rooms"].find_one({"roomId": room_id})
    if room:
        return rooms_util(room)
    raise HTTPException(status_code=404, detail="Room not found")