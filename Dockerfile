# Use Python 3.12 slim image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    python3-numpy \
    python3-matplotlib \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app .

# Create results directory with proper permissions
RUN mkdir -p results/visualizations/slaughterhouse/2d && \
    mkdir -p results/visualizations/slaughterhouse/3d && \
    mkdir -p results/visualizations/food_processing/2d && \
    mkdir -p results/visualizations/food_processing/3d && \
    chmod -R 777 results

# Create a volume for persistent storage
VOLUME ["/app/results"]

# Set environment variables
ENV PORT=8000
ENV HOST=0.0.0.0
ENV PYTHONUNBUFFERED=1
ENV MPLBACKEND=Agg

# Expose port
EXPOSE 8000

# Initialize matplotlib with Agg backend
RUN python3 -c "import matplotlib; matplotlib.use('Agg')"

# Start the FastAPI application
CMD ["python", "-m", "uvicorn", "halal_compliance_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
