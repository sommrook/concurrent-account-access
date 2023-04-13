from pydantic import BaseModel

class BasicResponse(BaseModel):
    response_code: str
    response_message: str