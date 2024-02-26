FROM python:3.11-slim-bookworm

WORKDIR /app
COPY requirements.txt .
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    poppler-utils \
    tesseract-ocr \
    tesseract-ocr-eng \
    tesseract-ocr-chi-sim \
    libmagic-dev \    
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt 
RUN pip install -U llama-index --upgrade --no-cache-dir --force-reinstall
RUN pip install llama-parse
COPY src src
CMD ["streamlit", "run", "src/main.py"]