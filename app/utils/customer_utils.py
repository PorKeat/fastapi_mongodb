
def customers_util(customer) -> dict:
    return {
        "customerId": customer["customerId"],
        "name": customer["name"],
        "email": customer["email"],
        "phone": customer["phone"],
        "address": customer["address"],
        "membershipId": customer["membershipId"]
    }