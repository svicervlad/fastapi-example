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


class Story(BaseModel):
    '''
    Story object
    '''
    id: str | None = None
    title: str
    body: str
    type: StoryType
    updated: datetime | None
    created: datetime | None

    def create(self):
        '''
        Create story
        '''
        self.updated = datetime.utcnow()
        self.created = datetime.utcnow()
        story = self.dict(exclude={"id"})
        story_id = collection.insert_one(story).inserted_id
        if not story_id:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Story can't created")
        self.id = str(story_id)
        return self

    def update(self):
        '''
        Update story by id
        '''
        self.updated = datetime.utcnow()
        id_to_update = get_object_id(self.id)
        if not id_to_update:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Id is not valid")
        result = collection.update_one(
            {"_id": id_to_update},
            {
                "$set": self.dict(exclude={"id"})
            }
        )
        if result.modified_count < 1:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Story not found")
        return self


class ExistedStory(Story):
    '''
    Model for story in db
    '''
    id: str
    updated: datetime
    created: datetime


def get_stories_from_db(stories_type: StoryType) -> list[Story]:
    '''
    Get all stories from db by type
    '''
    objects = collection.find({'type': stories_type})
    df = pd.DataFrame(objects)
    if len(df) == 0:
        return []
    df['id'] = pd.Series(df['_id']).apply(lambda x: str(x))
    del df["_id"]
    stories = [Story(**x) for x in df.to_dict('records')]
    return stories


def get_story_by_id(story_id: str) -> ExistedStory:
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
    story = ExistedStory(**story_raw)
    return story
