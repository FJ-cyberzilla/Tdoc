# Use Python 3.11 slim image
FROM python:3.11-slim

# Install UV
RUN pip install uv

# Set working directory
WORKDIR /app

# Copy pyproject.toml and uv.lock first (for better caching)
COPY pyproject.toml uv.lock ./

# Install dependencies using UV
RUN uv sync --no-dev

# Copy the rest of the application
COPY src/ ./src/
COPY docs/ ./docs/
COPY Makefile ./

# Set Python path
ENV PYTHONPATH=/app

# Run the application
CMD ["uv", "run", "python", "src/main.py"]
