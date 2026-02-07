from fastapi import FastAPI
from src.api.routes import router as api_router
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Podcaster API")

app.include_router(api_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Podcaster API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
