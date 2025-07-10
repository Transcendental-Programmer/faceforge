FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Copy requirements and install
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy all code
COPY . .

# Expose Gradio port
EXPOSE 7860

# Run Gradio app
CMD ["python", "faceforge_ui/app.py"] 