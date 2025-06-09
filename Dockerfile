FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
CMD ["bash", "-c", "python fetch_nasa_data.py && python ingest.py && python graph_demo.py"]