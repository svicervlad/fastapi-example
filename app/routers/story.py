from fastapi import APIRouter
from app.models.story import Story


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
