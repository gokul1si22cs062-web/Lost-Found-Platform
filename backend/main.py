from fastapi import FastAPI, HTTPException, Depends, status, Header, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from bson import ObjectId
import motor.motor_asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

# TODO: When Member 3's JWT authentication is ready, replace get_current_user_id
# with a dependency that extracts user_id from JWT token
# Example: 
# from fastapi.security import HTTPBearer
# security = HTTPBearer()
# async def get_current_user_id(token: str = Depends(security)) -> str:
#     # Decode JWT and return user_id
#     return decoded_token["user_id"]

app = FastAPI(title="Lost & Found Platform API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB connection
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "lost_found_db")

client = AsyncIOMotorClient(MONGODB_URL)
db = client[DATABASE_NAME]
posts_collection = db["posts"]

# Pydantic models
class PostBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    location: str = Field(..., min_length=1, max_length=200)
    date_lost_found: str  # ISO format date string
    post_type: str = Field(..., pattern="^(lost|found)$")
    images: Optional[List[str]] = []  # List of image URLs

class PostCreate(PostBase):
    user_id: str  # Owner's user ID

class PostUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1)
    location: Optional[str] = Field(None, min_length=1, max_length=200)
    date_lost_found: Optional[str] = None
    images: Optional[List[str]] = None

class PostResponse(PostBase):
    id: str
    user_id: str
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True

# Helper function to convert ObjectId to string
def post_helper(post) -> dict:
    return {
        "id": str(post["_id"]),
        "title": post["title"],
        "description": post["description"],
        "location": post["location"],
        "date_lost_found": post["date_lost_found"],
        "post_type": post["post_type"],
        "images": post.get("images", []),
        "user_id": post["user_id"],
        "created_at": post["created_at"],
        "updated_at": post["updated_at"]
    }

# Helper function to get user_id from request
# For now, accepts user_id as query param or header
# TODO: Replace with JWT token extraction when auth is integrated
async def get_current_user_id(
    user_id: Optional[str] = Query(None),
    x_user_id: Optional[str] = Header(None, alias="X-User-ID")
) -> str:
    """Get user_id from query param or header. Will be replaced with JWT extraction."""
    if user_id:
        return user_id
    if x_user_id:
        return x_user_id
    raise HTTPException(
        status_code=401,
        detail="User ID is required. Provide 'user_id' query param or 'X-User-ID' header"
    )

# Routes

@app.get("/")
async def root():
    return {"message": "Lost & Found Platform API", "version": "1.0.0"}

# Create a new post
@app.post("/api/posts", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(post: PostCreate):
    try:
        # Validate date format
        datetime.fromisoformat(post.date_lost_found.replace('Z', '+00:00'))
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use ISO format (YYYY-MM-DD)")
    
    post_dict = {
        "title": post.title,
        "description": post.description,
        "location": post.location,
        "date_lost_found": post.date_lost_found,
        "post_type": post.post_type,
        "images": post.images or [],
        "user_id": post.user_id,
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    }
    
    result = await posts_collection.insert_one(post_dict)
    created_post = await posts_collection.find_one({"_id": result.inserted_id})
    
    return post_helper(created_post)

# Get all posts with optional filters
@app.get("/api/posts", response_model=List[PostResponse])
async def get_posts(
    post_type: Optional[str] = None,
    location: Optional[str] = None,
    search: Optional[str] = None,
    user_id: Optional[str] = None,
    limit: int = 50,
    skip: int = 0
):
    query = {}
    
    # Filter by post type (lost/found)
    if post_type:
        if post_type not in ["lost", "found"]:
            raise HTTPException(status_code=400, detail="post_type must be 'lost' or 'found'")
        query["post_type"] = post_type
    
    # Filter by location (case-insensitive partial match)
    if location:
        query["location"] = {"$regex": location, "$options": "i"}
    
    # Filter by user_id (to get posts by a specific user)
    if user_id:
        query["user_id"] = user_id
    
    # Search in title and description (case-insensitive)
    if search:
        query["$or"] = [
            {"title": {"$regex": search, "$options": "i"}},
            {"description": {"$regex": search, "$options": "i"}},
            {"location": {"$regex": search, "$options": "i"}}
        ]
    
    cursor = posts_collection.find(query).sort("created_at", -1).skip(skip).limit(limit)
    posts = await cursor.to_list(length=limit)
    
    return [post_helper(post) for post in posts]

# Get a single post by ID
@app.get("/api/posts/{post_id}", response_model=PostResponse)
async def get_post(post_id: str):
    try:
        post = await posts_collection.find_one({"_id": ObjectId(post_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid post ID format")
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    return post_helper(post)

# Update a post (only owner can update)
@app.put("/api/posts/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: str, 
    post_update: PostUpdate, 
    user_id: str = Depends(get_current_user_id)
):
    # Check if post exists
    try:
        existing_post = await posts_collection.find_one({"_id": ObjectId(post_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid post ID format")
    
    if not existing_post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Check ownership
    if existing_post.get("user_id") != user_id:
        raise HTTPException(
            status_code=403, 
            detail="You don't have permission to edit this post. Only the owner can edit."
        )
    
    # Build update dictionary (only include fields that are provided)
    update_dict = {"updated_at": datetime.utcnow().isoformat()}
    
    if post_update.title is not None:
        update_dict["title"] = post_update.title
    if post_update.description is not None:
        update_dict["description"] = post_update.description
    if post_update.location is not None:
        update_dict["location"] = post_update.location
    if post_update.date_lost_found is not None:
        # Validate date format
        try:
            datetime.fromisoformat(post_update.date_lost_found.replace('Z', '+00:00'))
            update_dict["date_lost_found"] = post_update.date_lost_found
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use ISO format (YYYY-MM-DD)")
    if post_update.images is not None:
        update_dict["images"] = post_update.images
    
    await posts_collection.update_one(
        {"_id": ObjectId(post_id)},
        {"$set": update_dict}
    )
    
    updated_post = await posts_collection.find_one({"_id": ObjectId(post_id)})
    return post_helper(updated_post)

# Delete a post (only owner can delete)
@app.delete("/api/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: str, 
    user_id: str = Depends(get_current_user_id)
):
    # Check if post exists
    try:
        existing_post = await posts_collection.find_one({"_id": ObjectId(post_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid post ID format")
    
    if not existing_post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Check ownership
    if existing_post.get("user_id") != user_id:
        raise HTTPException(
            status_code=403, 
            detail="You don't have permission to delete this post. Only the owner can delete."
        )
    
    await posts_collection.delete_one({"_id": ObjectId(post_id)})
    return None

# Get posts by location (with date range filter)
@app.get("/api/posts/search/location", response_model=List[PostResponse])
async def search_by_location(
    location: str,
    post_type: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    limit: int = 50
):
    query = {"location": {"$regex": location, "$options": "i"}}
    
    if post_type:
        if post_type not in ["lost", "found"]:
            raise HTTPException(status_code=400, detail="post_type must be 'lost' or 'found'")
        query["post_type"] = post_type
    
    # Date range filter
    if start_date or end_date:
        date_query = {}
        if start_date:
            date_query["$gte"] = start_date
        if end_date:
            date_query["$lte"] = end_date
        query["date_lost_found"] = date_query
    
    cursor = posts_collection.find(query).sort("created_at", -1).limit(limit)
    posts = await cursor.to_list(length=limit)
    
    return [post_helper(post) for post in posts]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

