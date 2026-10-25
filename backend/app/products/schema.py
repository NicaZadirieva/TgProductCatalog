from pydantic import BaseModel


class CreateProductRequest(BaseModel):
    name: str
    photo_path: str


class CreateProductResponse(BaseModel):
    product_id: int
