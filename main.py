from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    id: Optional[int] = None


posts = [
    {"id": 1, "title1": "demo1", "content": "this is demo post 1"},
    {"id": 2, "title2": "demo2", "content": "this is demo post 2"},
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
        return {"data": "not_found"}
    return {"data": [p for p in posts if p["id"] == post_id]}


@app.post("/posts")
def create_post(post: Post):
    new_post = post.dict()
    new_post["id"] = len(posts)+1
    posts.append(new_post)
    return {"data": new_post}
