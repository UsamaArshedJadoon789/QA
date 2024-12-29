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

# Initialize matplotlib with Agg backend
RUN python3 -c "import matplotlib; matplotlib.use('Agg')"

# Start the application with data generation
CMD poetry run python -u app/generate_test_data.py && poetry run uvicorn app.main:app --host 0.0.0.0 --port ${PORT}
