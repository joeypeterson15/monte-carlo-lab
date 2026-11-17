FROM python:3.13-slim
WORKDIR /app
RUN useradd --create-home --uid 10001 worker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY main.py .
USER worker
HEALTHCHECK --interval=10s --timeout=5s --start-period=10s --retries=5 \
  CMD python -c "import os,redis; redis.Redis.from_url(os.environ['REDIS_URL']).ping()"
CMD ["python", "-u", "main.py"]
