from fastapi import APIRouter, HTTPException
from typing import List
from ..models.customer import Customer
from ..database import db

router = APIRouter()

@router.get("/", response_model=List[Customer])
async def get_all_customers():
    cursor = db["customers"].find()
    return [Customer(**doc) async for doc in cursor]

@router.get("/{customer_id}", response_model=Customer)
async def get_customer(customer_id: str):
    customer = await db["customers"].find_one({"customerId": customer_id})
    if customer:
        return Customer(**customer)
    raise HTTPException(status_code=404, detail="Customer not found")

@router.post("/", response_model=Customer)
async def create_customer(customer: Customer):
    result = await db["customers"].insert_one(customer.dict())
    if result.inserted_id:
        return customer
    raise HTTPException(status_code=500, detail="Failed to create customer")

@router.put("/{customer_id}", response_model=Customer)
async def update_customer(customer_id: str, customer: Customer):
    result = await db["customers"].replace_one({"customerId": customer_id}, customer.dict())
    if result.modified_count == 1:
        return customer
    raise HTTPException(status_code=404, detail="Customer not found or not modified")

@router.delete("/{customer_id}")
async def delete_customer(customer_id: str):
    result = await db["customers"].delete_one({"customerId": customer_id})
    if result.deleted_count == 1:
        return {"message": "Customer deleted"}
    raise HTTPException(status_code=404, detail="Customer not found")
