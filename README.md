# NASA Document Q&A System

> **An intelligent question-answering system powered by LangChain and OpenAI that provides executive-level insights from NASA technical documents.**

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://python.org)
[![LangChain](https://img.shields.io/badge/LangChain-0.3-green.svg)](https://langchain.com)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-orange.svg)](https://openai.com)
[![Chroma](https://img.shields.io/badge/Chroma-Vector%20DB-purple.svg)](https://trychroma.com)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://docker.com)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [Quick Start](#quick-start)
  - [Example Prompts](#example-prompts)
  - [Advanced Usage](#advanced-usage)
- [Docker Deployment](#-docker-deployment)
- [Architecture](#architecture)
- [Debugging & Troubleshooting](#debugging--troubleshooting)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

This system transforms NASA's technical documentation into an interactive Q&A interface designed for executives and technical leaders. Built with LangChain's React agent pattern and OpenAI's GPT-4.1, it provides accurate, contextual answers by intelligently retrieving relevant information from processed NASA documents. The system features optional MCP (Model Context Protocol) integration for enhanced filesystem capabilities and follows a clean 5-layer modular architecture.

### What Problems Does This Solve?

- **Information Overload**: NASA documents are extensive and complex - this system extracts key insights quickly
- **Executive Decision Making**: Provides executive-level summaries and analysis from technical documents
- **Compliance Tracking**: Enables quick retrieval of governance and compliance information
- **Knowledge Discovery**: Uncovers connections between different NASA documents and initiatives

### Why This Technology Stack?

- **LangChain**: Provides robust document processing, retrieval pipelines, and React agent framework
- **OpenAI GPT-4.1**: Delivers high-quality, cost-effective text generation and embeddings
- **Chroma Vector Database**: Enables semantic search across document chunks
- **MCP (Model Context Protocol)**: Optional integration for filesystem and external tool access
- **React Agent Pattern**: Intelligent reasoning and tool selection for complex queries

## ✨ Features

- **📄 PDF Document Processing**: Automatically ingests and processes NASA PDFs
- **🔍 Semantic Search**: Vector-based similarity search for relevant content
- **🎯 Executive Summaries**: Tailored responses for executive audiences
- **⚡ Fast Retrieval**: Sub-second query processing with 361 indexed documents
- **🛠️ Comprehensive Debugging**: Built-in tools for system health monitoring
- **🔧 Modular Architecture**: Clean 5-layer architecture with single responsibility components
- **🔌 MCP Integration**: Optional Model Context Protocol support for filesystem operations
- **🤖 React Agent Pattern**: Intelligent tool selection and reasoning capabilities
- **🐳 Docker Ready**: Containerized deployment with interactive support
- **📊 Analytics Ready**: Built-in metrics and performance monitoring
- **⚙️ Environment-Driven**: Configuration management with validation and graceful degradation

## 🔧 Prerequisites

### System Requirements

- **Python**: 3.13+ (tested with 3.13.1)
- **OpenAI API Key**: Required for embeddings and text generation
- **Memory**: 4GB+ RAM recommended for vector operations
- **Storage**: 500MB+ for vector database and documents

### Supported Platforms

- macOS (ARM64/Intel)
- Linux (x86_64/ARM64)
- Windows (WSL recommended)

## 🚀 Installation

You can run the NASA Q&A system either locally with Python or using Docker. Choose the method that best fits your environment:

- **🐍 Local Python Setup**: Full development capabilities with debugging tools
- **🐳 Docker Setup**: Isolated environment, consistent deployment (see [Docker Deployment](#-docker-deployment))

> **💡 Pro Tip**: Get your OpenAI API key from [platform.openai.com/account/api-keys](https://platform.openai.com/account/api-keys)

### Quick Setup (Recommended)

```bash
# 1. Clone and navigate to the project
git clone https://github.com/driches/ai-hackathon-demo
cd hackathon-demo

# 2. Edit your API key in the .env file
# Replace 'your_openai_api_key_here' with your actual OpenAI API key
cp .env.example .env
nano .env  # or use your preferred editor

# 3. Build Docker Container
make docker-build

# 4. Start Chat
make docker-interactive


```
### Local Setup
```bash 
# 1. Run the automated setup script
make setup

# 2. Edit your API key in the .env file
# Replace 'your_openai_api_key_here' with your actual OpenAI API key
cp .env.example .env
nano .env  # or use your preferred editor
```

### Activation for Development

```bash
# Activate the environment for future sessions
source ./activate.sh

# Or use the standard activation
source .venv/bin/activate
```

### 2. Verify Setup

```bash

# Test your configuration
make debug-env

# Expected output:
# ✅ OPENAI_API_KEY: Set
# ✅ Python 3.13.1 detected
# ✅ Virtual environment active
```


## 🎮 Usage

### Quick Start

#### 1. Complete Setup

```bash

# Activate environment, download data, and ingest documents
source ./activate.sh
make fetch-data
make ingest

# Verify the vector database
make debug-vectordb

# Start an MCP server
make mcp-http 

```

#### 2. Start Asking Questions

```bash
# To run with MCP tools (if configured in .env)
make run

# To run without MCP tools
make run-no-mcp

# You'll see the prompt:
# Ask ▶ 
```

#### 3. Try Your First Query

```text
Ask ▶ What are the key risk mitigation strategies in NASA's Systems Engineering Handbook?

→ The NASA Systems Engineering Handbook outlines several key risk mitigation strategies:

1. **Risk-Informed Decision Making (RIDM)**: A systematic approach that combines...
2. **Continuous Risk Management (CRM)**: Ongoing identification and assessment...
3. **Technical Risk Assessment**: Dual approach combining quantitative and qualitative...

[Detailed response continues...]
```

#### 4. Exit the Application

```bash
Ask ▶ quit
# or press Ctrl+C
```

### Example Prompts

Here are proven prompts that demonstrate the system's capabilities:

| Prompt | Expected Angle | Use Case |
|--------|----------------|----------|
| "Summarize the key technical risk mitigation steps recommended by NASA's Systems Engineering Handbook." | Compliance / governance traceability | Risk management compliance, audit preparation |
| "List the mission objectives of Artemis I and the success metrics." | KPI extraction from press kit | Executive briefings, mission status reports |
| "What are the primary systems engineering processes NASA recommends for large-scale projects?" | Process standardization | Project planning, methodology alignment |
| "Describe the safety requirements and protocols mentioned in the NASA documentation." | Safety compliance | Safety audits, regulatory compliance |
| "What testing and validation procedures does NASA require for mission-critical systems?" | Quality assurance | QA process development, validation planning |
| "Summarize the budget allocations and cost considerations for Artemis I." | Financial oversight | Budget reviews, cost analysis |
| "What are the key stakeholder communication requirements in NASA projects?" | Stakeholder management | Communication planning, governance |
| "List the environmental and sustainability considerations in NASA missions." | Environmental compliance | ESG reporting, environmental impact |

### Advanced Usage

#### Custom Document Processing

To add your own PDF documents:

```bash
# 1. Add PDFs to the data directory
cp your-document.pdf ./data/

# 2. Re-ingest documents
make clean-vectordb
make ingest

# 3. Verify new documents
make debug-vectordb
```

#### Batch Query Processing

```bash
# Test multiple queries
make test-retrieval

# Custom retrieval testing
python test_retrieval.py
```

#### Performance Monitoring

```bash
# Comprehensive system check
make debug

# Individual component testing
make test-components
make debug-embeddings
```

### MCP (Model Context Protocol) Integration

The system supports optional MCP integration for enhanced filesystem operations alongside NASA document search.

#### What is MCP?

MCP (Model Context Protocol) is a protocol that allows AI agents to interact with external tools and services. In our system, it provides filesystem access capabilities that complement the NASA document search.

#### MCP Features

- **Filesystem Operations**: Read, write, list files and directories
- **Distributed Architecture**: MCP servers run separately from the main application
- **Graceful Degradation**: System works with or without MCP servers
- **Async/Sync Bridge**: Seamless integration between MCP's async protocol and LangChain's sync tools

#### Running with MCP

```bash

# 1. Configure MCP in your .env file
# This is usually done once
echo "MCP_SERVER_URLS=http://127.0.0.1:8000/mcp/" >> .env

# 2. Start an MCP server
make mcp-http 

# 3. Run the application with MCP support
make run

# The agent will now have both NASA search AND filesystem tools
```

#### Running without MCP

```bash
# Run with NASA documents only (no filesystem tools)
make run-no-mcp

# Or leave MCP_SERVER_URLS empty in .env file
```

#### MCP Architecture

```
User Query → React Agent → Tool Selection
                 │
       ┌─────────┼─────────┐
       │         │         │
  NASA Search   MCP    File System
  (Vector DB)  Bridge   Operations
       │         │         │
  Executive    HTTP     Read/Write
  Response    Request    Files
```

## 🐳 Docker Deployment

Docker provides an isolated, reproducible environment for running the NASA Q&A system. The containerized version automatically handles data fetching, document ingestion, and application startup.

### Prerequisites for Docker

- **Docker Desktop**: Latest version recommended
- **OpenAI API Key**: Required and configured in `.env` file
- **Memory**: 4GB+ RAM for Docker container operations

### Quick Docker Start

#### 1. Build the Docker Image

```bash
# Build the Docker image with all dependencies
make docker-build

# Or use direct Docker command:
# docker build -t nasa-qa-demo .
```

#### 2. Run Interactively (Recommended)

```bash
# Start interactive Q&A session in Docker
make docker-interactive

# This will:
# ✅ Download NASA documents automatically
# ✅ Process them into vector database
# ✅ Start the interactive Q&A interface
# ✅ Show the thinking animation
# ✅ Allow you to ask questions and get responses
```

You'll see output like:
```text
🐳 Starting interactive NASA Q&A system in Docker...
💡 You can now ask questions about NASA documents!
💡 Type 'quit', 'exit', or 'q' to stop, or press Ctrl+C

↓ nasa_se_handbook.pdf
↓ artemis_i_press_kit.pdf
↓ clps_press_kit.pdf
NASA docs ready → ./data
🚀 NASA Document Q&A System
Ask questions about NASA documents. Type 'quit', 'exit', or 'q' to stop.
============================================================
Ask ▶ 
```

#### 3. Test Your Docker Setup

```bash
# Run non-interactive mode for testing
make docker-run

# This validates the complete pipeline without user interaction
```

### Docker Commands Reference

| Command | Purpose | Use Case |
|---------|---------|----------|
| `make docker-build` | Build Docker image | Initial setup, after code changes |
| `make docker-interactive` | Interactive Q&A session | Normal usage, demonstrations |
| `make docker-run` | Non-interactive pipeline test | CI/CD, automated testing |

### Direct Docker Commands

If you prefer using Docker directly:

```bash
# Build image
docker build -t nasa-qa-demo .

# Run interactively (recommended for Q&A)
docker run -it --rm --env-file .env nasa-qa-demo

# Run non-interactively (for testing)
docker run --rm --env-file .env nasa-qa-demo
```

### Docker vs Local Development

| Aspect | Docker | Local Development |
|--------|--------|-------------------|
| **Setup** | One command after build | Multi-step setup process |
| **Dependencies** | Isolated container | Requires Python 3.13+ |
| **Performance** | ~10% overhead | Native performance |
| **Debugging** | Limited access | Full debugging tools |
| **Updates** | Rebuild required | Instant code changes |

### Docker Troubleshooting

#### Common Docker Issues

**1. Container Exits Immediately**
```bash
# Check Docker logs
docker logs <container-id>

# Verify .env file exists and has OPENAI_API_KEY
ls -la .env
```

**2. Interactive Mode Not Working**
```bash
# Use our recommended command
make docker-interactive

# NOT: docker-compose up (has interactive input limitations)
```

**3. API Key Issues in Docker**
```bash
# Verify .env file format
cat .env

# Should contain:
# OPENAI_API_KEY=sk-your-actual-key-here
```

**4. Out of Memory Errors**
```bash
# Increase Docker memory limit in Docker Desktop
# Recommended: 4GB+ for smooth operation
```

### When to Use Docker

**✅ Use Docker when:**
- Deploying to production servers
- Ensuring consistent environments across teams
- Running in CI/CD pipelines
- Avoiding local Python environment conflicts
- Demonstrating to stakeholders

**🔧 Use Local Development when:**
- Actively developing and debugging code
- Need access to debugging tools (`make debug`)
- Frequent code changes and testing
- Full performance optimization required

## 🏗️ Architecture

### System Flow

```
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
```

### 5-Layer Clean Architecture

The system follows a modular, clean architecture pattern with distinct layers:

1. **Configuration Layer** (`common/config.py`): Environment setup and validation
2. **Data Layer** (`common/nasa_search.py`): Vector database and document retrieval  
3. **Integration Layer** (`common/mcp_client.py`): External MCP server connections
4. **Agent Layer** (`common/agent_factory.py`): AI agent creation and configuration
5. **Presentation Layer** (`main.py`): User interface and interaction

### Key Components

- **`main.py`**: Main application using modular components
- **`common/config.py`**: Environment and configuration management with validation
- **`common/nasa_search.py`**: RAG implementation for NASA document search
- **`common/mcp_client.py`**: MCP (Model Context Protocol) integration with async/sync bridge
- **`common/agent_factory.py`**: Factory for creating configured AI agents
- **`common/thinking_spinner.py`**: UI components with threading support
- **`ingest.py`**: PDF processing and vector database creation
- **`debug_embeddings.py`**: Comprehensive embedding pipeline testing
- **`test_retrieval.py`**: Query testing and validation
- **`chroma_db/`**: Vector database storage
- **`data/`**: Source PDF documents

### Agent Architecture (React Pattern)

```
┌─────────────┐
│ User Query  │
└─────┬───────┘
      │
┌─────▼───────┐
│ React Agent │ ◀── LangChain create_react_agent
└─────┬───────┘
      │
┌─────▼───────┐    ┌─────────────┐    ┌─────────────┐
│    Tools    │◀──▶│ NASA Search │ +  │ MCP Tools   │
└─────┬───────┘    └─────────────┘    └─────────────┘
      │                    │                  │
┌─────▼───────┐    ┌─────▼─────┐    ┌─────▼─────┐
│  Response   │    │Vector DB  │    │File System│
└─────────────┘    └───────────┘    └───────────┘
```

### Design Patterns Used

- **Singleton Pattern**: Configuration and client instances
- **Factory Pattern**: Agent creation with different tool configurations  
- **Adapter Pattern**: Async/sync bridge for MCP integration
- **Strategy Pattern**: Different tool sets based on MCP server availability
- **Template Method**: Standardized agent creation workflow
- **Command Pattern**: User queries processed through agent invocation

## 🔍 Debugging & Troubleshooting

### Built-in Debugging Tools

The system includes comprehensive debugging commands accessible via `make`:

```bash
# Complete system health check
make debug

# Individual component testing
make debug-env          # Environment and configuration
make debug-embeddings   # OpenAI embeddings pipeline
make debug-vectordb     # Vector database inspection
make debug-graph        # LangGraph workflow visualization
make test-components    # LLM and embedding connectivity
make test-retrieval     # Query processing validation
```

### Common Issues and Solutions

#### 1. OpenAI API Key Issues

**Problem**: `AuthenticationError: Error code: 401`

**Solutions**:
```bash
# Check API key format
make debug-env

# Verify key starts with 'sk-'
echo $OPENAI_API_KEY

# Force reload environment
unset OPENAI_API_KEY
source .venv/bin/activate
```

#### 2. Empty Vector Database

**Problem**: No documents retrieved for queries

**Solutions**:
```bash
# Check database status
make debug-vectordb

# Re-ingest documents if needed
make clean-vectordb
make ingest
```

#### 3. Slow Query Performance

**Problem**: Queries taking >10 seconds

**Solutions**:
```bash
# Test embedding performance
make debug-embeddings

# Check system resources
htop  # or Activity Monitor on macOS
```

#### 4. Import/Module Errors

**Problem**: `ModuleNotFoundError` or `ImportError`

**Solutions**:
```bash
# Quick fix: Re-run setup
./setup.sh

# Or verify virtual environment manually
make debug-env

# Reinstall dependencies if needed
pip install -r requirements.txt

# Check Python version compatibility
python --version  # Should be 3.13+
```

#### 5. Environment Issues

**Problem**: Virtual environment or activation problems

**Solutions**:
```bash
# Use the activation script
source ./activate.sh

# Or re-run complete setup
./setup.sh

# Verify environment status
make debug-env
```

### Performance Benchmarks

- **Query Response Time**: <5 seconds typical
- **Document Ingestion**: ~2 minutes for 3 large PDFs
- **Vector Search**: <1 second for 361 documents
- **Memory Usage**: ~500MB during operation

### Debug Command Reference

| Command | Purpose | Typical Use Case |
|---------|---------|------------------|
| `make debug` | Full system check | Daily health monitoring |
| `make debug-env` | Environment verification | Setup validation |
| `make debug-embeddings` | Embedding pipeline test | API connectivity issues |
| `make debug-vectordb` | Database inspection | Query result problems |
| `make test-retrieval` | Query testing | Performance validation |
| `make debug-verbose` | Detailed diagnostics | Complex troubleshooting |

## 🛠️ Development

### Project Structure

```
.
├── main.py                # Main application
├── ingest.py              # Document processing
├── fetch_nasa_data.py     # NASA document downloader  
├── debug_embeddings.py    # Embedding diagnostics
├── test_retrieval.py      # Query testing
├── requirements.txt       # Python dependencies
├── Makefile              # Automation commands (includes Docker targets)
├── Dockerfile            # Docker container configuration
├── docker-compose.yaml   # Docker Compose configuration
├── .env                  # Configuration (create from .env.example)
├── common/               # Modular architecture components
│   ├── __init__.py       # Package exports (38 lines)
│   ├── README.md         # Architecture documentation
│   ├── config.py         # Environment & configuration (88 lines)
│   ├── nasa_search.py    # RAG implementation (87 lines)
│   ├── mcp_client.py     # MCP integration (138 lines)
│   ├── agent_factory.py  # Agent creation (79 lines)
│   └── thinking_spinner.py # UI components (67 lines)
├── data/                 # Source PDF documents (auto-downloaded)
│   ├── nasa_se_handbook.pdf
│   ├── artemis_i_press_kit.pdf
│   └── clps_press_kit.pdf
├── chroma_db/            # Vector database
└── .venv/                # Python virtual environment
```

### Adding New Features

1. **New Document Types**: Modify `ingest.py` to support additional formats
2. **Custom Prompts**: Update `common/nasa_search.py` prompt templates
3. **Additional Tools**: Add new tools to `common/agent_factory.py` tool list
4. **New Integrations**: Extend `common/mcp_client.py` for additional MCP servers
5. **Configuration**: Add new settings to `common/config.py` environment management
6. **Monitoring**: Add metrics collection to existing debug tools

### Modular Architecture Benefits

- **Single Responsibility**: Each module has one clear purpose
- **Testability**: Components can be unit tested independently  
- **Reusability**: Common modules can be used in other projects
- **Maintainability**: Changes are isolated to specific components
- **Scalability**: Easy to add new features without modifying existing code

### Testing

```bash
# Unit testing
make test-components

# Integration testing
make debug

# Performance testing
make debug-embeddings

# End-to-end testing
make test-retrieval
```

### Code Quality

- **Type Hints**: All functions include type annotations
- **Error Handling**: Comprehensive exception handling with user-friendly messages
- **Logging**: Built-in debug output for troubleshooting
- **Documentation**: Inline comments and docstrings

## 🤝 Contributing

### Getting Started

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-capability`
3. Make your changes
4. Test thoroughly: `make debug`
5. Submit a pull request

### Development Guidelines

- Add type hints to all functions
- Include comprehensive error handling
- Update documentation for new features
- Test all changes with `make debug`

### Reporting Issues

When reporting issues, please include:

1. **System Information**: Output of `make debug-env`
2. **Error Messages**: Full traceback if available
3. **Reproduction Steps**: Minimal example to reproduce
4. **Expected vs Actual**: What you expected vs what happened

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **NASA**: For providing comprehensive technical documentation
- **LangChain**: For the robust document processing framework
- **OpenAI**: For powerful embedding and generation capabilities
- **Chroma**: For efficient vector database operations


