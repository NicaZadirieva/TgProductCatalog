from pydantic import BaseModel


class CreateProductResponse(BaseModel):
    product_id: int
