
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