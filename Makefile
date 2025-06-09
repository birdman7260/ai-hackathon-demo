.PHONY: setup activate mcp-server run run-no-mcp clean help debug debug-embeddings debug-env debug-vectordb debug-graph debug-ingest test-retrieval test-components debug-verbose clean-vectordb clean-all

# Default target
help:
	@echo "Available targets:"
	@echo "  make setup           - Set up the project (run setup.sh)"
	@echo "  make mcp-server      - Start the MCP filesystem server"
	@echo "  make run             - Run the main application"
	@echo "  make run-no-mcp      - Run without MCP (avoids connection errors)"
	@echo "  make clean           - Clean up temporary files and directories"
	@echo "  make clean-vectordb  - Remove vector database"
	@echo "  make clean-all       - Full cleanup including vector database"
	@echo ""
	@echo "Debug targets:"
	@echo "  make debug           - Run all debugging tests"
	@echo "  make debug-embeddings - Test OpenAI embeddings pipeline"
	@echo "  make debug-env       - Check environment variables and setup"
	@echo "  make debug-vectordb  - Inspect vector database contents"
	@echo "  make debug-graph     - Show graph structure and flow"
	@echo "  make debug-ingest    - Test PDF ingestion process"
	@echo "  make test-retrieval  - Test retrieval with sample queries"
	@echo "  make test-components - Test individual components (LLM, embeddings)"
	@echo "  make debug-verbose   - Run verbose debugging with all tests"

# Setup the project
setup:
	@echo "Setting up the project..."
	chmod +x setup.sh
	./setup.sh

# Start the MCP filesystem server
mcp-server:
	@echo "Starting MCP filesystem server..."
	cd servers/src/filesystem && npm start

# Run the application
run:
	@echo "Running the application..."
	source .venv/bin/activate && python graph_demo.py

# Run the application without MCP to avoid connection errors
run-no-mcp:
	@echo "Running the application without MCP..."
	source .venv/bin/activate && MCP_SERVER_URLS="" python graph_demo.py

# === DEBUG TARGETS ===

# Run comprehensive debugging suite
debug: debug-env debug-embeddings debug-vectordb debug-graph
	@echo "🎉 All debugging tests completed!"

# Test OpenAI embeddings pipeline
debug-embeddings:
	@echo "🧪 Testing embeddings pipeline..."
	source .venv/bin/activate && python debug_embeddings.py

# Check environment variables and setup
debug-env:
	@echo "🔍 Checking environment setup..."
	@echo "Python version:"
	@which python3
	@python3 --version
	@echo ""
	@echo "Virtual environment:"
	@echo "VIRTUAL_ENV: $$VIRTUAL_ENV"
	@echo ""
	@echo "Environment variables:"
	@source .venv/bin/activate && python -c "from dotenv import load_dotenv; import os; load_dotenv(override=True); print(f'OPENAI_API_KEY: {\"✅ Set\" if os.getenv(\"OPENAI_API_KEY\", \"\").startswith(\"sk-\") else \"❌ Missing or invalid\"}'); print(f'MCP_SERVER_URLS: {repr(os.getenv(\"MCP_SERVER_URLS\", \"\"))}')"

# Inspect vector database contents
debug-vectordb:
	@echo "📊 Inspecting vector database..."
	@if [ -d "./chroma_db" ]; then \
		echo "Vector database exists:"; \
		ls -la chroma_db/; \
		echo ""; \
		source .venv/bin/activate && python -c "from langchain_chroma import Chroma; from langchain_openai import OpenAIEmbeddings; from dotenv import load_dotenv; load_dotenv(override=True); vectordb = Chroma(persist_directory='./chroma_db', embedding_function=OpenAIEmbeddings(model='text-embedding-3-small')); collection = vectordb._collection; print(f'📈 Documents: {collection.count()}'); print(f'📝 Collection: {collection.name}')"; \
	else \
		echo "❌ Vector database not found. Run 'make debug-ingest' first."; \
	fi

# Show graph structure and execution flow
debug-graph:
	@echo "🔗 Analyzing graph structure..."
	source .venv/bin/activate && python -c "from graph_demo import chain; print('Graph nodes and edges:'); chain.get_graph().print_ascii()"

# Test PDF ingestion process
debug-ingest:
	@echo "📄 Testing PDF ingestion..."
	@if [ -d "./data" ] && [ $$(ls -1 ./data/*.pdf 2>/dev/null | wc -l) -gt 0 ]; then \
		echo "PDF files found:"; \
		ls -la data/*.pdf; \
		echo ""; \
		echo "Running ingestion..."; \
		source .venv/bin/activate && python ingest.py; \
		echo "✅ Ingestion completed"; \
	else \
		echo "❌ No PDF files found in ./data directory"; \
		echo "Please add PDF files to ./data/ first"; \
	fi

# Test retrieval with sample queries
test-retrieval:
	@echo "🔍 Testing retrieval with sample queries..."
	@if [ -d "./chroma_db" ]; then \
		source .venv/bin/activate && python test_retrieval.py; \
	else \
		echo "❌ Vector database not found. Run 'make debug-ingest' first."; \
	fi

# Test individual components
test-components:
	@echo "🧩 Testing individual components..."
	@echo "1. Testing OpenAI connection..."
	@source .venv/bin/activate && python -c "from langchain_openai import ChatOpenAI; from dotenv import load_dotenv; load_dotenv(override=True); llm = ChatOpenAI(model='gpt-4o-mini'); response = llm.invoke('Hello, respond with just OK'); print(f'✅ LLM Response: {response.content}')"
	@echo ""
	@echo "2. Testing embeddings..."
	@source .venv/bin/activate && python -c "from langchain_openai import OpenAIEmbeddings; from dotenv import load_dotenv; load_dotenv(override=True); embedder = OpenAIEmbeddings(model='text-embedding-3-small'); embedding = embedder.embed_query('test'); print(f'✅ Embedding dimensions: {len(embedding)}')"

# Debug with verbose output
debug-verbose: 
	@echo "🔊 Running verbose debugging..."
	@echo "=== ENVIRONMENT ==="
	@make debug-env
	@echo ""
	@echo "=== VECTOR DATABASE ==="
	@make debug-vectordb
	@echo ""
	@echo "=== COMPONENTS ==="
	@make test-components
	@echo ""
	@echo "=== EMBEDDINGS PIPELINE ==="
	@make debug-embeddings

# Clean up temporary files and directories
clean:
	@echo "Cleaning up..."
	rm -rf __pycache__
	rm -rf .pytest_cache
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete

# Clean vector database (useful for testing re-ingestion)
clean-vectordb:
	@echo "🗑️  Cleaning vector database..."
	rm -rf chroma_db/
	@echo "✅ Vector database removed. Run 'make debug-ingest' to recreate."

# Full clean including vector database
clean-all: clean clean-vectordb
	@echo "🧹 Full cleanup completed" 