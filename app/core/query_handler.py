from app.utils.logger import get_logger
from app.utils.pdf_parser import parse_pdf
from app.utils.downloader import download_file_from_url
from app.services.vector_store import get_vectorstore
from langchain.docstore.document import Document
from app.main import get_components, DEFAULT_DOC_URL

logger = get_logger()

def handle_query(document_url: str, questions: list) -> list:
    logger.info(f"📥 Processing document: {document_url}")

    # Load preloaded components  
    embedding_model, llm, preloaded_vectorstore = get_components()  

    # Use cached vectorstore if it's the default doc  
    if document_url == DEFAULT_DOC_URL and preloaded_vectorstore is not None:  
        vectordb = preloaded_vectorstore  
        logger.info("✅ Using preloaded vectorstore from memory.")  
    else:  
        try:  
            logger.info("⬇️ Downloading and parsing custom document...")  
            path = download_file_from_url(document_url)  
            pages = parse_pdf(path)  
            vectordb = get_vectorstore(pages, embedding_model, source_url=document_url)  
            logger.info("✅ Vectorstore created for custom document.")  
        except Exception as e:  
            logger.exception("❌ Error loading custom document")  
            return ["Could not load the document."] * len(questions)  

    answers = []  
    for q in questions:  
        try:  
            docs: list[Document] = vectordb.similarity_search(q, k=3)  
            context = "\n\n".join([doc.page_content for doc in docs])  

            prompt = f"""Answer the question in one line using only the context below.
If the answer is not in the context, say "I don't know".
Context:
{context}

Question: {q}
Answer:"""

            response = llm.invoke(prompt)  
            answer = response.content.strip()  
            logger.info(f"✅ Q: {q}\nA: {answer}")  
            answers.append(answer)  
        except Exception as e:  
            logger.error(f"❌ Error answering question: {q} | {str(e)}")  
            answers.append("Could not answer this question.")  

    return answers
