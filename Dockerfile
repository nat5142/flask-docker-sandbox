FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN apt update && apt install -y git gcc libpq-dev

RUN pip3 install -r requirements.txt

COPY . .

ENTRYPOINT ["./boot.sh"]
