FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV PYTHONPATH=/app

CMD ["uvicorn", "halal_compliance_backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
