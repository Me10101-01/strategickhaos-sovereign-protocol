FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Python dependencies
RUN pip install --no-cache-dir pyyaml

# Copy DAMON agent code
COPY damon/damon-agent.py /app/damon-agent.py
COPY damon/configs /app/configs

# Make the agent executable
RUN chmod +x /app/damon-agent.py

# Default command runs all DAMONs
CMD ["python", "/app/damon-agent.py", "--all", "/app/configs", "--project-root", "/project"]
