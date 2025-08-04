from fastapi import APIRouter, HTTPException
from typing import List
from ..models.room import Room
from ..database import db
from ..utils.room_utils import rooms_util

router = APIRouter()

@router.get("/rooms", response_model=List[dict])
async def get_all_rooms():
    rooms_cursor = db["rooms"].find()
    rooms_list = []
    async for room in rooms_cursor:
        rooms_list.append(rooms_util(room))
    return rooms_list

@router.get("/rooms/{room_id}", response_model=Room)
async def get_room(room_id: str):
    room = await db["rooms"].find_one({"roomId": room_id})
    if room:
        return rooms_util(room)
    raise HTTPException(status_code=404, detail="Room not found")