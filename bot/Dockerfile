FROM python:3.9-slim-bullseye

ENV PYTHONUNBUFFERED True
WORKDIR /bot

COPY ../requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir pip -r /tmp/requirements.txt

COPY .. .