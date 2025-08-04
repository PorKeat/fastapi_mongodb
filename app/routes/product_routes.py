from fastapi import APIRouter, HTTPException
from typing import List
from ..models.product import Product
from ..database import db

router = APIRouter()

@router.get("/", response_model=List[Product])
async def get_all_products():
    cursor = db["products"].find()
    return [Product(**doc) async for doc in cursor]

@router.get("/{product_id}", response_model=Product)
async def get_product(product_id: str):
    product = await db["products"].find_one({"productId": product_id})
    if product:
        return Product(**product)
    raise HTTPException(status_code=404, detail="Product not found")

@router.post("/", response_model=Product)
async def create_product(product: Product):
    result = await db["products"].insert_one(product.dict())
    if result.inserted_id:
        return product
    raise HTTPException(status_code=500, detail="Failed to create product")

@router.put("/{product_id}", response_model=Product)
async def update_product(product_id: str, product: Product):
    result = await db["products"].replace_one({"productId": product_id}, product.dict())
    if result.modified_count == 1:
        return product
    raise HTTPException(status_code=404, detail="Product not found or not modified")

@router.delete("/{product_id}")
async def delete_product(product_id: str):
    result = await db["products"].delete_one({"productId": product_id})
    if result.deleted_count == 1:
        return {"message": "Product deleted"}
    raise HTTPException(status_code=404, detail="Product not found")
