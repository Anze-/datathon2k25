FROM python:3.10-slim
WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

RUN pip install numpy==1.26.4
RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install accelerate

COPY rag .

ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
