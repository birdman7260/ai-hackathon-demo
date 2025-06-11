"""
NASA Document Search Module - Vector Database and RAG Implementation

This module implements the NASA document search capability using a Retrieval-Augmented
Generation (RAG) approach. It provides executive-level insights from NASA technical
documents by combining semantic search with LLM generation.

RAG ARCHITECTURE:
1. Vector Database (Chroma): Stores document embeddings for semantic search
2. Embedding Model: Converts text to vector representations for similarity matching
3. Retrieval: Finds most relevant document chunks for a given query
4. Generation: Uses LLM to synthesize executive-level responses from retrieved context

DESIGN PATTERNS:
- Lazy Loading: Database and LLM initialized only when needed (performance)
- Singleton Pattern: Global instances for efficient resource usage
- Factory Pattern: Tool creation for agent integration
- Template Method: Consistent search-then-generate workflow

PERFORMANCE OPTIMIZATIONS:
- Lazy loading prevents unnecessary resource allocation at startup
- Vector similarity search provides fast semantic matching
- Chunked documents enable precise context retrieval
- Executive-focused prompts produce concise, relevant responses
"""

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.tools import tool


class NASADocumentSearch:
    """
    NASA document search engine using vector database and LLM generation.
    
    This class implements a complete RAG (Retrieval-Augmented Generation) pipeline:
    
    COMPONENTS:
    - Vector Database (Chroma): Stores preprocessed NASA document embeddings
    - Embedding Model: Converts queries to vectors for semantic similarity
    - LLM: Generates executive-level responses from retrieved context
    
    WORKFLOW:
    1. Query received → Convert to embedding vector
    2. Semantic search → Find most similar document chunks
    3. Context assembly → Combine relevant chunks
    4. LLM generation → Synthesize executive-level response
    
    LAZY LOADING DESIGN:
    Database and LLM connections are created only when first accessed.
    This prevents resource allocation during module import and enables
    faster application startup times.
    """
    
    def __init__(self, db_path: str = "./chroma_db", model: str = "gpt-4.1"):
        """
        Initialize NASA search with configurable paths and models.
        
        Args:
            db_path: Path to Chroma vector database directory
            model: OpenAI model name for response generation
            
        INITIALIZATION STRATEGY:
        - Store configuration parameters only
        - Defer expensive operations (DB connection, model loading) until needed
        - Enable multiple instances with different configurations
        """
        self.db_path = db_path
        self.model_name = model
        # Lazy loading: These will be initialized when first accessed
        self._vectordb = None
        self._llm = None
    
    @property
    def vectordb(self):
        """
        Lazy-loaded vector database connection.
        
        Returns:
            Chroma vector database instance with OpenAI embeddings
            
        LAZY LOADING BENEFITS:
        - Faster module import and application startup
        - Database connection only created when actually needed
        - Memory efficient (no unused connections)
        - Error isolation (connection errors only when using feature)
        
        EMBEDDING MODEL:
        Uses "text-embedding-3-small" for optimal cost/performance balance.
        This model provides good semantic understanding for NASA technical content
        while maintaining reasonable API costs.
        """
        if self._vectordb is None:
            self._vectordb = Chroma(
                persist_directory=self.db_path,
                embedding_function=OpenAIEmbeddings(model="text-embedding-3-small")
            )
        return self._vectordb
    
    @property
    def llm(self):
        """
        Lazy-loaded Large Language Model connection.
        
        Returns:
            ChatOpenAI instance configured for response generation
            
        MODEL SELECTION:
        Uses gpt-4.1 by default for optimal cost/performance:
        - Sufficient capability for executive summaries
        - Lower cost than GPT-4 for high-volume usage  
        - Fast response times for interactive applications
        """
        if self._llm is None:
            self._llm = ChatOpenAI(model=self.model_name)
        return self._llm
    
    def search_documents(self, query: str, k: int = 4) -> str:
        """
        Search NASA documents and generate executive-level response.
        
        Args:
            query: User's search query or question
            k: Number of document chunks to retrieve (default: 4)
            
        Returns:
            Executive-level response synthesized from retrieved documents
            
        RAG IMPLEMENTATION:
        This method implements the complete RAG (Retrieval-Augmented Generation) pipeline:
        
        1. RETRIEVAL PHASE:
           - Convert query to embedding vector
           - Perform semantic similarity search in vector database
           - Retrieve top-k most relevant document chunks
           
        2. CONTEXT ASSEMBLY:
           - Combine retrieved chunks into coherent context
           - Preserve document boundaries with double newlines
           - Maintain source information for potential citation
           
        3. GENERATION PHASE:
           - Create executive-focused prompt template
           - Include retrieved context and original query
           - Generate response optimized for executive audiences
           
        EXECUTIVE FOCUS:
        The prompt specifically targets executive-level responses:
        - Strategic insights rather than technical details
        - Actionable information and recommendations
        - Concise, high-impact communication style
        """
        # RETRIEVAL PHASE
        # Perform semantic similarity search to find most relevant document chunks
        # k=4 provides good balance between context richness and prompt length
        hits = self.vectordb.similarity_search(query, k=k)
        
        # CONTEXT ASSEMBLY
        # Combine retrieved document chunks with clear separation
        # Double newlines preserve readability and document boundaries
        context = "\n\n".join(d.page_content for d in hits)
        
        # GENERATION PHASE
        # Create prompt optimized for executive-level responses
        # Template includes context, query, and specific executive instruction
        prompt = f"""Answer for executives only.\nContext:\n{context}\nQuestion: {query}"""
        
        # Generate response using configured LLM
        answer = self.llm.invoke(prompt).content
        return answer
    
    def get_tool(self):
        """
        Create LangChain tool for agent integration.
        
        Returns:
            LangChain tool that can be used by AI agents
            
        TOOL PATTERN:
        This method implements the Tool Pattern for LangChain integration:
        - Wraps the search functionality in a tool interface
        - Provides proper metadata for tool discovery
        - Enables seamless integration with LangChain agents
        
        CLOSURE DESIGN:
        Uses closure to maintain reference to this instance while
        creating a standalone tool function. This enables:
        - Clean tool interface without class references
        - Proper instance method access within tool function
        - Memory-efficient tool creation
        """
        # Capture instance reference for closure
        search_instance = self
        
        @tool
        def nasa_document_search(query: str) -> str:
            """Search NASA documents and provide executive-level answers about space missions, engineering, and NASA policies"""
            # Delegate to instance method with full functionality
            return search_instance.search_documents(query)
        
        return nasa_document_search
    
    def get_database_info(self) -> dict:
        """
        Get comprehensive information about the vector database.
        
        Returns:
            Dictionary containing database statistics and metadata:
            - document_count: Number of document chunks in database
            - collection_name: Chroma collection identifier
            - db_path: File system path to database
            - error: Error message if database access fails
            
        This method is useful for:
        - System health monitoring
        - Debugging database issues
        - Capacity planning and usage tracking
        - User feedback about available content
        """
        try:
            # Access the underlying Chroma collection for statistics
            collection = self.vectordb._collection
            return {
                "document_count": collection.count(),
                "collection_name": collection.name,
                "db_path": self.db_path
            }
        except Exception as e:
            # Return error information for debugging
            return {"error": str(e)}


# GLOBAL INSTANCES FOR EFFICIENT RESOURCE USAGE
# Singleton pattern implementation for application-wide NASA search access
_nasa_search = None

def get_nasa_search_tool():
    """
    Get NASA search tool using singleton pattern.
    
    Returns:
        LangChain tool for NASA document search
        
    SINGLETON BENEFITS:
    - Single database connection across application
    - Consistent search behavior throughout system
    - Memory efficient resource usage
    - Faster subsequent tool requests
    
    This function provides a clean interface for getting NASA search
    capability without managing instance lifecycle manually.
    """
    global _nasa_search
    if _nasa_search is None:
        _nasa_search = NASADocumentSearch()
    return _nasa_search.get_tool()

def get_nasa_db_info() -> dict:
    """
    Get NASA database information using singleton pattern.
    
    Returns:
        Dictionary with database statistics and metadata
        
    This function provides access to database information without
    requiring direct instance management. Useful for system monitoring,
    debugging, and user feedback about available content.
    """
    global _nasa_search
    if _nasa_search is None:
        _nasa_search = NASADocumentSearch()
    return _nasa_search.get_database_info() 