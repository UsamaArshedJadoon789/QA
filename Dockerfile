# Use Python 3.12 slim image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies and poetry
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    python3-numpy \
    python3-matplotlib \
    && rm -rf /var/lib/apt/lists/* && \
    pip install poetry

# Copy poetry files
COPY pyproject.toml poetry.lock* README.md ./

# Copy application code
COPY ./app ./app/

# Install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Create results directory with proper permissions and ensure it persists
RUN mkdir -p /app/results/visualizations/slaughterhouse/2d && \
    mkdir -p /app/results/visualizations/slaughterhouse/3d && \
    mkdir -p /app/results/visualizations/food_processing/2d && \
    mkdir -p /app/results/visualizations/food_processing/3d && \
    chmod -R 777 /app/results

# Create a volume for results persistence
VOLUME ["/app/results"]

# Set environment variables
ENV PORT=8000
ENV HOST=0.0.0.0
ENV PYTHONMALLOC=debug
ENV MALLOC_TRIM_THRESHOLD_=65536
ENV PYTHONUNBUFFERED=1
ENV MPLBACKEND=Agg
ENV OMP_NUM_THREADS=1
ENV OPENBLAS_NUM_THREADS=1
ENV MKL_NUM_THREADS=1
ENV VECLIB_MAXIMUM_THREADS=1
ENV NUMEXPR_NUM_THREADS=1

# Expose port
EXPOSE 8000

# Pre-generate data and visualizations during build with detailed logging
RUN python3 -c "import matplotlib; matplotlib.use('Agg')" && \
    PYTHONUNBUFFERED=1 poetry run python -u app/generate_test_data.py 2>&1 | tee /tmp/visualization_generation.log && \
    cat /tmp/visualization_generation.log && \
    echo "Checking visualization directory contents:" && \
    ls -la /app/results/visualizations/ || \
    (echo "Error: Visualization generation failed. Log contents:" && \
     cat /tmp/visualization_generation.log && \
     exit 1)

# Start the application
CMD poetry run uvicorn app.main:app --host 0.0.0.0 --port ${PORT}
