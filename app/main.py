from fastapi import FastAPI
from dotenv import load_dotenv
from app.router import router

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="HackRx PDF QA System",
    version="1.0.0"
)

# Include API routes with prefix
app.include_router(router, prefix="/api/v1")

# Root endpoint for GET and HEAD requests
@app.api_route("/", methods=["GET", "HEAD"])
def read_root():
    return {"message": "HackRx PDF QA system is running."}
