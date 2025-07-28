FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

# Install dependencies (torch & torchvision from CPU index)
RUN pip install --no-cache-dir torch==2.2.2 torchvision==0.17.2 \
    --extra-index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir -r requirements.txt

COPY preload_models.py .
RUN python preload_models.py

COPY extractor.py .

ENTRYPOINT ["python", "extractor.py"]
