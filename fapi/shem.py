from pydantic import BaseModel
from typing import List
class CategoryBase(BaseModel):
    name: str

class ProductBase(BaseModel):
    name: str
    price: int
    category: List[str]
    image: str
    info : str
