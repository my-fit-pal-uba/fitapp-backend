# Base Image of dockerfile
FROM python:3.13-slim as base 
WORKDIR /usr/local/app

# Instal dependencies 
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt


# Copy source code
COPY src/ ./src
EXPOSE 8080

RUN useradd app 
USER app

CMD ["python", "src/app.py"]
