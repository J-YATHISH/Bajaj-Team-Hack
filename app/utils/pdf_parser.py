from langchain_community.document_loaders import PyPDFLoader

def parse_pdf(path: str):
    """
    Parses a PDF file using LangChain's PyPDFLoader and returns a list of Document objects.
    Each document corresponds to a page in the PDF.
    """
    loader = PyPDFLoader(path)
    return loader.load()
