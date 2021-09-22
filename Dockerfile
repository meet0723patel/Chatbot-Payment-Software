FROM python:3-slim

ENV PYTHONUNBUFFERED True

COPY .env /
COPY requirements.txt /

RUN pip install -r requirements.txt

COPY *.py /

ENTRYPOINT [ "python", "./server.py" ]