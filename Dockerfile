FROM python:3.11-slim
WORKDIR /app

# Copy requirements first for better Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

CMD ["bash", "-c", "python fetch_nasa_data.py && python ingest.py && python graph_demo.py"]