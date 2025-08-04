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