FROM python:3.11-slim
WORKDIR /app

# Copy requirements first for better Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Accept build arguments for API keys and MCP configuration
ARG OPENAI_API_KEY
ARG MCP_SERVER_URLS
ENV OPENAI_API_KEY=${OPENAI_API_KEY}
ENV MCP_SERVER_URLS=${MCP_SERVER_URLS}

# Download NASA documents and create vector database during build
RUN python fetch_nasa_data.py && python ingest.py

# Copy and make startup script executable
COPY start.sh .
RUN chmod +x start.sh

# Use startup script that handles MCP server and main app
CMD ["./start.sh"]