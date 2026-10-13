from dotenv import load_dotenv
from .file_reader import extract_paragraphs
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import os

load_dotenv()

# Using a high-quality open-source embedding model
# all-MiniLM-L6-v2 is fast and lightweight
embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Initialize FAISS vector store
# We first extract the chunks and then create the store from them
chunks = extract_paragraphs("pdfs/Penguins_ACL.pdf")
vectore_store = FAISS.from_texts(texts=chunks, embedding=embedding)

print(f"Indexed {len(chunks)} chunks using FAISS and HuggingFaceEmbeddings")
