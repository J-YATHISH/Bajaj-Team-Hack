from app.utils.logger import get_logger
from app.utils.pdf_parser import parse_pdf
from app.utils.downloader import download_file_from_url
from app.services.embeddings import get_embedding_model
from app.services.vector_store import get_vectorstore
from app.services.openai_llm import get_llm
from langchain.chains import RetrievalQA

logger = get_logger()

def handle_query(document_url: str, questions: list) -> list:
    logger.info(f"Processing document: {document_url}")
    
    path = download_file_from_url(document_url)
    pages = parse_pdf(path)
    logger.info(f"Loaded {len(pages)} pages from document.")

    embeddings = get_embedding_model()
    vectordb = get_vectorstore(pages, embeddings)

    logger.info("Loading LLM...")
    llm = get_llm()
    logger.info("Creating RetrievalQA chain")
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=vectordb.as_retriever())

    answers = []
    for q in questions:
        try:
            raw_answer = qa_chain.invoke({"query": q})
            logger.info(f"Raw LLM response: {raw_answer}")

            # Extract summary using the same LLM, reduce to one line
            concise = llm.invoke(f"Summarize in one line: {raw_answer['result']}")
            answers.append(concise.content.strip())
        except Exception as e:
            logger.error(f"Error answering question: {q} | {str(e)}")
            answers.append("Could not answer this question.")
    
    return answers