'''
Main Fast API application
'''
from fastapi import FastAPI

from loguru import logger
from .utils.logger import configure_logger
from .routers import story

app = FastAPI()

app.include_router(story.router)

@app.on_event("startup")
async def startup_event():
    '''
    Hook run after startup app
    '''
    configure_logger()
    logger.debug("app is stareted")


@app.on_event("shutdown")
def shutdown_event():
    '''
    Hook run after app stoped
    '''
    logger.debug("app is stoped")


@logger.catch
@app.get("/")
def read_root():
    '''
    Home page
    '''
    return {"Hello": "World"}
