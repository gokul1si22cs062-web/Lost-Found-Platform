# Backend API - Posts & Ownership Logic

Read this document and install the requirements This is Member 4 SANJAY B A's implementation for the Lost & Found Platform backend .

## Responsibilities
- Create, read, update, delete posts
- Ownership check (only owner can edit/delete)
- Search & filter APIs
- Date & location handling

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
- Copy `.env.example` to `.env`
- Update `MONGODB_URL` with your MongoDB connection string (MongoDB Atlas or local)
- Update `DATABASE_NAME` if needed

3. Run the server:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Create Post
- **POST** `/api/posts`
- Body: `{ title, description, location, date_lost_found, post_type, images[], user_id }`
- Returns: Created post

### Get All Posts
- **GET** `/api/posts`
- Query params:
  - `post_type`: "lost" or "found" (optional)
  - `location`: Filter by location (optional)
  - `search`: Search in title, description, location (optional)
  - `user_id`: Filter by user (optional)
  - `limit`: Number of results (default: 50)
  - `skip`: Pagination offset (default: 0)
- Returns: List of posts

### Get Single Post
- **GET** `/api/posts/{post_id}`
- Returns: Post details

### Update Post
- **PUT** `/api/posts/{post_id}`
- Query param: `user_id` (for ownership check)
- Body: `{ title?, description?, location?, date_lost_found?, images[]? }`
- Returns: Updated post
- **Note**: Only the owner can update their post

### Delete Post
- **DELETE** `/api/posts/{post_id}`
- Query param: `user_id` (for ownership check)
- Returns: 204 No Content
- **Note**: Only the owner can delete their post

### Search by Location
- **GET** `/api/posts/search/location`
- Query params:
  - `location`: Location to search (required)
  - `post_type`: "lost" or "found" (optional)
  - `start_date`: Start date filter (optional)
  - `end_date`: End date filter (optional)
  - `limit`: Number of results (default: 50)
- Returns: List of matching posts

## Ownership Logic

All update and delete operations require the `user_id` query parameter. The API checks if the provided `user_id` matches the post's owner (`user_id` field). If not, a 403 Forbidden error is returned.

## Date Format

Dates should be in ISO format: `YYYY-MM-DD` (e.g., "2024-02-10")

## Tech Stack
- FastAPI
- Motor (async MongoDB driver)
- Pydantic (data validation)
- Python-dotenv (environment variables)

