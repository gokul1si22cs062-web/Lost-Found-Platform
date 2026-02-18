# 🚀 START HERE - Quick Verification

## Quick Commands (Copy & Paste)

### 1. Install Dependencies
```powershell
cd "D:\internship project\Lost-Found-Platform-1\backend"
py -m pip install -r requirements.txt
```

### 2. Verify Setup
```powershell
py verify_setup.py
```

### 3. Start Server
```powershell
py -m uvicorn main:app --reload
```

### 4. Test API (in NEW terminal)
```powershell
cd "D:\internship project\Lost-Found-Platform-1\backend"
py test_api.py
```

## ✅ What to Check

1. **Server Running?** 
   - Open: http://localhost:8000/docs
   - Should see Swagger UI with all endpoints

2. **All Tests Pass?**
   - Run `py test_api.py`
   - Should see: "🎉 All tests passed!"

3. **Can Create Post?**
   - Use Swagger UI at http://localhost:8000/docs
   - Try POST /api/posts endpoint

4. **Ownership Works?**
   - Try updating a post with wrong user_id
   - Should get 403 Forbidden error

## 📚 Full Guide

See `VERIFICATION_STEPS.md` for detailed instructions.

## 🆘 Troubleshooting

- **Python not found?** Use `py` instead of `python`
- **MongoDB error?** Check `VERIFICATION_STEPS.md` troubleshooting section
- **Port in use?** Change port: `--port 8001`

---

**Your API is ready when:**
- ✅ Server starts without errors
- ✅ http://localhost:8000/docs works
- ✅ All tests pass
- ✅ Can create/read/update/delete posts
- ✅ Ownership checks work (403 for non-owners)

