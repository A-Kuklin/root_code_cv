FROM python:3.10

WORKDIR /code

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

ENV app_host "0.0.0.0"
ENV app_port 8080

CMD ["sh", "-c", "uvicorn app:app --host $app_host --port $app_port"]
