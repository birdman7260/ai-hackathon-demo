#!/usr/bin/env python3
"""
Debug script to test embedding and retrieval pipeline
"""

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
import time

load_dotenv(override=True)

def test_embeddings():
    """Test if embeddings are working"""
    print("🧪 Testing OpenAI Embeddings...")
    try:
        embedder = OpenAIEmbeddings(model="text-embedding-3-small")
        
        # Test single embedding
        start_time = time.time()
        test_embedding = embedder.embed_query("test query")
        end_time = time.time()
        
        print(f"  ✅ Single embedding: {len(test_embedding)} dimensions")
        print(f"  ⏱️  Time taken: {end_time - start_time:.2f}s")
        
        # Test batch embeddings
        start_time = time.time()
        batch_embeddings = embedder.embed_documents(["doc 1", "doc 2", "doc 3"])
        end_time = time.time()
        
        print(f"  ✅ Batch embeddings: {len(batch_embeddings)} documents")
        print(f"  ⏱️  Batch time: {end_time - start_time:.2f}s")
        
        return True
    except Exception as e:
        print(f"  ❌ Embedding failed: {str(e)}")
        return False

def test_vector_database():
    """Test vector database connection and contents"""
    print("\n📊 Testing Vector Database...")
    try:
        vectordb = Chroma(
            persist_directory="./chroma_db", 
            embedding_function=OpenAIEmbeddings(model="text-embedding-3-small")
        )
        
        # Get collection info
        collection = vectordb._collection
        count = collection.count()
        print(f"  ✅ Database loaded: {count} documents")
        
        # Test retrieval with different queries
        test_queries = [
            "NASA risk management",
            "technical risk mitigation", 
            "systems engineering",
            "Artemis mission"
        ]
        
        for query in test_queries:
            start_time = time.time()
            hits = vectordb.similarity_search(query, k=3)
            end_time = time.time()
            
            print(f"  🔍 Query: '{query}'")
            print(f"     Retrieved: {len(hits)} docs in {end_time - start_time:.2f}s")
            if hits:
                preview = hits[0].page_content.replace('\n', ' ')[:100]
                print(f"     Preview: {preview}...")
        
        return True
    except Exception as e:
        print(f"  ❌ Vector DB failed: {str(e)}")
        return False

def test_similarity_scores():
    """Test retrieval with similarity scores"""
    print("\n🎯 Testing Similarity Scores...")
    try:
        vectordb = Chroma(
            persist_directory="./chroma_db", 
            embedding_function=OpenAIEmbeddings(model="text-embedding-3-small")
        )
        
        query = "risk mitigation strategies"
        docs_with_scores = vectordb.similarity_search_with_score(query, k=5)
        
        print(f"  Query: '{query}'")
        for i, (doc, score) in enumerate(docs_with_scores):
            preview = doc.page_content.replace('\n', ' ')[:80]
            print(f"  {i+1}. Score: {score:.4f} | {preview}...")
            
        return True
    except Exception as e:
        print(f"  ❌ Similarity test failed: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting Embedding Pipeline Debug\n")
    
    # Run tests
    embedding_ok = test_embeddings()
    vector_ok = test_vector_database()
    similarity_ok = test_similarity_scores()
    
    print(f"\n📋 Summary:")
    print(f"  Embeddings: {'✅' if embedding_ok else '❌'}")
    print(f"  Vector DB: {'✅' if vector_ok else '❌'}")
    print(f"  Similarity: {'✅' if similarity_ok else '❌'}")
    
    if all([embedding_ok, vector_ok, similarity_ok]):
        print("\n🎉 All systems working! Your embedding pipeline is healthy.")
    else:
        print("\n⚠️  Some issues detected. Check the errors above.")

if __name__ == "__main__":
    main() 