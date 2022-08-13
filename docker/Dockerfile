FROM ubuntu:latest

COPY files/ files/

RUN apt-get update
RUN apt-get install -y $(cat files/dependencies.txt)
RUN python -m venv venv --upgrade-deps
RUN source venv/bin/activate
RUN pip install -r requirements.txt