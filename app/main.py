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
from fastapi.responses import HTMLResponse

app = FastAPI()

app.include_router(customer_routes.router, prefix="/customers", tags=["Customers"])
app.include_router(booking_routes.router, prefix="/bookings", tags=["Bookings"])
app.include_router(membership_routes.router, prefix="/memberships", tags=["Memberships"])
app.include_router(order_routes.router, prefix="/orders", tags=["Orders"])
app.include_router(payment_routes.router, prefix="/payments", tags=["Payments"])
app.include_router(product_routes.router, prefix="/products", tags=["Products"])
app.include_router(room_routes.router, prefix="/rooms", tags=["Rooms"])


@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <html>
        <head>
            <title>KTV Booking API</title>
        </head>
        <body style='font-family:sans-serif;text-align:center;margin-top:50px'>
            <h1>🎤 Welcome to KTV Booking API</h1>
            <p>Use the endpoints to manage customers, bookings, orders, and more.</p>
            <p>Visit <a href="/docs">/docs</a> for interactive API documentation.</p>
        </body>
    </html>
    """
