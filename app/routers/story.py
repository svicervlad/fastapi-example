'''
Stories routers
'''
from fastapi import APIRouter, status
from app.models.story import (
        StoryBase,StoryDB, StoryType,
        get_stories_from_db, get_story_by_id, story_create, story_update
    )


router = APIRouter(
    prefix="/stories",
    tags=["Stories"],
)


@router.get('/{stories_type}', response_model=list[StoryDB])
def get_stories(stories_type: StoryType):
    '''
    Get stories by story type
    '''
    return get_stories_from_db(stories_type)


@router.get('/story/{story_id}', response_model=StoryDB)
def get_story(story_id: str):
    '''
    Get story by id
    '''
    return get_story_by_id(story_id)


@router.put("/story/", response_model=StoryDB, status_code=status.HTTP_201_CREATED)
def create_story(story: StoryBase):
    return story_create(story)


@router.patch("/story/{story_id}", response_model=StoryDB, status_code=status.HTTP_200_OK)
def update_story(story: StoryBase, story_id: str):
    return story_update(story, story_id)
