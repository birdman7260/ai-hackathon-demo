# Software Design Specification

## 1. Overview

**Project Name:** NASA Document Q&A System  
**Purpose:**  
An intelligent question-answering system that provides executive-level insights from NASA technical documents. It leverages LangChain, OpenAI GPT-4, and a Chroma vector database to enable semantic search and retrieval-augmented generation (RAG) over NASA PDFs. Optional integration with the Model Context Protocol (MCP) allows for advanced filesystem and tool operations.

---

## 2. System Architecture

### 2.1 High-Level Flow

┌─────────────┐    ┌──────────────┐    ┌─────────────┐
│  PDF Docs   │───▶│   Ingestion  │───▶│  Vector DB  │
└─────────────┘    └──────────────┘    └─────────────┘
                                              │
┌─────────────┐    ┌──────────────┐    ┌─────▼─────┐
│   Response  │◀───│  AI Agent    │◀───│ Retrieval │
└─────────────┘    └──────────────┘    └───────────┘
                           ▲                  ▲
                    ┌──────▼──────┐    ┌──────▼──────┐
                    │ User Query  │    │ MCP Tools   │
                    └─────────────┘    └─────────────┘ 

### 2.2 Layered Architecture

The system follows a **5-layer clean architecture**:

1. **Configuration Layer** (`common/config.py`): Loads and validates environment variables, manages configuration.
2. **Data Layer** (`common/nasa_search.py`): Handles vector database, document ingestion, and semantic search.
3. **Integration Layer** (`common/mcp_client.py`): Manages optional MCP server connections for external tool access.
4. **Agent Layer** (`common/agent_factory.py`): Creates and configures AI agents with appropriate tools.
5. **Presentation Layer** (`main.py`): User interface and interaction loop.

---

## 3. Key Components

| File/Module                | Responsibility                                                                 |
|----------------------------|-------------------------------------------------------------------------------|
| `main.py`                  | Entry point, user interaction, orchestrates agent and config                  |
| `ingest.py`                | Processes PDF documents, creates vector database                              |
| `fetch_nasa_data.py`       | Downloads NASA PDFs                                                           |
| `common/config.py`         | Loads and validates environment/configuration                                 |
| `common/nasa_search.py`    | Implements RAG: vector search + LLM synthesis                                |
| `common/mcp_client.py`     | Integrates with MCP servers (filesystem/tools)                                |
| `common/agent_factory.py`  | Factory for creating agents with NASA/MCP tools                               |
| `common/thinking_spinner.py`| Terminal spinner for user feedback during processing                         |
| `debug_embeddings.py`      | Embedding pipeline diagnostics                                                |
| `test_retrieval.py`        | Retrieval and query testing                                                   |
| `Makefile`                 | Automation: setup, run, debug, Docker, MCP                                   |
| `Dockerfile`               | Containerizes the application                                                 |
| `chroma_db/`               | Vector database storage                                                       |
| `data/`                    | Source PDF documents                                                          |

---

## 4. Core Workflows

### 4.1 Document Ingestion

- **Input:** NASA PDF documents (auto-downloaded or user-supplied)
- **Process:**  
  - PDFs are split into chunks.
  - Each chunk is embedded using OpenAI embeddings.
  - Embeddings are stored in a Chroma vector database.
- **Output:** Vector DB ready for semantic search.

### 4.2 Question Answering

- **Input:** User query (via terminal)
- **Process:**  
  - Query is embedded and used to search the vector DB for relevant chunks.
  - Retrieved context is passed to an LLM (GPT-4) for synthesis.
  - If MCP is enabled, agent can also use filesystem/tools as needed.
- **Output:** Executive-level answer, shown in terminal.

### 4.3 Optional MCP Integration

- **Purpose:** Allows the agent to perform filesystem operations (read/write/list files) via MCP servers.
- **Design:**  
  - Async MCP protocol is adapted to synchronous tools for LangChain agents.
  - System degrades gracefully if MCP is not configured.

---

## 5. Design Patterns

- **Singleton:** For configuration and client instances.
- **Factory:** For agent and tool creation.
- **Adapter:** Async MCP interface to sync tools.
- **Strategy:** Tool selection based on MCP availability.
- **Template Method:** Standardized agent creation and RAG workflow.
- **Command:** User queries processed through agent invocation.

---

## 6. Extensibility & Modularity

- **Add new document types:** Extend `ingest.py`.
- **Custom prompts:** Update `common/nasa_search.py`.
- **New tools/integrations:** Add to `common/agent_factory.py` and `common/mcp_client.py`.
- **Configuration:** Centralized in `common/config.py`.
- **Testing:** Modular components allow for unit and integration testing.

---

## 7. Deployment

- **Local:**  
  - Python 3.13+, OpenAI API key required.
  - `make setup`, `make fetch-data`, `make ingest`, `make run`.
- **Docker:**  
  - `make docker-build`, `make docker-interactive`.
  - Container handles data fetching, ingestion, and app startup.

---

## 8. Quality & Testing

- **Type hints** and **docstrings** throughout.
- **Comprehensive error handling** and user feedback.
- **Debugging tools:** `make debug`, `make debug-env`, `make debug-embeddings`, etc.
- **Unit and integration tests:** `test_retrieval.py`, `test-components`.

---

## 9. Example Usage

- **Start Q&A:**  
  - `make run` (with MCP) or `make run-no-mcp` (without MCP)
- **Ask:**  
  - "What are the key risk mitigation strategies in NASA's Systems Engineering Handbook?"
  - "List the mission objectives of Artemis I and the success metrics."

---

## 10. Summary

This system is a robust, modular, and extensible Q&A platform for NASA documents, designed for both executive and technical users. It combines state-of-the-art LLMs, semantic search, and optional tool integration, following best practices in software architecture and design.

---

**For further details, see the in-repo `README.md` and module-level docstrings.** 