def memberships_util(membership) -> dict:
    return {
        "membershipId": membership["membershipId"],
        "customerId": membership["customerId"],
        "type": membership["type"],
        "startDate": membership["startDate"],
        "expiryDate": membership["expiryDate"]
    }