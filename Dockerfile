FROM python:3.12.6-slim-bullseye

WORKDIR /

COPY requirements.txt .

RUN python -m pip install -r requirements.txt

COPY . .

WORKDIR /src

EXPOSE 8000

CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "main:app", "-b", "0.0.0.0:8000"]
