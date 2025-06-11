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

### 3.2 `common/nasa_search.py`
- **Purpose:** NASA document search and RAG (Retrieval-Augmented Generation).
- **Responsibilities:**
  - Loads and manages the Chroma vector database.
  - Embeds and retrieves document chunks.
  - Synthesizes answers using LLMs.
- **Key Patterns:** Singleton, Factory, Template Method, Lazy Loading.

### 3.3 `common/mcp_client.py`
- **Purpose:** MCP (Model Context Protocol) integration for external tool access.
- **Responsibilities:**
  - Connects to MCP servers (filesystem, etc.).
  - Adapts async MCP protocol to synchronous tools for LangChain.
  - Provides tool wrappers for agent use.
- **Key Patterns:** Adapter, Singleton, Proxy, Factory.

### 3.4 `common/agent_factory.py`
- **Purpose:** Factory for creating and configuring AI agents.
- **Responsibilities:**
  - Assembles agents with NASA search and optional MCP tools.
  - Configures model, temperature, and system prompts.
  - Handles tool integration and error isolation.
- **Key Patterns:** Factory, Builder, Strategy, Template Method.

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
- **Role:** Presentation Layer.
- **Responsibilities:**
  - Loads configuration.
  - Creates the agent.
  - Runs the interactive Q&A loop.
  - Handles user input and output.
  - Provides error handling and user feedback.

### 4.2 `ingest.py`
- **Role:** Data Layer.
- **Responsibilities:**
  - Loads PDF files from the `data/` directory.
  - Splits documents into chunks.
  - Embeds chunks and stores them in the Chroma vector DB.

### 4.3 `fetch_nasa_data.py`
- **Role:** Data Acquisition.
- **Responsibilities:**
  - Downloads official NASA PDFs into the `data/` directory.

### 4.4 `debug_embeddings.py`
- **Role:** Diagnostics.
- **Responsibilities:**
  - Tests the embedding pipeline.
  - Verifies OpenAI API connectivity and embedding quality.

### 4.5 `test_retrieval.py`
- **Role:** Testing.
- **Responsibilities:**
  - Runs sample queries against the vector DB.
  - Validates retrieval and answer quality.

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
- **Custom prompts:** Update prompt templates in `common/nasa_search.py`.
- **New tools/integrations:** Add to `common/agent_factory.py` and `common/mcp_client.py`.
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
| Data              | `common/nasa_search.py`, `ingest.py`, `fetch_nasa_data.py` | Document ingestion, search, and retrieval       |
| Configuration     | `common/config.py`               | Environment and application configuration        |
| Testing/Debugging | `debug_embeddings.py`, `test_retrieval.py`, `test_langchain_mcp.py` | Diagnostics and validation                      |

---

**For further details, see the in-repo `README.md` and module-level docstrings.** 