'''
Define Story Object and cruds
'''
from datetime import datetime
from enum import Enum
import pandas as pd
from pydantic import BaseModel
from app.db.mongo import client

DB_NAME = 'story'

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

    def __collection(self):
        return client[DB_NAME][self.type]

    def create(self):
        '''
        Create story
        '''
        self.updated = datetime.utcnow()
        story = self.dict(exclude={"id"})
        story_id = self.__collection().insert_one(story).inserted_id
        self.id = str(story_id)
        return self

    def update(self):
        '''
        Update story by id
        '''
        self.updated = datetime.utcnow()
        self.__collection().update_one(
            {"_id": self.id},
            {
                "$set": self.dict(exclude={"id"})
            }
        )
        return self


def get_stories_from_db(stories_type: StoryType) -> list[Story]:
    '''
    Get all stories from db by type
    '''
    collection = client[DB_NAME][stories_type]
    objects = collection.find()
    df = pd.DataFrame(objects)
    if len(df) == 0:
        return []
    df['id'] = pd.Series(df['_id']).apply(lambda x: str(x))
    del df["_id"]
    stories = [Story(**x) for x in df.to_dict('records')]
    return stories
