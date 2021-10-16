FROM python:3.9-slim-bullseye

ENV PYTHONUNBUFFERED True
WORKDIR /app

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir pip -r /tmp/requirements.txt

COPY . .

EXPOSE 8080
CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--forwarded-allow-ips", "*" ]