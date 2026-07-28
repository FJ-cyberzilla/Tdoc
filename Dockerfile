# Use Python 3.11 slim image
FROM python:3.11-slim

# Install UV and make
RUN apt-get update && apt-get install -y make && rm -rf /var/lib/apt/lists/*
RUN pip install uv

# Set working directory
WORKDIR /app

# Copy project files
COPY pyproject.toml uv.lock README.md ./

# If README.md doesn't exist, create it
RUN if [ ! -f README.md ]; then echo "# Tdoc - System Diagnostics & Control HUD" > README.md; fi

# Install dependencies using UV
RUN uv sync --no-dev

# Copy the rest of the application
COPY . .

# Set Python path
ENV PYTHONPATH=/app

# Run the application using UV
CMD ["uv", "run", "python", "src/main.py"]
