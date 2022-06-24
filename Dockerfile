FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN apt update && apt install -y git gcc

RUN pip3 install -r requirements.txt

COPY . .

CMD ["gunicorn", "-b", ":5000", "--access-logfile", "-", "--error-logfile", "-", "app:app"]
