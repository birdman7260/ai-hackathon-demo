"""
NASA Document Search Module - Handles vector database and document retrieval
Provides executive-level insights from NASA technical documents
"""

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.tools import tool


class NASADocumentSearch:
    """Handles NASA document search using vector database"""
    
    def __init__(self, db_path: str = "./chroma_db", model: str = "gpt-4o-mini"):
        self.db_path = db_path
        self.model_name = model
        self._vectordb = None
        self._llm = None
    
    @property
    def vectordb(self):
        """Lazy load vector database"""
        if self._vectordb is None:
            self._vectordb = Chroma(
                persist_directory=self.db_path,
                embedding_function=OpenAIEmbeddings(model="text-embedding-3-small")
            )
        return self._vectordb
    
    @property
    def llm(self):
        """Lazy load LLM"""
        if self._llm is None:
            self._llm = ChatOpenAI(model=self.model_name)
        return self._llm
    
    def search_documents(self, query: str, k: int = 4) -> str:
        """Search NASA documents and return executive-level answer"""
        # Retrieve relevant documents
        hits = self.vectordb.similarity_search(query, k=k)
        context = "\n\n".join(d.page_content for d in hits)
        
        # Generate executive-level response
        prompt = f"""Answer for executives only.\nContext:\n{context}\nQuestion: {query}"""
        answer = self.llm.invoke(prompt).content
        return answer
    
    def get_tool(self):
        """Get the NASA search tool for agent integration"""
        search_instance = self
        
        @tool
        def nasa_document_search(query: str) -> str:
            """Search NASA documents and provide executive-level answers about space missions, engineering, and NASA policies"""
            return search_instance.search_documents(query)
        
        return nasa_document_search
    
    def get_database_info(self) -> dict:
        """Get information about the vector database"""
        try:
            collection = self.vectordb._collection
            return {
                "document_count": collection.count(),
                "collection_name": collection.name,
                "db_path": self.db_path
            }
        except Exception as e:
            return {"error": str(e)}


# Global instance for reuse
_nasa_search = None

def get_nasa_search_tool():
    """Get NASA search tool - singleton pattern"""
    global _nasa_search
    if _nasa_search is None:
        _nasa_search = NASADocumentSearch()
    return _nasa_search.get_tool()

def get_nasa_db_info() -> dict:
    """Get NASA database information"""
    global _nasa_search
    if _nasa_search is None:
        _nasa_search = NASADocumentSearch()
    return _nasa_search.get_database_info() 