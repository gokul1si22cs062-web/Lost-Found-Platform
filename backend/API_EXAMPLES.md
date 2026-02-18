# API Usage Examples

## Base URL
```
http://localhost:8000
```

## Interactive API Documentation
FastAPI provides automatic interactive documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Example Requests

### 1. Create a Post
```bash
POST /api/posts
Content-Type: application/json

{
  "title": "Lost Wallet",
  "description": "Black leather wallet with credit cards",
  "location": "Library, 2nd floor",
  "date_lost_found": "2024-02-10",
  "post_type": "lost",
  "images": ["https://example.com/image1.jpg"],
  "user_id": "user123"
}
```

### 2. Get All Posts
```bash
GET /api/posts
```

### 3. Filter Posts by Type
```bash
GET /api/posts?post_type=lost
```

### 4. Search Posts
```bash
GET /api/posts?search=wallet
```

### 5. Filter by Location
```bash
GET /api/posts?location=library
```

### 6. Get Posts by User
```bash
GET /api/posts?user_id=user123
```

### 7. Get Single Post
```bash
GET /api/posts/{post_id}
```

### 8. Update Post (Owner Only)
```bash
PUT /api/posts/{post_id}?user_id=user123
Content-Type: application/json

{
  "title": "Lost Wallet - Updated",
  "description": "Black leather wallet with credit cards and ID"
}
```

Or using header:
```bash
PUT /api/posts/{post_id}
X-User-ID: user123
Content-Type: application/json

{
  "location": "Library, 3rd floor"
}
```

### 9. Delete Post (Owner Only)
```bash
DELETE /api/posts/{post_id}?user_id=user123
```

Or using header:
```bash
DELETE /api/posts/{post_id}
X-User-ID: user123
```

### 10. Search by Location with Date Range
```bash
GET /api/posts/search/location?location=library&post_type=lost&start_date=2024-02-01&end_date=2024-02-15
```

## Using with cURL

```bash
# Create post
curl -X POST "http://localhost:8000/api/posts" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Found Keys",
    "description": "Set of car keys found",
    "location": "Cafeteria",
    "date_lost_found": "2024-02-09",
    "post_type": "found",
    "user_id": "user456"
  }'

# Get all lost items
curl "http://localhost:8000/api/posts?post_type=lost"

# Update post
curl -X PUT "http://localhost:8000/api/posts/{post_id}?user_id=user456" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Set of car keys with keychain"
  }'

# Delete post
curl -X DELETE "http://localhost:8000/api/posts/{post_id}?user_id=user456"
```

## Error Responses

### 403 Forbidden (Ownership Check Failed)
```json
{
  "detail": "You don't have permission to edit this post. Only the owner can edit."
}
```

### 404 Not Found
```json
{
  "detail": "Post not found"
}
```

### 400 Bad Request
```json
{
  "detail": "Invalid date format. Use ISO format (YYYY-MM-DD)"
}
```

