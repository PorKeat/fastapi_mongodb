def products_util(product) -> dict:
    return {
        "productId": product["productId"],
        "name": product["name"],
        "price": product["price"],
        "category": product["category"],
        "description": product.get("description", None)
    }