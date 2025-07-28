FROM --platform=linux/amd64 python:3.9-slim-buster as base
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ./model /app/model
COPY . /app

# Create input/output dirs for runtime
RUN mkdir -p /app/input /app/output

ENTRYPOINT ["python", "round1b_persona_intelligence.py", "--input", "/app/input", "--output", "/app/output"]
