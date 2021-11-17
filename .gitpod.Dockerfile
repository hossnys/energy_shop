FROM ubuntu:20.04

LABEL maintainer="rob@threefold.tech"

# Update Ubuntu
RUN apt-get update
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Amsterdam
RUN apt-get install -y tzdata
RUN apt-get upgrade -y

# install prerequisites
RUN apt-get install -y git python3-venv python3-pip redis-server tmux nginx
RUN pip3 install poetry

RUN apt-get install -y python3-pyqt5 libsecp256k1-0 python3-cryptography curl && \
    curl https://download.electrum.org/4.1.5/Electrum-4.1.5.tar.gz -o Electrum-4.1.5.tar.gz  && \
    pip3 install Electrum-4.1.5.tar.gz

# create the datafolder and mark it as a volume
RUN mkdir /data
VOLUME /data

# install js-sdk dependancies
RUN mkdir -p /code/tftshop/jumpscale/packages/gettft && touch /code/tftshop/jumpscale/packages/gettft/__init__.py
WORKDIR /code/tftshop
COPY pyproject.toml /code/tftshop/
COPY poetry.lock /code/tftshop/
RUN poetry install

# Copy code
COPY . /code/tftshop
USER root

RUN bash  ./entrypoint.sh
