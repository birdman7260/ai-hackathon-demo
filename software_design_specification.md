# Software Design Specification (SDS)

## 1. Overview

The CA DEQ Document Q&A System is an intelligent, modular application that enables executive-level question answering over California Department of Environmental Quality (CalEPA) studies and reports. It leverages LangChain, OpenAI LLMs, and Chroma vector database, with optional integration of Model Context Protocol (MCP) for external tool access.

## 2. System Architecture

### 2.1 Layered Architecture

The system follows a clean, 5-layer modular architecture:

1. **Configuration Layer** (`common/config.py`): Loads and validates environment variables and settings.
2. **Data Layer** (`common/cadeq_search.py`): Manages vector database and document retrieval for CA DEQ studies.
3. **Integration Layer** (`common/mcp_client.py`): Handles optional MCP server connections for external tools.
4. **Agent Layer** (`common/agent_factory.py`): Creates and configures AI agents with CA DEQ and optional MCP tools.
5. **Presentation Layer** (`main.py`): Provides user interface and interaction.

### 2.2 Data Flow

- User submits a question via the CLI (`main.py`).
- The agent (from `common/agent_factory.py`) receives the query and determines which tools to use.
- The CA DEQ document search tool (`common/cadeq_search.py`) performs semantic search and retrieval over embedded CA DEQ/CalEPA studies.
- The agent synthesizes an executive-level answer using the retrieved context and the LLM.
- The answer is returned to the user.

## 3. Key Features

- PDF ingestion and vectorization of CA DEQ/CalEPA studies
- Semantic search and retrieval
- Executive summary generation
- Optional filesystem tool integration via MCP
- Modular, clean 5-layer architecture

## 4. External Dependencies

- LangChain
- OpenAI API
- Chroma vector database
- Requests, dotenv, etc.

## 5. Document Sources

The system uses the following CA DEQ/CalEPA studies and reports as its knowledge base:

- 2014 Annual Report on the Air Resources Board's Fine Particulate Matter Monitoring Program
- Indicators of Climate Change in California (2013)
- California Water Action Plan
- 2019 CalEPA Enforcement Report
- Environmental Justice Program Update (2016)
- Improving Public and Worker Safety at Oil Refineries (2014)
- Draft California Communities Environmental Health Screening Tool Report (CalEnviroScreen 2.0)
- 2013 Annual Report on the Air Resources Board's Fine Particulate Matter Monitoring Program
- A Report To The California Legislature on the Potential Health and Environmental Impacts of Leaf Blowers
- Source apportionment of fine and ultrafine particles in California

## 6. Security and Privacy

- All documents are public CA DEQ/CalEPA reports.
- No user data is stored.

## 7. Future Improvements

- Add support for additional CA DEQ/CalEPA document types.
- Enhance prompt engineering for more nuanced executive summaries.
- Integrate with more advanced retrieval and summarization models as they become available.

---

## 8. Key Components

| File/Module                | Responsibility                                                                 |
|----------------------------|-------------------------------------------------------------------------------|
| `main.py`                  | Entry point, user interaction, orchestrates agent and config                  |
| `ingest.py`                | Processes PDF documents, creates vector database                              |
| `fetch_nasa_data.py`       | Downloads NASA PDFs                                                           |
| `common/config.py`         | Loads and validates environment/configuration                                 |
| `common/cadeq_search.py`   | Implements RAG: vector search + LLM synthesis                                |
| `common/mcp_client.py`     | Integrates with MCP servers (filesystem/tools)                                |
| `common/agent_factory.py`  | Factory for creating agents with CA DEQ and optional MCP tools                   |
| `common/thinking_spinner.py`| Terminal spinner for user feedback during processing                         |
| `debug_embeddings.py`      | Embedding pipeline diagnostics                                                |
| `test_retrieval.py`        | Retrieval and query testing                                                   |
| `Makefile`                 | Automation: setup, run, debug, Docker, MCP                                   |
| `Dockerfile`               | Containerizes the application                                                 |
| `chroma_db/`               | Vector database storage                                                       |
| `data/`                    | Source PDF documents                                                          |

---

## 9. Core Workflows

### 9.1 Document Ingestion

- **Input:** NASA PDF documents (auto-downloaded or user-supplied)
- **Process:**  
  - PDFs are split into chunks.
  - Each chunk is embedded using OpenAI embeddings.
  - Embeddings are stored in a Chroma vector database.
- **Output:** Vector DB ready for semantic search.

### 9.2 Question Answering

- **Input:** User query (via terminal)
- **Process:**  
  - Query is embedded and used to search the vector DB for relevant chunks.
  - Retrieved context is passed to an LLM (GPT-4) for synthesis.
  - If MCP is enabled, agent can also use filesystem/tools as needed.
- **Output:** Executive-level answer, shown in terminal.

### 9.3 Optional MCP Integration

- **Purpose:** Allows the agent to perform filesystem operations (read/write/list files) via MCP servers.
- **Design:**  
  - Async MCP protocol is adapted to synchronous tools for LangChain agents.
  - System degrades gracefully if MCP is not configured.

---

## 10. Design Patterns

- **Singleton:** For configuration and client instances.
- **Factory:** For agent and tool creation.
- **Adapter:** Async MCP interface to sync tools.
- **Strategy:** Tool selection based on MCP availability.
- **Template Method:** Standardized agent creation and RAG workflow.
- **Command:** User queries processed through agent invocation.

---

## 11. Extensibility & Modularity

- **Add new document types:** Extend `ingest.py`.
- **Custom prompts:** Update `common/cadeq_search.py`.
- **New tools/integrations:** Add to `common/agent_factory.py` and `common/mcp_client.py`.
- **Configuration:** Centralized in `common/config.py`.
- **Testing:** Modular components allow for unit and integration testing.

---

## 12. Deployment

- **Local:**  
  - Python 3.13+, OpenAI API key required.
  - `make setup`, `make fetch-data`, `make ingest`, `make run`.
- **Docker:**  
  - `make docker-build`, `make docker-interactive`.
  - Container handles data fetching, ingestion, and app startup.

---

## 13. Quality & Testing

- **Type hints** and **docstrings** throughout.
- **Comprehensive error handling** and user feedback.
- **Debugging tools:** `make debug`, `make debug-env`, `make debug-embeddings`, etc.
- **Unit and integration tests:** `test_retrieval.py`, `test-components`.

---

## 14. Example Usage

- **Start Q&A:**  
  - `make run` (with MCP) or `make run-no-mcp` (without MCP)
- **Ask:**  
  - "What are the key risk mitigation strategies in NASA's Systems Engineering Handbook?"
  - "List the mission objectives of Artemis I and the success metrics."

---

## 15. Summary

This system is a robust, modular, and extensible Q&A platform for NASA documents, designed for both executive and technical users. It combines state-of-the-art LLMs, semantic search, and optional tool integration, following best practices in software architecture and design.

---

**For further details, see the in-repo `README.md` and module-level docstrings.** 