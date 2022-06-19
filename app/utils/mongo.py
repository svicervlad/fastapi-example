'''
Utils for mongodb
'''
from bson.objectid import ObjectId
from bson.errors import InvalidId

def get_object_id(id: str) -> ObjectId | None:
    '''
    Try to parse string to bson ObjectID
    '''
    try:
        id = ObjectId(id)
    except (InvalidId, TypeError):
        return None
    return id
