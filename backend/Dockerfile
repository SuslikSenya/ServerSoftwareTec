FROM python:3.12.6-slim-bullseye

WORKDIR /

COPY requirements.txt .

RUN python -m pip install -r requirements.txt

COPY . .

WORKDIR /src

EXPOSE 8000

#ENV DATABASE_URL="postgresql+asyncpg://sasha:NOV87CMvgEy7OKXP7kkOn0tgAUENFAeL@dpg-ctad51jtq21c73c3jvpg-a.oregon-postgres.render.com/lab3_au3f"
ENV DATABASE_URL="postgresql+asyncpg://sasha:Tsa0zS5iXO1Y6xyfvJXtDCVAcUuZAqQ6@dpg-cvdvtpnnoe9s73ejduvg-a.oregon-postgres.render.com/test_xaa1"

CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "main:app", "-b", "0.0.0.0:8000"]
