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