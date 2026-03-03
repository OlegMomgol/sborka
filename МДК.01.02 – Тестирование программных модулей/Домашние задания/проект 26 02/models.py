from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    id: Optional[int]
    name: str
    email: str
    status: str  


@dataclass
class Order:
    id: Optional[int]
    user_id: int
    product_name: str
    quantity: int