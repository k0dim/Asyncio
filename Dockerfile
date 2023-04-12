FROM python:3.11-alpine

COPY ./app /app

WORKDIR /app

RUN pip install --no-cache-dir -r /app/requirements.txt

CMD ["python", "main.py"]