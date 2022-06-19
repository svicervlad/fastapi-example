'''
Define Story Object and cruds
'''

from datetime import datetime
from pydantic import BaseModel
from app.db.mongo import client

DB_NAME = 'story'


class Story(BaseModel):
    '''
    Story object
    '''
    id: str | None = None
    title: str
    body: str
    type: str
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
