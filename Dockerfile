FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN apt update && apt install -y git gcc libpq-dev

RUN pip3 install -r requirements.txt

COPY . .

CMD ["gunicorn", "-b", ":5000", "--workers", "1", "--threads", "4", "--log-level", "warning", "--access-logfile", "-", "--error-logfile", "-", "app:app"]
