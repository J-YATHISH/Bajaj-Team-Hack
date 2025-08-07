from app.utils.logger import get_logger
from app.utils.pdf_parser import parse_pdf
from app.utils.downloader import download_file_from_url
from app.services.vector_store import get_vectorstore
from langchain.docstore.document import Document
from app.shared import get_components, DEFAULT_DOC_URL

logger = get_logger()

def handle_query(document_url: str, questions: list) -> list:
    logger.info(f"Processing document: {document_url}")
    embedding_model, llm, preloaded_vectorstore = get_components()

    if document_url == DEFAULT_DOC_URL and preloaded_vectorstore is not None:
        vectordb = preloaded_vectorstore
        logger.info("✅ Using preloaded vectorstore from memory.")
    else:
        logger.info("📄 Downloading and creating vectorstore for new document...")
        path = download_file_from_url(document_url)
        pages = parse_pdf(path)
        vectordb = get_vectorstore(pages, embedding_model, source_url=document_url)
        logger.info("✅ New vectorstore created.")

    answers = []
    for q in questions:
        try:
            docs: list[Document] = vectordb.similarity_search(q, k=3)
            context = "\n\n".join([doc.page_content for doc in docs])

            prompt = f"""Answer the question in one line using the context below:
Context:
{context}

Question: {q}
Answer:"""

            response = llm.invoke(prompt)
            answer = response.content.strip()
            logger.info(f"Q: {q} | A: {answer}")
            answers.append(answer)
        except Exception as e:
            logger.error(f"Error answering question: {q} | {str(e)}")
            answers.append("Could not answer this question.")

    return answers
