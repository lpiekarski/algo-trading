FROM ubuntu:latest

COPY . /SP2137

WORKDIR /SP2137
RUN apt-get update
RUN apt-get install -y $(cat docker/linux/dependencies.txt)
RUN git config --global user.name "Automated Workflow"
RUN git config --global user.email "workflow@github.com"
RUN python3 -m venv venv --upgrade-deps
RUN ./venv/bin/python3 -m pip install -r requirements.txt
ENV COLOR_OUTPUT=true
ENV GIT_DRIVE_REPO_URL="https://github.com/S-P-2137/Data"