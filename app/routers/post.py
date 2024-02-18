from fastapi import FastAPI,Response,status,HTTPException, Depends, APIRouter
from .. import models,schemas
from sqlalchemy.orm import Session
from ..database import get_db
from typing import Optional,List
from .. import models, schemas, oauth2


router = APIRouter(
    prefix="/post",
    tags=["Posts"]
)

@router.get("/get_post",response_model=List[schemas.Post])
def get_post(db:Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts""")
    # post= cursor.fetchall()
    post=db.query(models.Post).all()
    # print(post)
    return post


@router.get("/get_post/{id}",response_model=schemas.Post)
def get_post(id:int,db:Session = Depends(get_db)):       #response:Response
    # cursor.execute("""SELECT * FROM posts WHERE id= %s""",(str(id),))
    # post= cursor.fetchone()
    post=db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} was not found")
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {"message":f"post with id:{id} was not found"}
    # print(post)
    return post





#show details by name
@router.get("/get_post/by_name/{published}")
def get_post(published: Optional[str]=None):
    cursor.execute("""SELECT * FROM posts WHERE published= %s""",(str(published),))
    post= cursor.fetchall()
    # print(post)
    return {"data":post}


# @app.post("/create-post")
# def create_post():
#     # print(new_post.title)
#     return {"data":"new post"}
# @app.post("/create_post")
# def create_post(post:Post):
#     cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s, %s, %s) RETURNING * """,
#                    (post.title, post.content, post.published))
#     new_post=cursor.fetchone()
#     conn.commit()
#     return {"data":new_post}

@router.post('/create_posts',status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post:schemas.PostCreate, db:Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("INSERT INTO posts(title, content,published) VALUES(%s, %s,%s) RETURNING *", (post.title, post.content,post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    # print(current_user.email)
    new_post=models.Post(**post.dict())#title=post.title,content=post.content,published=post.published
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return  new_post



@router.delete("/delete_post/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id= %s RETURNING *""",(str(id),))
    # delete_post= cursor.fetchone()
    # conn.commit()
    # print(post)
    post=db.query(models.Post).filter(models.Post.id==id)
    
    if post.first()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} was not found")
        
    post.delete(synchronize_session=False)
    db.commit()    
    return {"data": "Delete successful", "deleted_post": post}




@router.put("/update_post/{id}",response_model=schemas.Post)
def update_post(id:int,updatet_post:schemas.PostCreate,db:Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title=%s,content=%s,published=%s WHERE id= %s RETURNING *""",
    #                (post.title,post.content,post.published, str(id),))
    # updated_post= cursor.fetchone()
    # conn.commit()
    # print(post)
    post_query =db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} was not found")
    post_query.update(updatet_post.dict(),synchronize_session=False)
    db.commit()    
        
    return  post_query.first()

# @app.patch("/update_post/{id}")
# def update_post(id:str,post:UpdatePost):
#     if post.title ==None:
#         return post[id].title == post.title
#     if post.content ==None:
#         return post[id].content == post.content
#     if post.published ==None:
#         return post[id].published == post.published
#     else:
#         cursor.execute("""UPDATE posts SET title=%s,content=%s,published=%s WHERE id= %s RETURNING *""",
#                     (post.title,post.content,post.published, str(id),))
#         updated_post= cursor.fetchone()
#         conn.commit()
#     # print(post)
#     return {"data": "updated_post successful", "deleted_post": updated_post}


# @router.patch("/update_post/{id}")
# def update_post(id: int, updated_post: schemas.UpdatePost,db:Session = Depends(get_db)):
#     # Check if any field is provided for update
#     if updated_post.title is None and updated_post.content is None and updated_postt.published is None:
#         return {"data": "No fields provided for update"}

#     # Construct the SET clause based on provided fields
#     set_clause = []
#     values = []

#     if updated_post.title is not None:
#         set_clause.append("title = %s")
#         values.append(updated_post.title)
#     if updated_post.content is not None:
#         set_clause.append("content = %s")
#         values.append(updated_post.content)
#     if updated_post.published is not None:
#         set_clause.append("published = %s")
#         values.append(updated_post.published)

#     # Construct and execute the UPDATE query
#     # update_query = f"""UPDATE posts SET {', '.join(set_clause)} WHERE id = %s RETURNING *"""
#     # cursor.execute(update_query, (*values, id))
#     # updated_post = cursor.fetchone()
#     # conn.commit()
#     post_query =db.query(models.Post).filter(models.Post.id == str(id))
#     post = post_query.first()
#     if post==None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"post with id:{id} was not found")
#     post_query.update(updated_post.dict(),synchronize_session=False)
#     db.commit()

#     return {"data": "Update successful"}
@router.patch("/update_post/{id}")
# @router.put("/update_post/{id}", response_model=schemas.Post)
def update_post(id: int, update_post: schemas.UpdatePost, db: Session = Depends(get_db)):
    # Fetch the post from the database
    post = db.query(models.Post).filter(models.Post.id == id).first()

    # Check if the post with the given id exists
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id:{id} was not found"
        )

    # Update only the specified fields
    if update_post.title:
        post.title = update_post.title
    if update_post.content:
        post.content = update_post.content
    if update_post.published is not None:
        post.published = update_post.published

    # Commit the changes to the database
    db.commit()

    # Return the updated post
    return post
