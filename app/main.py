from fastapi import FastAPI
from dotenv import load_dotenv
from app.router import router
from app.utils.logger import get_logger
from app.utils.pdf_parser import parse_pdf
from app.utils.downloader import download_file_from_url
from app.services.embeddings import get_embedding_model
from app.services.vector_store import get_vectorstore
from app.services.openai_llm import get_llm

# Load environment variables
load_dotenv()

# Logger
logger = get_logger()

# Constants
DEFAULT_DOC_URL = (
    "https://hackrx.blob.core.windows.net/assets/policy.pdf?"
    "sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&"
    "sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D"
)

# Global shared components (populated at startup)
embedding_model = None
llm = None
vectorstore = None

# FastAPI instance
app = FastAPI(
    title="HackRx PDF QA System",
    version="1.0.0"
)

# Return shared components safely to other modules (query_handler etc.)
def get_components():
    return embedding_model, llm, vectorstore

# Startup event: load models and vectorstore
@app.on_event("startup")
def preload_models_and_vectorstore():
    global embedding_model, llm, vectorstore
    try:
        logger.info("🔄 Preloading embedding model and LLM...")
        embedding_model = get_embedding_model()
        llm = get_llm()
        logger.info("✅ Models loaded.")

        logger.info("📄 Preloading vectorstore for default document...")
        path = download_file_from_url(DEFAULT_DOC_URL)
        pages = parse_pdf(path)
        vectorstore = get_vectorstore(pages, embedding_model, source_url=DEFAULT_DOC_URL)
        logger.info("✅ Vectorstore loaded.")

    except Exception as e:
        logger.exception("❌ Error during startup model/vectorstore preload")

# Include API routes
app.include_router(router, prefix="/api/v1")

# Basic root route (GET, HEAD)
@app.api_route("/", methods=["GET", "HEAD"])
def read_root():
    return {
        "message": "✅ HackRx PDF QA system is running. Use POST /api/v1/hackrx/run to ask questions."
    }
