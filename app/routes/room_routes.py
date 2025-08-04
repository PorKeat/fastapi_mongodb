from fastapi import APIRouter, HTTPException
from typing import List
from ..models.room import Room
from ..database import db

router = APIRouter()

@router.get("/", response_model=List[Room])
async def get_all_rooms():
    cursor = db["rooms"].find()
    return [Room(**doc) async for doc in cursor]

@router.get("/{room_id}", response_model=Room)
async def get_room(room_id: str):
    room = await db["rooms"].find_one({"roomId": room_id})
    if room:
        return Room(**room)
    raise HTTPException(status_code=404, detail="Room not found")

@router.post("/", response_model=Room)
async def create_room(room: Room):
    result = await db["rooms"].insert_one(room.dict())
    if result.inserted_id:
        return room
    raise HTTPException(status_code=500, detail="Failed to create room")

@router.put("/{room_id}", response_model=Room)
async def update_room(room_id: str, room: Room):
    result = await db["rooms"].replace_one({"roomId": room_id}, room.dict())
    if result.modified_count == 1:
        return room
    raise HTTPException(status_code=404, detail="Room not found or not modified")

@router.delete("/{room_id}")
async def delete_room(room_id: str):
    result = await db["rooms"].delete_one({"roomId": room_id})
    if result.deleted_count == 1:
        return {"message": "Room deleted"}
    raise HTTPException(status_code=404, detail="Room not found")
