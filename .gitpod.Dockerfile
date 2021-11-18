FROM gitpod/workspace-full

LABEL maintainer="rob@threefold.tech"

USER root

# Update Ubuntu
RUN apt-get update
RUN apt install sudo -y
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Amsterdam
RUN apt-get install -y tzdata
RUN apt-get upgrade -y

ENV tftshop_wallet_secret="SCX2AQFNVESSTGTNMH5PHA76YRNTY7P6QYLYPOACONGMPGFNPRYK7CHV"
ENV stellar_network="TEST"
ENV network="testnet"
ENV mpk="vpub5VDwtZH8SbRBPRV4c2LNrhDzyaLV7KB4udk55tfDfNkL5mjbEehZRCwte2ydSgVTsq1THG3yfGMTmKa3aNNxbdJ3S1ZwQAorfFRvR1neZr2"

# install prerequisites
RUN apt-get install -y git python3-venv python3-pip redis-server tmux nginx
RUN apt-get install -y python3-pyqt5 libsecp256k1-0 python3-cryptography curl && \
    curl https://download.electrum.org/4.1.5/Electrum-4.1.5.tar.gz -o Electrum-4.1.5.tar.gz  

USER gitpod
RUN pip3 install pip -U
RUN pip3 install poetry 
RUN pip3 install Electrum-4.1.5.tar.gz

# install js-sdk dependancies
RUN mkdir -p code/tftshop/jumpscale/packages/gettft && touch code/tftshop/jumpscale/packages/gettft/__init__.py
WORKDIR code/tftshop
COPY pyproject.toml .
COPY poetry.lock .
RUN poetry install

# Copy code
COPY . .
RUN ./entrypoint.sh
