from pydantic import BaseModel

class OrderCreate(BaseModel):
    product_id: int
    customer_name: str
    customer_address: str
    customer_phone: str
    quantity: int

class OrderResponse(OrderCreate):
    id: int

    class Config:
        from_attributes = True
