FROM python:3.9-slim

WORKDIR /app

COPY . .

ENV PYTHONPATH="/app/src:${PYTHONPATH}"

RUN python3 -m pip install --no-cache-dir -r requirements-dev.txt

EXPOSE 8000

# Start the application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
