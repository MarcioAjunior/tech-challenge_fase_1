FROM python:3.11.9-slim

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

CMD unicorn main::app --port8000 --host=0.0.0.0