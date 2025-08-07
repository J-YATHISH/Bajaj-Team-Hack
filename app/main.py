from fastapi import FastAPI
from dotenv import load_dotenv
from app.router import router
from app.utils.pdf_parser import parse_pdf
from app.utils.downloader import download_file_from_url
from app.shared import logger, get_components, DEFAULT_DOC_URL, embedding_model, llm, vectorstore
from app.services.embeddings import get_embedding_model
from app.services.vector_store import get_vectorstore
from app.services.openai_llm import get_llm

load_dotenv()

app = FastAPI(
title="HackRx PDF QA System",
version="1.0.0"
)

@app.on_event("startup")
def preload_models_and_vectorstore():
from app import shared # avoid circular import at module level
try:
logger.info("🔄 Preloading embedding model and LLM...")
shared.embedding_model = get_embedding_model()
shared.llm = get_llm()
logger.info("✅ Models loaded.")

vbnet
Copy
Edit
    logger.info("📄 Preloading vectorstore for default document...")
    path = download_file_from_url(DEFAULT_DOC_URL)
    pages = parse_pdf(path)
    shared.vectorstore = get_vectorstore(pages, shared.embedding_model, source_url=DEFAULT_DOC_URL)
    logger.info("✅ Vectorstore loaded.")

except Exception as e:
    logger.exception("❌ Error during startup model/vectorstore preload")
app.include_router(router, prefix="/api/v1")

@app.api_route("/", methods=["GET", "HEAD"])
def read_root():
return {"message": "✅ HackRx PDF QA system is running."}
