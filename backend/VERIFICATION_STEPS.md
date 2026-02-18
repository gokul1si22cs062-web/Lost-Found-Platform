# Step-by-Step Verification Guide

Follow these steps in order to verify your backend is working:

## Prerequisites Check

1. **Python Installation**
   ```powershell
   py --version
   ```
   Should show Python 3.8 or higher

2. **Install Dependencies**
   ```powershell
   cd "D:\internship project\Lost-Found-Platform-1\backend"
   py -m pip install -r requirements.txt
   ```
   
   If pip is not available, install it first:
   ```powershell
   py -m ensurepip --upgrade
   ```

## Step 1: Verify Setup

Run the pre-flight check:
```powershell
py verify_setup.py
```

**Expected Output:**
```
✓ Python 3.x.x
✓ fastapi
✓ uvicorn
✓ motor
✓ pydantic
✓ MongoDB connection successful (or connection error with instructions)
```

## Step 2: Start the Server

In the backend directory, run:
```powershell
py -m uvicorn main:app --reload
```

**Expected Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**Keep this terminal window open!**

## Step 3: Test the API

### Option A: Use the Interactive API Docs (Easiest)

1. Open your browser
2. Go to: **http://localhost:8000/docs**
3. You'll see a Swagger UI with all endpoints
4. Click "Try it out" on any endpoint to test it

### Option B: Run Automated Tests

Open a **NEW terminal window** (keep server running), then:
```powershell
cd "D:\internship project\Lost-Found-Platform-1\backend"
py test_api.py
```

**Expected Output:**
```
✓ PASS - Root
✓ PASS - Create Post
✓ PASS - Get All Posts
✓ PASS - Get Single Post
✓ PASS - Search Posts
✓ PASS - Filter by Type
✓ PASS - Update Post
✓ PASS - Location Search
✓ PASS - Delete Post

🎉 All tests passed! Your API is working correctly.
```

### Option C: Manual Testing with Browser

1. **Root endpoint**: http://localhost:8000/
   - Should show: `{"message":"Lost & Found Platform API","version":"1.0.0"}`

2. **Get all posts**: http://localhost:8000/api/posts
   - Should show: `[]` (empty array initially)

3. **API Documentation**: http://localhost:8000/docs
   - Interactive UI to test all endpoints

## Step 4: Test Key Features

### Test 1: Create a Post

Using the Swagger UI at http://localhost:8000/docs:

1. Find **POST /api/posts**
2. Click "Try it out"
3. Use this example:
```json
{
  "title": "Lost Wallet",
  "description": "Black leather wallet with credit cards",
  "location": "Library, 2nd floor",
  "date_lost_found": "2024-02-10",
  "post_type": "lost",
  "images": [],
  "user_id": "user123"
}
```
4. Click "Execute"
5. Should return 201 with the created post

### Test 2: Get All Posts

1. Find **GET /api/posts**
2. Click "Try it out" → "Execute"
3. Should return the post you just created

### Test 3: Ownership Check (Update)

1. Find **PUT /api/posts/{post_id}**
2. Use the post_id from Test 1
3. Set `user_id` query param to `user123` (correct owner)
4. Update title to "Lost Wallet - Updated"
5. Should return 200 (success)

6. Now try with `user_id=wrong_user`
7. Should return 403 (Forbidden - ownership check works!)

### Test 4: Ownership Check (Delete)

1. Find **DELETE /api/posts/{post_id}**
2. Try with wrong user_id first → Should get 403
3. Try with correct user_id → Should get 204 (deleted)

### Test 5: Search and Filter

1. Create a few test posts (different types, locations)
2. Test search: `GET /api/posts?search=wallet`
3. Test filter: `GET /api/posts?post_type=lost`
4. Test location: `GET /api/posts?location=library`

## Verification Checklist

- [ ] Python 3.8+ installed
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] MongoDB accessible (local or Atlas)
- [ ] Server starts without errors
- [ ] Root endpoint returns success
- [ ] Can create a post (POST /api/posts)
- [ ] Can get all posts (GET /api/posts)
- [ ] Can get single post (GET /api/posts/{id})
- [ ] Can update post with correct owner (PUT /api/posts/{id})
- [ ] Cannot update post with wrong owner (403 error)
- [ ] Can delete post with correct owner (DELETE /api/posts/{id})
- [ ] Cannot delete post with wrong owner (403 error)
- [ ] Search functionality works
- [ ] Filter by type works
- [ ] Filter by location works

## Troubleshooting

### "Module not found" errors
```powershell
py -m pip install -r requirements.txt
```

### MongoDB connection error
- **Local MongoDB**: Make sure MongoDB service is running
- **MongoDB Atlas**: Create `.env` file with your connection string:
  ```
  MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/
  DATABASE_NAME=lost_found_db
  ```

### Port 8000 already in use
```powershell
py -m uvicorn main:app --reload --port 8001
```

### Server won't start
- Check for syntax errors in `main.py`
- Make sure you're in the `backend` directory
- Check Python version: `py --version` (need 3.8+)

## Success Indicators

✅ **Everything is working if:**
- Server starts without errors
- http://localhost:8000/docs opens and shows all endpoints
- You can create, read, update, and delete posts
- Ownership checks work (403 for non-owners)
- Search and filter work correctly

## Next Steps After Verification

Once everything works:
1. ✅ Your part (Member 4) is complete!
2. Share API endpoints with Member 2 (Frontend)
3. Coordinate with Member 3 for JWT integration
4. Work with Member 5 on MongoDB schema alignment

