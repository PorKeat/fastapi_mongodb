from fastapi import APIRouter, HTTPException
from typing import List
from ..models.product import Product
from ..database import db
from ..utils.product_utils import products_util

router = APIRouter()

@router.get("/products", response_model=List[Product])
async def get_all_products():
    products_cursor = db["products"].find()
    products_list = []
    async for product in products_cursor:
        products_list.append(products_util(product))
    return products_list

@router.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: str):
    product = await db["products"].find_one({"productId": product_id})
    if product:
        return products_util(product)
    raise HTTPException(status_code=404, detail="Product not found")