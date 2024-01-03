from pydantic import BaseModel

class PostBase(BaseModel):  # pydantic model
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass


class Post(BaseModel):
    id: int
    title: str
    content: str
    published: bool

    class Config:
        orm_mode = True