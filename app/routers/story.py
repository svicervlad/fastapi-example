'''
Stories routers
'''
from fastapi import APIRouter, status
from app.models.story import Story, ExistedStory, StoryType, get_stories_from_db, get_story_by_id


router = APIRouter(
    prefix="/stories",
    tags=["stories"],
)


@router.get('/{stories_type}', response_model=list[Story])
def get_stories(stories_type: StoryType):
    '''
    Get stories by stories type
    '''
    return get_stories_from_db(stories_type)


@router.get('/story/{story_id}', response_model=ExistedStory)
def get_story(story_id: str):
    '''
    Get story by id
    '''
    return get_story_by_id(story_id)


@router.put("/", response_model=Story, status_code=status.HTTP_201_CREATED)
def create_story(story: Story):
    '''
    "id" and "updated" params no need to request - auto generating

    '''
    story.create()
    return story


@router.patch("/", response_model=ExistedStory, status_code=status.HTTP_200_OK)
def update_story(story: ExistedStory):
    '''
    "updated" param no need to request - auto generating

    '''
    story = story.update()
    return story
