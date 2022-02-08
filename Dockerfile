FROM python:3.9-slim-bullseye

RUN useradd -m -d /home/appuser appuser
USER appuser
WORKDIR /app

ENV PATH=/home/appuser/.local/bin:$PATH \
    PYTHONUNBUFFERED=1                  \
    PYTHONDONTWRITEBYTECODE=1           \
    PIP_NO_CACHE_DIR=1                  \
    PIP_PROGRESS_BAR=off                \
    PIP_NO_COLOR=1                      \
    PIP_DISABLE_PIP_VERSION_CHECK=1     \
    PIP_USER=1

COPY --chown=appuser requirements.txt /tmp/requirements.txt
RUN pip install --user -r /tmp/requirements.txt && rm /tmp/requirements.txt

EXPOSE 8080
CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--forwarded-allow-ips", "*" ]

COPY --chown=appuser . .
