from typing import List
from fastapi import  FastAPI
from pydantic import  BaseModel

app = FastAPI()

class Item(BaseModel):
    nane: str
    price: float
    is_offer: bool = None

class User(BaseModel):
    username: str
    full_name: str = None

class Order(BaseModel):
    items: list[Item]
    user: User
    