# syntax=docker/dockerfile:1

FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt 

# copy everything after tests to speed up caching
COPY . .

# install the logger with pip
RUN pip install -e .

CMD python -u nycmesh_metrics_logger