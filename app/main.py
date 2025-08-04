from fastapi import FastAPI
from .routes import (
    customer_routes,
    booking_routes,
    membership_routes,
    order_routes,
    payment_routes,
    product_routes,
    room_routes
)

app = FastAPI()

app.include_router(customer_routes.router, prefix="/customers", tags=["Customers"])
app.include_router(booking_routes.router, prefix="/bookings", tags=["Bookings"])
app.include_router(membership_routes.router, prefix="/memberships", tags=["Memberships"])
app.include_router(order_routes.router, prefix="/orders", tags=["Orders"])
app.include_router(payment_routes.router, prefix="/payments", tags=["Payments"])
app.include_router(product_routes.router, prefix="/products", tags=["Products"])
app.include_router(room_routes.router, prefix="/rooms", tags=["Rooms"])
