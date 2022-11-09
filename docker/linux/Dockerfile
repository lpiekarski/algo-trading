FROM ubuntu:latest

COPY docker/linux/dependencies.txt dependencies.txt
COPY requirements.txt requirements.txt

RUN apt-get update
RUN apt-get install -y $(cat dependencies.txt)
RUN git config --global user.name "Automated"
RUN git config --global user.email "l.piekarski@student.uw.edu.pl"
RUN python3 -m venv venv --upgrade-deps
RUN ./venv/bin/python3 -m pip install -r requirements.txt
ENV COLOR_OUTPUT=true