# syntax=docker/dockerfile:1.4
FROM --platform=$BUILDPLATFORM python:3.11-alpine AS builder

WORKDIR /code
COPY ../.. .
RUN --mount=type=cache,target=/root/.cache/pip \
pip3 install -r requirements.txt

CMD ["python3", "main.py"]
