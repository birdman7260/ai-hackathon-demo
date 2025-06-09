from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv

load_dotenv(override=True)

pdfs = Path("data").glob("*.pdf")
docs = []
for pdf in pdfs:
    loader = PyPDFLoader(str(pdf))
    docs.extend(loader.load())

chunks = RecursiveCharacterTextSplitter().split_documents(docs)
Chroma.from_documents(chunks, OpenAIEmbeddings(model="text-embedding-3-small"),
                      persist_directory="./chroma_db")