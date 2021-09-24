FROM python:3.9

ENV PYTHONBUFFERED True
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir pip -r requirements.txt

COPY . .
CMD [ "uvicorn", "main:app" ]