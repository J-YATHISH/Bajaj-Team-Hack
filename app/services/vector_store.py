from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from app.utils.logger import get_logger
import os

logger = get_logger()
CHROMA_DIR = "chroma_db"

def get_vectorstore(pages: list, embedding_model):
    if os.path.exists(CHROMA_DIR) and os.listdir(CHROMA_DIR):
        logger.info("Vectorstore found. Loading from disk.")
        return Chroma(persist_directory=CHROMA_DIR, embedding_function=embedding_model)

    logger.info("Vectorstore not found. Creating new index.")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)

    # ✅ FIX: extract text from Document objects
    documents = [doc.page_content for doc in pages]
    texts = text_splitter.create_documents(documents)

    vectordb = Chroma.from_documents(
        documents=texts,
        embedding=embedding_model,
        persist_directory=CHROMA_DIR
    )
    vectordb.persist()
    logger.info("Vector store created and persisted successfully.")
    return vectordb