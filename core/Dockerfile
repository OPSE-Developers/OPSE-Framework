FROM ubuntu:22.04

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y python3 \
    && apt-get install -y python3-pip

ADD . /core
WORKDIR /core

RUN pip install -r requirements.txt

# RUN useradd OPSE-dev
# USER OPSE-dev
# 
