def payments_util(payment) -> dict:
    return {
        "paymentId": payment["paymentId"],
        "customerId": payment["customerId"],
        "amount": payment["amount"],
        "paymentDate": payment["paymentDate"],
        "method": payment["method"]
    }