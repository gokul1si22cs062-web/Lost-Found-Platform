# run_test.py
from fastapi import FastAPI
import uvicorn
from authentication.auth_routes import router

app = FastAPI()
app.include_router(router)

@app.get("/")
def home():
    return {"message": "Welcome to the Member 3 Auth System! Visit /docs to test."}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)