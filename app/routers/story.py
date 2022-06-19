from fastapi import APIRouter
from app.models.story import Story, StoryType, get_stories_from_db


router = APIRouter(
    prefix="/stories",
    tags=["stories"],
)


@router.post("/", response_model=Story)
def create_story(story: Story):
    '''
    Create new story
    '''
    story = story.create()
    return story

@router.get('/{stories_type}', response_model=list[Story])
def get_stories(stories_type: StoryType):
    '''
    Get stories by stories type
    '''
    result = get_stories_from_db(stories_type)
    return result
