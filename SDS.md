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