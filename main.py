'''
Main Fast API application
'''
from fastapi import FastAPI

from loguru import logger
from api.item_model import Item

logger.add("file.log", rotation="5 MB")

logger.debug("Application stareted")

app = FastAPI()


@logger.catch
@app.get("/")
def read_root():
    '''
    Home page
    '''
    return {"Hello": "World"}


@logger.catch
@app.post("/items/", response_model=Item)
def calc_full_price(item: Item) -> Item:
    '''
    Calculate price with tax
    '''
    item.full_price = item.price + item.tax
    return item


@logger.catch
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):  # pylint: disable=invalid-name
    '''
    Get some item
    '''
    return {"item_id": item_id, "query": q}
