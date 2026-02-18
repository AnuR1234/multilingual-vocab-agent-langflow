FROM langflowai/langflow:1.6.9

RUN /app/.venv/bin/pip install --no-cache-dir psycopg2-binary
ENV PATH="/app/.venv/bin:$PATH"

CMD ["python", "-m", "langflow", "run", "--host", "0.0.0.0", "--port", "7860"]


