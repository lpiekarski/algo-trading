FROM ubuntu:latest

COPY files/ files/

RUN apt-get update
RUN apt-get install -y $(cat files/dependencies.txt)
RUN git config --global user.name "Automated"
RUN git config --global user.email "l.piekarski@student.uw.edu.pl"
RUN git lfs install
RUN python3 -m venv venv --upgrade-deps
RUN ./venv/bin/python3 -m pip install -r files/requirements.txt
ENV COLOR_OUTPUT=true