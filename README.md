# NASA Document Q&A System

> **An intelligent question-answering system powered by LangChain and OpenAI that provides executive-level insights from NASA technical documents.**

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://python.org)
[![LangChain](https://img.shields.io/badge/LangChain-0.3-green.svg)](https://langchain.com)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-orange.svg)](https://openai.com)
[![Chroma](https://img.shields.io/badge/Chroma-Vector%20DB-purple.svg)](https://trychroma.com)

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
- [Architecture](#architecture)
- [Debugging & Troubleshooting](#debugging--troubleshooting)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

This system transforms NASA's technical documentation into an interactive Q&A interface designed for executives and technical leaders. Built with LangChain and OpenAI's GPT-4o-mini, it provides accurate, contextual answers by intelligently retrieving relevant information from processed NASA documents.

### What Problems Does This Solve?

- **Information Overload**: NASA documents are extensive and complex - this system extracts key insights quickly
- **Executive Decision Making**: Provides executive-level summaries and analysis from technical documents
- **Compliance Tracking**: Enables quick retrieval of governance and compliance information
- **Knowledge Discovery**: Uncovers connections between different NASA documents and initiatives

### Why This Technology Stack?

- **LangChain**: Provides robust document processing and retrieval pipelines
- **OpenAI GPT-4o-mini**: Delivers high-quality, cost-effective text generation
- **Chroma Vector Database**: Enables semantic search across document chunks
- **LangGraph**: Orchestrates complex workflows with retrieval and generation steps

## ✨ Features

- **📄 PDF Document Processing**: Automatically ingests and processes NASA PDFs
- **🔍 Semantic Search**: Vector-based similarity search for relevant content
- **🎯 Executive Summaries**: Tailored responses for executive audiences
- **⚡ Fast Retrieval**: Sub-second query processing with 361 indexed documents
- **🛠️ Comprehensive Debugging**: Built-in tools for system health monitoring
- **🔧 Flexible Architecture**: Modular design with optional MCP integration
- **📊 Analytics Ready**: Built-in metrics and performance monitoring

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

### Quick Setup (Recommended)

```bash
# 1. Clone and navigate to the project
git clone <your-repository-url>
cd hackathon-demo

# 2. Run the automated setup script
./setup.sh

# 3. Edit your API key in the .env file
# Replace 'your_openai_api_key_here' with your actual OpenAI API key
nano .env  # or use your preferred editor
```

### Activation for Development

```bash
# Activate the environment for future sessions
source ./activate.sh

# Or use the standard activation
source .venv/bin/activate
```

### Manual Setup (Alternative)

If you prefer manual setup or encounter issues:

```bash
# Create virtual environment
python3 -m venv .venv

# Activate environment
source .venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Create .env file from example
cp .env.example .env
# Then edit .env with your OpenAI API key
```

## ⚙️ Configuration

### 1. Set Your OpenAI API Key

After running `./setup.sh`, edit the `.env` file:

```bash
# Edit the .env file created by setup
nano .env  # or code .env, vim .env, etc.

# Update this line with your actual API key:
OPENAI_API_KEY=sk-your-actual-openai-api-key-here

# Optional: Leave MCP_SERVER_URLS empty to disable MCP
MCP_SERVER_URLS=
```

> **💡 Pro Tip**: Get your OpenAI API key from [platform.openai.com/account/api-keys](https://platform.openai.com/account/api-keys)

### 2. Verify Setup

```bash
# Activate environment (if not already active)
source ./activate.sh

# Test your configuration
make debug-env

# Expected output:
# ✅ OPENAI_API_KEY: Set
# ✅ Python 3.13.1 detected
# ✅ Virtual environment active
```

### 3. Ingest NASA Documents

```bash
# Process the included NASA PDFs
make ingest

# Verify the vector database
make debug-vectordb

# Expected output:
# 📈 Documents: 361
# 📝 Collection: langchain
```

## 🎮 Usage

### Quick Start

#### 1. Complete Setup

```bash
# Run the setup script and configure your API key
./setup.sh
nano .env  # Add your OpenAI API key

# Activate environment and ingest documents
source ./activate.sh
make ingest
```

#### 2. Start Asking Questions

```bash
# Launch the Q&A system
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

## 🏗️ Architecture

### System Flow

```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐
│  PDF Docs   │───▶│   Ingestion  │───▶│  Vector DB  │
└─────────────┘    └──────────────┘    └─────────────┘
                                              │
┌─────────────┐    ┌──────────────┐    ┌─────▼─────┐
│   Response  │◀───│  Generation  │◀───│ Retrieval │
└─────────────┘    └──────────────┘    └───────────┘
                           ▲
                    ┌──────▼──────┐
                    │ User Query  │
                    └─────────────┘
```

### Key Components

- **`graph_demo.py`**: Main application with LangGraph workflow
- **`ingest.py`**: PDF processing and vector database creation
- **`debug_embeddings.py`**: Comprehensive embedding pipeline testing
- **`test_retrieval.py`**: Query testing and validation
- **`chroma_db/`**: Vector database storage
- **`data/`**: Source PDF documents

### LangGraph Workflow

```
┌───────────┐
│ __start__ │
└─────┬─────┘
      │
┌─────▼─────┐
│ retrieve  │  ◀── Semantic search in vector DB
└─────┬─────┘
      │
┌─────▼─────┐
│ generate  │  ◀── LLM generates executive response
└─────┬─────┘
      │
┌─────▼─────┐
│ __end__   │
└───────────┘
```

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
├── graph_demo.py           # Main application
├── ingest.py              # Document processing
├── debug_embeddings.py    # Embedding diagnostics
├── test_retrieval.py      # Query testing
├── requirements.txt       # Python dependencies
├── Makefile              # Automation commands
├── .env                  # Configuration (create from .env.example)
├── data/                 # Source PDF documents
│   ├── nasa_se_handbook.pdf
│   ├── artemis_i_press_kit.pdf
│   └── clps_press_kit.pdf
├── chroma_db/            # Vector database
└── .venv/                # Python virtual environment
```

### Adding New Features

1. **New Document Types**: Modify `ingest.py` to support additional formats
2. **Custom Prompts**: Update `graph_demo.py` generation templates
3. **Additional Tools**: Extend LangGraph workflow with new nodes
4. **Monitoring**: Add metrics collection to existing debug tools

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

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/your-repo/issues)
- **Documentation**: This README and inline code comments

---

