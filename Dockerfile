# Use Python 3.11 slim image
FROM python:3.11-slim

# Install UV
RUN pip install uv

# Set working directory
WORKDIR /app

# Copy everything
COPY . .

# Create README.md if missing
RUN if [ ! -f README.md ]; then echo "# Tdoc" > README.md; fi

# Install using UV pip (skips the package build issue)
RUN uv pip install --system -e .

# Set Python path
ENV PYTHONPATH=/app

# Run the application
CMD ["tdoc"]
