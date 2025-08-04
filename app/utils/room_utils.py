def rooms_util(room) -> dict:
    return {
        "roomId": room["roomId"],
        "name": room["name"],
        "type": room["type"],
        "pricePerHour": room["pricePerHour"],
        "description": room.get("description", None),
        "available": room.get("available", True)
    }