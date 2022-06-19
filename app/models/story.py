'''
Define Story Object and cruds
'''
from datetime import datetime
from enum import Enum
from fastapi import HTTPException, status
import pandas as pd
from pydantic import BaseModel
from app.db.mongo import db
from app.utils.mongo import get_object_id

STORY_COLLECTION = 'story'
collection = db[STORY_COLLECTION]


class StoryType(str, Enum):
    '''
    Allow story types
    '''
    NEWS = 'news'
    DRAFT = 'draft'


class StoryBase(BaseModel):
    '''
    Base story object
    '''
    title: str
    body: str
    type: StoryType


class StoryDB(StoryBase):
    '''
    Model for story in db
    '''
    id: str
    updated: datetime
    created: datetime


def story_create(story: StoryBase) -> StoryDB:
    '''
    Create story
    '''
    story = story.dict()
    story['updated'] = datetime.utcnow()
    story['created'] = datetime.utcnow()
    story_id = collection.insert_one(story).inserted_id
    if not story_id:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Story can't created")
    story['id'] = str(story_id)
    story = StoryDB(**story)
    return story


def story_update(story: StoryBase, story_id: str) -> StoryDB:
    '''
    Update story by id
    '''
    story = story.dict()
    story['updated'] = datetime.utcnow()
    id_to_update = get_object_id(story_id)
    if not id_to_update:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Id is not valid")
    story_raw = collection.find_one_and_update(
        {"_id": id_to_update},
        {
            "$set": story
        }
    )
    if not story_raw:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Story not found")
    story_raw['id'] = story_id
    del story_raw['_id']
    story_raw = StoryDB(**story_raw)
    return story_raw



def get_stories_from_db(stories_type: StoryType) -> list[StoryDB]:
    '''
    Get all stories from db by type
    '''
    objects = collection.find({'type': stories_type})
    if len(objects) == 0:
        return []
    df = pd.DataFrame(objects)
    df['id'] = pd.Series(df['_id']).apply(lambda x: str(x))
    del df["_id"]
    stories = [StoryDB(**x) for x in df.to_dict('records')]
    return stories


def get_story_by_id(story_id: str) -> StoryDB:
    '''
    Get story by id
    '''
    story_id_object = get_object_id(story_id)
    if not story_id_object:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Id is not valid")
    story_raw = collection.find_one({'_id': story_id_object})
    if not story_raw:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Story not found")
    story_raw['id'] = story_id
    del story_raw['_id']
    story = StoryDB(**story_raw)
    return story
