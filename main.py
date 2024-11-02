# main.py

from fastapi import FastAPI, HTTPException
from models import PostCreate, PostUpdate, PostDB
from database import db
from bson import ObjectId
from typing import List

app = FastAPI()

@app.post("/posts/", response_model=PostDB)
async def create_post(post: PostCreate):
    post_data = post.dict()
    result = await db.posts.insert_one(post_data)
    post_data["_id"] = result.inserted_id
    return PostDB(**post_data)

@app.get("/posts/{post_id}", response_model=PostDB)
async def get_post(post_id: str):
    if not ObjectId.is_valid(post_id):
        raise HTTPException(status_code=400, detail="Invalid post ID")
    post = await db.posts.find_one({"_id": ObjectId(post_id)})
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return PostDB(**post)

@app.get("/posts/", response_model=List[PostDB])
async def list_posts():
    posts = await db.posts.find().to_list(1000)
    return [PostDB(**post) for post in posts]

@app.put("/posts/{post_id}", response_model=PostDB)
async def update_post(post_id: str, post: PostUpdate):
    if not ObjectId.is_valid(post_id):
        raise HTTPException(status_code=400, detail="Invalid post ID")
    update_data = {k: v for k, v in post.dict().items() if v is not None}
    if update_data:
        result = await db.posts.update_one({"_id": ObjectId(post_id)}, {"$set": update_data})
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Post not found")
    updated_post = await db.posts.find_one({"_id": ObjectId(post_id)})
    return PostDB(**updated_post)

@app.delete("/posts/{post_id}")
async def delete_post(post_id: str):
    if not ObjectId.is_valid(post_id):
        raise HTTPException(status_code=400, detail="Invalid post ID")
    result = await db.posts.delete_one({"_id": ObjectId(post_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"message": "Post deleted successfully"}
