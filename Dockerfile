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

# Create directories with correct permissions
RUN mkdir -p /app/results/visualizations && \
    chmod -R 777 /app/results && \
    chown -R nobody:nogroup /app/results

# Initialize matplotlib with Agg backend
RUN python3 -c "import matplotlib; matplotlib.use('Agg')"

# Create a startup script with enhanced error handling
RUN echo '#!/bin/bash\n\
MAX_RETRIES=3\n\
RETRY_COUNT=0\n\
\n\
while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do\n\
    echo "Attempt $(($RETRY_COUNT + 1)) of $MAX_RETRIES to generate visualizations..."\n\
    python -u app/generate_test_data.py\n\
    if [ $? -eq 0 ]; then\n\
        echo "=== Visualization Generation Successful ==="\n\
        echo "Checking visualization files..."\n\
        for model in slaughterhouse food_processing; do\n\
            for dim in 2d 3d; do\n\
                DIR="/app/results/visualizations/$model/$dim"\n\
                echo "Checking $DIR..."\n\
                if [ ! -d "$DIR" ]; then\n\
                    echo "Error: Directory $DIR does not exist"\n\
                    RETRY_COUNT=$((RETRY_COUNT + 1))\n\
                    continue 2\n\
                fi\n\
                ls -la "$DIR"\n\
                COUNT=$(ls -1 "$DIR"/*.png 2>/dev/null | wc -l)\n\
                if [ $COUNT -eq 0 ]; then\n\
                    echo "Error: No visualization files found in $DIR"\n\
                    RETRY_COUNT=$((RETRY_COUNT + 1))\n\
                    continue 2\n\
                fi\n\
                echo "Found $COUNT visualization files in $DIR"\n\
            done\n\
        done\n\
        echo "All visualizations verified successfully"\n\
        echo "Starting FastAPI application..."\n\
        exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT}\n\
        exit 0\n\
    else\n\
        echo "Visualization generation failed on attempt $(($RETRY_COUNT + 1))"\n\
        RETRY_COUNT=$((RETRY_COUNT + 1))\n\
        if [ $RETRY_COUNT -lt $MAX_RETRIES ]; then\n\
            echo "Retrying in 5 seconds..."\n\
            sleep 5\n\
        fi\n\
    fi\n\
done\n\
\n\
echo "Failed to generate visualizations after $MAX_RETRIES attempts"\n\
exit 1' > /app/start.sh && \
chmod +x /app/start.sh

# Start the application with data generation
CMD ["/app/start.sh"]
