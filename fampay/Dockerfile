# pull official base image
FROM python:3.9-slim-buster
LABEL maintainer=uddipta
# set work directory
WORKDIR /fampay
ADD requirements.txt /fampay

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install dependencies required for psycopg2 python package
RUN apt-get -qq update -y  \
    && apt-get --no-install-recommends -y install gcc postgresql vim \
    && apt-get autoclean && rm -rf /var/lib/apt/lists/* \
    && pip3 install --upgrade pip \
    && pip3 install -r requirements.txt


# copy entrypoint.sh
ADD entrypoint.sh /fampay

# copy project
ADD . /fampay

