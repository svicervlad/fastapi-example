'''
Define item model class
'''
from pydantic import BaseModel


class Item(BaseModel):
    '''
    Product Variant
    '''
    name: str
    code: str | int
    description: str | None
    price: float
    tax: float
