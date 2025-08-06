from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from app.utils.logger import get_logger
import os

logger = get_logger()
CHROMA_DIR = "chroma_db"

def get_vectorstore(pages: list, embedding_model, source_url: str=None):
    if os.path.exists(CHROMA_DIR) and os.listdir(CHROMA_DIR):
        logger.info("Vectorstore found. Loading from disk.")
        return Chroma(persist_directory=CHROMA_DIR, embedding_function=embedding_model)

    logger.info("Vectorstore not found. Creating new index.")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)

    # Extract raw text from pages
    raw_texts = [doc.page_content for doc in pages]
    chunks = text_splitter.create_documents(raw_texts)

    # Add source_url as metadata
    documents = [
        Document(page_content=chunk.page_content, metadata={"source": source_url})
        for chunk in chunks
    ]

    vectordb = Chroma.from_documents(
        documents=documents,
        embedding=embedding_model,
        persist_directory=CHROMA_DIR
    )
    vectordb.persist()
    logger.info("✅ Vector store created and persisted successfully.")
    return vectordb
