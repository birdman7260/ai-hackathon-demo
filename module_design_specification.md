# Module Design Specification (MDS)

## Project: NASA Document Q&A System

---

## 1. Introduction

This document details the design and responsibilities of each module in the NASA Document Q&A System. The system is modular, extensible, and follows a clean 5-layer architecture for maintainability and scalability.

---

## 2. Module Overview

| Module/File                  | Description                                                                 |
|------------------------------|-----------------------------------------------------------------------------|
| `main.py`                    | Application entry point and user interface loop.                            |
| `ingest.py`                  | PDF ingestion and vector database creation.                                 |
| `fetch_nasa_data.py`         | Downloads NASA PDF documents.                                               |
| `debug_embeddings.py`        | Embedding pipeline diagnostics and debugging.                               |
| `test_retrieval.py`          | Retrieval and query testing.                                                |
| `test_langchain_mcp.py`      | Tests LangChain and MCP integration.                                        |
| `mcp_filesystem.py`          | Implements MCP filesystem server for tool integration.                      |
| `common/`                    | Core library modules (see below).                                           |
| `Makefile`                   | Automation for setup, run, debug, Docker, and MCP.                         |
| `Dockerfile`                 | Containerizes the application.                                              |
| `docker-compose.yaml`        | Docker Compose configuration.                                               |
| `requirements.txt`           | Python dependencies.                                                        |
| `setup.sh`, `activate.sh`    | Shell scripts for environment setup and activation.                         |

---

## 3. Core Library Modules (`common/`)

### 3.1 `common/config.py`
- **Purpose:** Centralized environment and application configuration.
- **Responsibilities:**
  - Loads and validates environment variables.
  - Provides default values and type conversion.
  - Exposes configuration via `AppConfig` class.
- **Key Patterns:** Singleton, Factory, Validation.

### 3.2 `common/cadeq_search.py`
- **Purpose:** Implements the `CADEQDocumentSearch` class for vector search and RAG over CA DEQ/CalEPA studies.
- **Key Functions:**
  - `CADEQDocumentSearch`: Handles vector DB connection, semantic search, and LLM-based answer generation.
  - `get_cadeq_search_tool`: Returns a LangChain tool for agent integration.
  - `get_cadeq_db_info`: Returns metadata about the vector database.

### 3.3 `common/mcp_client.py`
- **Purpose:** MCP (Model Context Protocol) integration for external tool access.
- **Responsibilities:**
  - Connects to MCP servers (filesystem, etc.).
  - Adapts async MCP protocol to synchronous tools for LangChain.
  - Provides tool wrappers for agent use.
- **Key Patterns:** Adapter, Singleton, Proxy, Factory.

### 3.4 `common/agent_factory.py`
- **Purpose:** Implements the `AgentFactory` for creating agents with CA DEQ and optional MCP tools.
- **Key Functions:**
  - `AgentFactory`: Handles agent creation, tool integration, and prompt generation.
  - `create_cadeq_agent`: Factory function for main application.

### 3.5 `common/thinking_spinner.py`
- **Purpose:** Terminal UI spinner for user feedback during processing.
- **Responsibilities:**
  - Runs a background thread to animate a spinner.
  - Implements context manager for automatic start/stop.
- **Key Patterns:** Context Manager, Threading.

### 3.6 `common/__init__.py`
- **Purpose:** Exports core functions and classes for easy import.
- **Responsibilities:**
  - Aggregates and exposes key components from submodules.

---

## 4. Application Modules

### 4.1 `main.py`
- **Purpose:** User interface for Q&A over CA DEQ documents.
- **Key Functions:**
  - Loads configuration and agent
  - Handles user input and displays answers

### 4.2 `ingest.py`
- **Purpose:** Ingests all CA DEQ PDFs, splits into chunks, and builds Chroma vector DB.
- **Key Functions:**
  - Loads all PDFs from `data/`
  - Splits documents into chunks
  - Embeds and stores in Chroma DB

### 4.3 `fetch_cadeq_data.py`
- **Purpose:** Downloads 10 CA DEQ/CalEPA studies and reports as PDFs for ingestion.
- **Key Functions:**
  - `download_cadeq_documents`: Downloads and saves all source PDFs to the `data/` directory.

### 4.4 `debug_embeddings.py`
- **Purpose:** Test and debug scripts for embeddings and retrieval, using CA DEQ/environmental queries.
- **Key Functions:**
  - Test embedding pipeline and vector DB
  - Run sample queries for retrieval validation

### 4.5 `test_retrieval.py`
- **Purpose:** Test and debug scripts for embeddings and retrieval, using CA DEQ/environmental queries.
- **Key Functions:**
  - Test embedding pipeline and vector DB
  - Run sample queries for retrieval validation

### 4.6 `test_langchain_mcp.py`
- **Role:** Integration Testing.
- **Responsibilities:**
  - Tests LangChain agent with MCP tool integration.

### 4.7 `mcp_filesystem.py`
- **Role:** MCP Server Implementation.
- **Responsibilities:**
  - Implements a filesystem server for MCP protocol.
  - Enables file operations as agent tools.

---

## 5. Data & Storage

- **`data/`**: Stores source PDF documents (auto-downloaded or user-supplied).
- **`chroma_db/`**: Stores the Chroma vector database for semantic search.

---

## 6. Automation & Deployment

- **`Makefile`**: Provides commands for setup, ingestion, running, debugging, Docker, and MCP.
- **`Dockerfile`**: Builds a container with all dependencies, data, and vector DB.
- **`docker-compose.yaml`**: Orchestrates multi-container setups (if needed).
- **Shell Scripts**: `setup.sh` and `activate.sh` automate environment setup and activation.

---

## 7. Extensibility

- **Add new document types:** Extend `ingest.py` to support new formats.
- **Custom prompts:** Update prompt templates in `common/cadeq_search.py`.
- **New tools/integrations:** Add to `common/mcp_client.py`.
- **Configuration:** Add new settings to `common/config.py`.
- **Testing:** Add new test scripts or extend existing ones.

---

## 8. Interactions & Dependencies

- **LangChain**: Used for agent orchestration and tool integration.
- **OpenAI**: Used for embeddings and LLM-based answer synthesis.
- **Chroma**: Used for vector database and semantic search.
- **MCP**: Optional, for external tool and filesystem access.

---

## 9. Error Handling & Logging

- All modules include error handling and user-friendly messages.
- Debugging and diagnostics are available via Makefile targets and dedicated scripts.

---

## 10. Summary Table

| Layer             | Module(s)                        | Responsibility                                  |
|-------------------|----------------------------------|-------------------------------------------------|
| Presentation      | `main.py`, `common/thinking_spinner.py` | User interaction, feedback, UI                  |
| Agent             | `common/agent_factory.py`        | Agent creation and configuration                 |
| Integration       | `common/mcp_client.py`, `mcp_filesystem.py` | MCP tool integration, external access           |
| Data              | `common/cadeq_search.py`, `ingest.py`, `fetch_cadeq_data.py` | Document ingestion, search, and retrieval       |
| Configuration     | `common/config.py`               | Environment and application configuration        |
| Testing/Debugging | `debug_embeddings.py`, `test_retrieval.py`, `test_langchain_mcp.py` | Diagnostics and validation                      |

---

**For further details, see the in-repo `README.md` and module-level docstrings.** 