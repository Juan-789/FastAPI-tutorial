from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import  randrange


app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts = [{"title": "title of post1", "content": "content of post 1", "id":1}]

def find_posts(id):
    for p in my_posts:
        if p["id"]==id:
            return p

def find_index(id):
    for i, p  in enumerate(my_posts):
        if p['id'] == id:
            return i

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts")
async def posts():
    return {"posts": my_posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def createposts(post: Post):
    post_dict = post.model_dump()
    post_dict["id"] =  randrange(0, 100000)
    my_posts.append(post_dict)
    #HTTPException(status_code=status.HTTP_201_CREATED, detail=f"post with id: {id} was created")
    return {"data":  post_dict}

@app.get("/posts/{id}")
async def get_post(id: int):
    post = find_posts(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f"post with id: {id} was not found"}
    return {"post_detail": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    """deleting post"""
    index = find_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} doesn't exist")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
async def update_post(id: int, post: Post):
    print(post)
    index = find_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} doesn't exist")

    post_dict = post.model_dump()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"data": post_dict}
#     post
# @app.delete("/posts/{id}")

#    return {"new_post":  f"title {payload['title']} content: {payload['content']}"}
# title str, content str

