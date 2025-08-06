from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.query_handler import handle_query
from app.utils.logger import get_logger
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

router = APIRouter(prefix="/hackrx", tags=["HackRx"])
logger = get_logger()

# Load TEAM_TOKEN from .env
TEAM_TOKEN = os.getenv("TEAM_TOKEN")

# Security scheme
security = HTTPBearer()

@router.api_route("/run", methods=["GET", "POST"])
async def run_query(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    # Optional: log token (disable in production)
    print("TEAM_TOKEN from .env:", TEAM_TOKEN)
    print("Authorization header:", credentials.credentials)

    if credentials.credentials != TEAM_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid token")

    if request.method == "GET":
        return {
            "message": "✅ HackRx PDF QA system is ready. Send a POST request to this endpoint with 'documents' and 'questions' in the JSON body to get answers."
        }

    # POST request
    body = await request.json()
    document_url = body.get("documents")
    questions = body.get("questions", [])

    if not document_url or not questions:
        raise HTTPException(
            status_code=400,
            detail="Missing 'documents' or 'questions' field in request body."
        )

    try:
        logger.info(f"Authenticated request for document: {document_url}")
        answers = handle_query(document_url, questions)
        return JSONResponse(content={"answers": answers})
    except Exception as e:
        logger.exception("Error processing query")
        return JSONResponse(status_code=500, content={"error": str(e)})
