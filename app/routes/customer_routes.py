from fastapi import APIRouter, HTTPException
from typing import List
from ..models.customer import Customer
from ..database import db
from ..utils.customer_utils import customers_util

router = APIRouter()

@router.get("/", response_model=List[Customer])
async def get_all_customers():
    customers_cursor = db["customers"].find()
    customers_list = []
    async for customer in customers_cursor:
        customers_list.append(customers_util(customer))
    return customers_list

@router.get("/{customer_id}", response_model=Customer)
async def get_customer(customer_id: str):
    customer = await db["customers"].find_one({"customerId": customer_id})
    if customer:
        return customers_util(customer)
    raise HTTPException(status_code=404, detail="Customer not found")

@router.post("/", response_model=Customer)
async def create_customer(customer: Customer):
    customer_dict = customer.dict()
    result = await db["customers"].insert_one(customer_dict)
    if result.acknowledged:
        return customers_util(customer_dict)
    raise HTTPException(status_code=500, detail="Failed to create customer")
