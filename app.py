import json
from sys import api_version
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Text, Optional
from datetime import datetime
from uuid import uuid4 as uuid

app = FastAPI()

# db = json.load( open('./db/tei-db-data.json'))
db = []

class Post(BaseModel):
    id: Optional[str]
    title: str
    author: str
    content: Text
    created_at: datetime = datetime.now()
    published_at: Optional[datetime]
    published: bool = False

api_version = "/api/v1"

@app.get('/')
def get_root():
    return {"msg":"Welcome to my FastAPI"}
    
@app.get(api_version + '/posts')
def get_posts():
    return db

@app.get( api_version + '/posts/{post_id}')
def get_post(post_id: str):
    for post in db:
        if post["id"] == post_id:
            return post
    raise HTTPException(status_code=404, detail="Resource not found")

@app.post( api_version + '/posts')
def save_post(post: Post):
    post.id = str(uuid())
    db.append(post.dict())
    return (post.dict())

@app.put( api_version + '/posts/{post_id}')
def delete_post(post_id: str, udpatedPost: Post):
    for index, post in enumerate(db):
        if post["id"] == post_id:
            db[index]["title"] = udpatedPost.title
            db[index]["author"] = udpatedPost.author
            db[index]["content"] = udpatedPost.content
            return { "msg": "Resource updated successfully"}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.delete( api_version + '/posts/{post_id}')
def delete_post(post_id: str):
    for index, post in enumerate(db):
        if post["id"] == post_id:
            db.pop(index)
            return { "msg": "Resource deleted successfully"}
    raise HTTPException(status_code=404, detail="Resource not found")