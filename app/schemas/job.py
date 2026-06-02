from pydantic import BaseModel

class JobCreate(BaseModel):
    title: str
    company: str
    location: str
    description: str