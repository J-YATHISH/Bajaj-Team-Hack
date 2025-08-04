from fastapi import FastAPI
from dotenv import load_dotenv
from app.router import router

load_dotenv()

app = FastAPI(
    title="HackRx PDF QA System",
    version="1.0.0"
)

app.include_router(router, prefix="/api/v1")  # 👈 Add prefix here

@app.get("/")
def read_root():
    return {"message": "HackRx PDF QA system is running."}
