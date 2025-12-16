FROM python:3.11-slim

# Set up work directory
WORKDIR /app

# Install OS dependencies only if needed
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     && rm -rf /var/lib/apt/lists/*

# Copy requirements first for caching
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Default command: run your script
CMD ["python", "main.py"]
