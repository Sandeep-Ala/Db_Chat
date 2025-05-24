FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     build-essential \
#     gcc \
#     && apt-get clean \
#     && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirments.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirments.txt

# Copy application code
COPY . .

# Expose the Streamlit port
EXPOSE 8501

# Command to run the application
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]