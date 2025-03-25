FROM python:3.9

WORKDIR /app

COPY src/ ./src
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENV PORT=5000

CMD ["python", "src/app.py"]
