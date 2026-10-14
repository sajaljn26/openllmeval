from .indexing import vectore_store
from langchain.tools import tool

last_retrieved_context = []
K_VALUE = 3

@tool
def collecting_info(query: str) -> str:
    """
    Search the PDF knowledge base and return relevant information
    for the user's question
    """
    global last_retrieved_context

    # Perform similarity search using the FAISS store
    docs = vectore_store.similarity_search(query, k=K_VALUE) 

    # save the Real retrieved chunks
    last_retrieved_context = [doc.page_content for doc in docs]

    return "\n\n".join(last_retrieved_context)
