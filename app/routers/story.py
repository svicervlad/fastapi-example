'''
Stories routers
'''
from fastapi import APIRouter, HTTPException
from app.models.story import Story, ExistedStory, StoryType, get_stories_from_db


router = APIRouter(
    prefix="/stories",
    tags=["stories"],
)


@router.post("/", response_model=Story)
def create_story(story: Story):
    '''
    ## Create new story

    "id" and "updated" params no need to request - auto generating

    '''
    story.create()
    return story


@router.patch("/", response_model=ExistedStory)
def update_story(story: ExistedStory):
    '''
    ## Create new story

    "updated" param no need to request - auto generating

    '''
    story = story.update()
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    return story

@router.get('/{stories_type}', response_model=list[Story])
def get_stories(stories_type: StoryType):
    '''
    Get stories by stories type
    '''
    result = get_stories_from_db(stories_type)
    return result
