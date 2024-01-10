from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models, schemas, oauth2
from ..database import get_db


#   creating the router for the posts
router = APIRouter(
    prefix="/posts",
    tags = ['Posts']
)


@router.get("/", response_model=List[schemas.Post])
async def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
                    Limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    """
    gets posts from the API
    :param db:
    :param current_user:
    :param Limit:
    :param skip:
    :param search:
    :return:
    """

    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(Limit).offset(skip).all()

    results = db.query(models.Post).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).go
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def createposts(post:schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    """
    creates a post for the user that's logged in
    :param post:
    :param db:
    :param current_user:
    :return:
    """
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    # cursor.execute("""INSERT INTO POSTS (title, content, published) values(%s, %s, %s) returning * """,
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()

    # post_dict = post.model_dump()
    # post_dict["id"] =  randrange(0, 100000)
    # my_posts.append(post_dict)
    #HTTPException(status_code=status.HTTP_201_CREATED, detail=f"post with id: {id} was created")
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}", response_model=schemas.Post)
async def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    """
    gets a post based on it's id
    :param id:
    :param db:
    :param current_user:
    :return:
    """
    post = db.query(models.Post).filter(models.Post.id==id).first()
    # cursor.execute("""select * from posts where id=%s """, (str(id)))
    # post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f"post with id: {id} was not found"}
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    """
    deletes the post with the id provided, and it's limited to only the user's posts
    :param id:
    :param db:
    :param current_user:
    :return:
    """
    # cursor.execute("""DELETE FROM POSTS WHERE ID=%s returning *""",(str(id)))
    # deleted_post = cursor.fetchone()
    # connection.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} doesn't exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
@router.put("/{id}", response_model=schemas.Post)
async def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    """
    puts a
    :param id:
    :param updated_post:
    :param db:
    :param current_user:
    :return:
    """
    # cursor.execute("""update posts set title = %s, content=%s, published=%s where id = %s returning *""",
    #                (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # connection.commit()
    post_query = db.query(models.Post).filter(models.Post.id==id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} doesn't exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    post_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()

    return post_query.first()