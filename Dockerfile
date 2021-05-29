FROM python:3.8-alpine
ENV PYTHONUNBUFFERED=1
RUN apk update && apk add alpine-sdk gcc musl-dev python3-dev libffi-dev openssl-dev && apk add postgresql-dev gcc python3-dev musl-dev
WORKDIR /django
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt