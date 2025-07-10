FROM python:3.10-slim

# Install dependencies
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 7860

# Set environment variables
ENV PYTHONPATH="/app"
ENV PYTHONUNBUFFERED=1
ENV API_URL="/api"
ENV MOCK_API="false"

# Start app (with the patch applied)
CMD ["python", "app.py"] 