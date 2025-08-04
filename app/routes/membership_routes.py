from fastapi import APIRouter, HTTPException
from typing import List
from ..models.membership import Membership
from ..database import db

router = APIRouter()

@router.get("/", response_model=List[Membership])
async def get_all_memberships():
    cursor = db["memberships"].find()
    return [Membership(**doc) async for doc in cursor]

@router.get("/{membership_id}", response_model=Membership)
async def get_membership(membership_id: str):
    membership = await db["memberships"].find_one({"membershipId": membership_id})
    if membership:
        return Membership(**membership)
    raise HTTPException(status_code=404, detail="Membership not found")

@router.post("/", response_model=Membership)
async def create_membership(membership: Membership):
    result = await db["memberships"].insert_one(membership.dict())
    if result.inserted_id:
        return membership
    raise HTTPException(status_code=500, detail="Failed to create membership")

@router.put("/{membership_id}", response_model=Membership)
async def update_membership(membership_id: str, membership: Membership):
    result = await db["memberships"].replace_one({"membershipId": membership_id}, membership.dict())
    if result.modified_count == 1:
        return membership
    raise HTTPException(status_code=404, detail="Membership not found or not modified")

@router.delete("/{membership_id}")
async def delete_membership(membership_id: str):
    result = await db["memberships"].delete_one({"membershipId": membership_id})
    if result.deleted_count == 1:
        return {"message": "Membership deleted"}
    raise HTTPException(status_code=404, detail="Membership not found")
