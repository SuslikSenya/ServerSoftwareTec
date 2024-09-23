FROM python:3.12.6-slim-bullseye

WORKDIR /app

COPY requirements.txt .

RUN python -m pip install -r requirements.txt

COPY . /app

WORKDIR /app/src

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
