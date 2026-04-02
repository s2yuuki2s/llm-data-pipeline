# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Install OpenJDK 17 (Required for PySpark)
RUN apt-get update && \
    apt-get install -y openjdk-17-jre-headless procps curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH=$PATH:$JAVA_HOME/bin
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install uv (modern package manager)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies using uv
RUN uv sync --frozen --no-cache

# Copy project files
COPY . .

# Default command to run the pipeline
CMD ["uv", "run", "bash", "run_pipeline.sh"]
