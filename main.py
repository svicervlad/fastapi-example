'''
Main Fast API application
'''
from typing import Union

from fastapi import FastAPI

from loguru import logger

logger.info("App lication stareted")


app = FastAPI()


@logger.catch
@app.get("/")
def read_root():
    '''
    Home page
    '''
    return {"Hello": "World"}

@logger.catch
@app.get("/items/{item_id}")
def read_item(item_id: int, query: Union[str, None] = None):
    '''
    Get some item
    '''
    return {"item_id": item_id, "q": query}
