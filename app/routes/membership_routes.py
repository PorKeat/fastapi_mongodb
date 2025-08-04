from fastapi import APIRouter, HTTPException
from typing import List
from ..models.membership import Membership
from ..database import db
from ..utils.membership_utils import memberships_util

router = APIRouter()

@router.get("/memberships", response_model=List[Membership])
async def get_all_memberships():
    memberships_cursor = db["memberships"].find()
    memberships_list = []
    async for membership in memberships_cursor:
        memberships_list.append(memberships_util(membership))
    return memberships_list

@router.get("/memberships/{membership_id}", response_model=Membership)
async def get_membership(membership_id: str):
    membership = await db["memberships"].find_one({"membershipId": membership_id})
    if membership:
        return memberships_util(membership)
    raise HTTPException(status_code=404, detail="Membership not found")
