FROM ubuntu:latest

COPY files/ files/
COPY ../requirements.txt requirements.txt

RUN apt-get update
RUN apt-get install -y $(cat files/dependencies.txt)
RUN python3 -m venv venv --upgrade-deps
RUN ./venv/bin/python3 -m pip install -r requirements.txt