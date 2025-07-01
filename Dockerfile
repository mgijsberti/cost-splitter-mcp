FROM python:3.11-slim

WORKDIR /app

COPY . .

# Install security updates and clean up
RUN apt-get update \
    && apt-get upgrade -y \
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

EXPOSE 8000

CMD ["fastmcp", "run", "main.py", "--transport", "http", "--host", "0.0.0.0", "--port", "8000"] 