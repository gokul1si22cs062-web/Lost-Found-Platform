# Quick Start Guide - Verification

Follow these steps to verify everything is working:

## Step 1: Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

## Step 2: Verify Setup

Run the pre-flight check:

```bash
python verify_setup.py
```

This will check:
- ✓ Python version (3.8+)
- ✓ All required packages installed
- ✓ MongoDB connection

## Step 3: Start the Server

```bash
uvicorn main:app --reload
```

The server will start at: `http://localhost:8000`

## Step 4: Verify API is Working

### Option A: Automatic Test (Recommended)

In a new terminal, run:
```bash
python test_api.py
```

This will test all endpoints automatically.

### Option B: Manual Testing

1. **Open API Documentation** (Interactive UI):
   - Visit: http://localhost:8000/docs
   - This provides a Swagger UI to test all endpoints

2. **Test Root Endpoint**:
   ```bash
   curl http://localhost:8000/
   ```

3. **Create a Test Post**:
   ```bash
   curl -X POST "http://localhost:8000/api/posts" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "Test Lost Wallet",
       "description": "Black leather wallet",
       "location": "Library",
       "date_lost_found": "2024-02-10",
       "post_type": "lost",
       "user_id": "test_user_123"
     }'
   ```

4. **Get All Posts**:
   ```bash
   curl http://localhost:8000/api/posts
   ```

## Step 5: Windows Users - Use Batch File

If you're on Windows, you can use the automated script:

```bash
run_and_test.bat
```

This will:
1. Verify setup
2. Start the server
3. Run tests automatically

## Troubleshooting

### MongoDB Connection Error

If you see MongoDB connection errors:

1. **For Local MongoDB**:
   - Make sure MongoDB is installed and running
   - Default connection: `mongodb://localhost:27017`

2. **For MongoDB Atlas**:
   - Create a `.env` file in the `backend` folder
   - Add: `MONGODB_URL=your_atlas_connection_string`
   - Add: `DATABASE_NAME=lost_found_db`

### Port Already in Use

If port 8000 is already in use:
```bash
uvicorn main:app --reload --port 8001
```

### Missing Dependencies

If packages are missing:
```bash
pip install -r requirements.txt
```

## Expected Results

When everything works, you should see:
- ✓ Server running on http://localhost:8000
- ✓ API docs accessible at http://localhost:8000/docs
- ✓ All test cases passing in test_api.py
- ✓ Can create, read, update, and delete posts
- ✓ Ownership checks working (403 errors for non-owners)

## Next Steps

Once verified:
1. Share the API endpoints with Member 2 (Frontend Integration)
2. Coordinate with Member 3 for JWT authentication integration
3. Work with Member 5 to ensure MongoDB schema matches

