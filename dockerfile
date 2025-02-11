# syntax=docker/dockerfile:1

FROM python:3.11.7

COPY app/ .

RUN pip3 install -r requirements.txt

ENTRYPOINT ["/docker-entrypoint.sh"]
