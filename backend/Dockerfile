FROM python:3.12-slim as builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.12-slim

WORKDIR /app

COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

ENV PYTHONUNBUFFERED=1 \
    EVENTLET_NO_GREENDNS=yes

RUN useradd -m appuser && \
    chown -R appuser:appuser /app

COPY app/ ./app/
COPY wsgi.py .

RUN mkdir -p /app/instance && \
    chown -R appuser:appuser /app/instance

USER appuser

EXPOSE 5000

CMD ["gunicorn", \
     "--worker-class", "eventlet", \
     "--bind", "0.0.0.0:5000", \
     "--workers", "1", \
     "--threads", "1000", \
     "--timeout", "120", \
     "--keep-alive", "65", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "wsgi:app"]
