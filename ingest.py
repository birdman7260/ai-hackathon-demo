# =============================================================================
# CA DEQ Document Ingestion Pipeline
# =============================================================================
# This script processes CA DEQ PDF documents into a searchable vector database.
# It extracts text from PDFs, splits them into manageable chunks, and creates
# embeddings using OpenAI's embedding model for semantic search capabilities.
# =============================================================================

# Core imports for file handling and document processing
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# OpenAI integration for embeddings
from langchain_openai import OpenAIEmbeddings

# Vector database for semantic search
from langchain_chroma import Chroma

# Environment configuration
from dotenv import load_dotenv

# Load environment variables with override to ensure .env file takes precedence
# This is crucial for getting the OpenAI API key needed for embeddings
load_dotenv(override=True)

# =============================================================================
# DOCUMENT DISCOVERY
# =============================================================================
# Find all PDF files in the data directory for processing
# Uses pathlib.Path.glob() for cross-platform file discovery

print("📄 Discovering CA DEQ PDF documents...")
pdfs = Path("data").glob("*.pdf")
pdf_list = list(pdfs)  # Convert to list to check count
print(f"📋 Found {len(pdf_list)} CA DEQ PDF files to process")

# =============================================================================
# DOCUMENT LOADING
# =============================================================================
# Load and extract text content from each PDF document
# PyPDFLoader handles the PDF parsing and text extraction

docs = []
print("📖 Loading and extracting text from CA DEQ PDFs...")

for pdf in pdf_list:
    print(f"   📄 Processing: {pdf.name}")
    
    # Create PDF loader for current document
    # PyPDFLoader extracts text page by page, preserving document structure
    loader = PyPDFLoader(str(pdf))
    
    # Load document and extend our docs list
    # Each page becomes a separate document with metadata
    docs.extend(loader.load())

print(f"✅ Loaded {len(docs)} pages from {len(pdf_list)} CA DEQ PDF files")

# =============================================================================
# TEXT CHUNKING
# =============================================================================
# Split large documents into smaller, semantically meaningful chunks
# This improves retrieval accuracy and fits within LLM context windows

print("✂️  Splitting CA DEQ documents into searchable chunks...")

# Initialize the text splitter with optimized settings
# RecursiveCharacterTextSplitter preserves semantic boundaries (paragraphs, sentences)
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,        # Maximum characters per chunk
    chunk_overlap=200,      # Overlap between chunks to preserve context
    length_function=len,    # Use character count for measuring length
    separators=["\n\n", "\n", " ", ""]  # Split on paragraphs first, then sentences
)

# Split all documents into chunks
chunks = text_splitter.split_documents(docs)
print(f"📋 Created {len(chunks)} searchable CA DEQ chunks")

# =============================================================================
# VECTOR DATABASE CREATION
# =============================================================================
# Create embeddings for each chunk and store in Chroma vector database
# This enables semantic search based on meaning rather than just keywords

print("🧠 Creating embeddings and building CA DEQ vector database...")
print("   (This may take a few minutes for large document collections)")

# Create vector database with OpenAI embeddings
# - Documents are converted to numerical vectors using text-embedding-3-small
# - Chroma stores vectors with metadata for efficient similarity search
# - persist_directory ensures the database persists between sessions
vectordb = Chroma.from_documents(
    documents=chunks,                                           # Document chunks to embed
    embedding=OpenAIEmbeddings(model="text-embedding-3-small"), # OpenAI embedding model
    persist_directory="./chroma_db"                            # Local storage location
)

print(f"✅ CA DEQ vector database created successfully!")
print(f"📊 Database contains {len(chunks)} embedded CA DEQ document chunks")
print(f"💾 Database persisted to: ./chroma_db")
print("\n🎉 CA DEQ document ingestion complete! Ready for Q&A queries.")