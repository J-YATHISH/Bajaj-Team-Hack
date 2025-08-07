from app.utils.logger import get_logger
from app.utils.pdf_parser import parse_pdf
from app.utils.downloader import download_file_from_url
from app.services.embeddings import get_embedding_model
from app.services.vector_store import get_vectorstore
from app.services.openai_llm import get_llm

DEFAULT_DOC_URL = (
    "https://hackrx.blob.core.windows.net/assets/policy.pdf?"
    "sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&"
    "sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D"
)

logger = get_logger()

embedding_model = None
llm = None
vectorstore = None

def preload_components():
    global embedding_model, llm, vectorstore

    logger.info("🔄 Preloading models and vectorstore...")
    embedding_model = get_embedding_model()
    llm = get_llm()
    logger.info("✅ Embedding model and LLM loaded.")

    path = download_file_from_url(DEFAULT_DOC_URL)
    pages = parse_pdf(path)
    vectorstore = get_vectorstore(pages, embedding_model, source_url=DEFAULT_DOC_URL)
    logger.info("✅ Vectorstore for default document ready.")

def get_components():
    return embedding_model, llm, vectorstore
