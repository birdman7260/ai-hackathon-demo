# Module Design Specification (MDS)

## 1. Module: `common/cadeq_search.py`

- **Purpose:** Implements the `CADEQDocumentSearch` class for vector search and RAG over CA DEQ/CalEPA studies.
- **Key Functions:**
  - `CADEQDocumentSearch`: Handles vector DB connection, semantic search, and LLM-based answer generation.
  - `get_cadeq_search_tool`: Returns a LangChain tool for agent integration.
  - `get_cadeq_db_info`: Returns metadata about the vector database.

## 2. Module: `common/agent_factory.py`

- **Purpose:** Implements the `AgentFactory` for creating agents with CA DEQ and optional MCP tools.
- **Key Functions:**
  - `AgentFactory`: Handles agent creation, tool integration, and prompt generation.
  - `create_cadeq_agent`: Factory function for main application.

## 3. Module: `fetch_cadeq_data.py`

- **Purpose:** Downloads 10 CA DEQ/CalEPA studies and reports as PDFs for ingestion.
- **Key Functions:**
  - `download_cadeq_documents`: Downloads and saves all source PDFs to the `data/` directory.

## 4. Module: `ingest.py`

- **Purpose:** Ingests all CA DEQ PDFs, splits into chunks, and builds Chroma vector DB.
- **Key Functions:**
  - Loads all PDFs from `data/`
  - Splits documents into chunks
  - Embeds and stores in Chroma DB

## 5. Module: `main.py`

- **Purpose:** User interface for Q&A over CA DEQ documents.
- **Key Functions:**
  - Loads configuration and agent
  - Handles user input and displays answers

## 6. Module: `debug_embeddings.py` and `test_retrieval.py`

- **Purpose:** Test and debug scripts for embeddings and retrieval, using CA DEQ/environmental queries.
- **Key Functions:**
  - Test embedding pipeline and vector DB
  - Run sample queries for retrieval validation

## 7. Data and Document Flow

- Documents are downloaded via `fetch_cadeq_data.py` and stored in `data/`.
- `ingest.py` processes PDFs, splits, embeds, and builds the Chroma DB.
- `CADEQDocumentSearch` in `common/cadeq_search.py` provides semantic search and LLM-based answers.
- The agent (from `common/agent_factory.py`) orchestrates tool use and response generation.
- `main.py` provides the CLI for user interaction.

--- 