#!/usr/bin/env python3
"""
Test retrieval with sample queries
"""

from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv(override=True)

def test_retrieval():
    """Test retrieval with sample queries"""
    vectordb = Chroma(
        persist_directory='./chroma_db', 
        embedding_function=OpenAIEmbeddings(model='text-embedding-3-small')
    )
    
    test_queries = [
        'NASA risk management', 
        'Artemis mission', 
        'systems engineering', 
        'technical requirements'
    ]
    
    print('Testing retrieval with sample queries:')
    
    for query in test_queries:
        hits = vectordb.similarity_search(query, k=2)
        print(f'\n🔍 Query: "{query}"')
        print(f'   📊 Retrieved: {len(hits)} documents')
        if hits:
            preview = hits[0].page_content.replace('\n', ' ')[:100]
            print(f'   📝 Preview: {preview}...')

if __name__ == "__main__":
    test_retrieval() 