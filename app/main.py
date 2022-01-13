from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI, status, HTTPException

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    id: Optional[int] = None


posts = [
    {"id": 1, "title": "demo1", "content": "this is demo post 1"},
    {"id": 2, "title": "demo2", "content": "this is demo post 2"},
]


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/posts")
def get_all_posts():
    return {"data": posts}


@app.get("/posts/{post_id}")
def get_post_by_id(post_id: int):
    if post_id > len(posts) or post_id < 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id {post_id} is not found')
    return {"data": [p for p in posts if p["id"] == post_id]}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    new_post = post.dict()
    new_post["id"] = len(posts)+1
    posts.append(new_post)
    return {"data": new_post}


def find_index_of_post(id):
    for i, p in enumerate(posts):
        if p["id"] == id:
            return i
    return -1


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post_by_id(post_id: int):
    index = find_index_of_post(post_id)
    if index == -1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id {post_id} is not found')
    posts.pop(index)
    return {"data": f'post with id {post_id} was deleted'}


@app.put("/posts/{post_id}")
def update_post(post_id: int, post_info: Post):
    index = find_index_of_post(post_id)
    if index == -1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id {post_id} is not found')
    posts[index]["title"] = post_info.title
    posts[index]["content"] = post_info.content
    return {"data": "post update successfully"}
