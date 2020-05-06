FROM python:slim

RUN apt-get update && \
    apt-get install -y iproute2 procps && \
    rm -rf /var/cache/apk/* /tmp/* /var/tmp/* $HOME/.cache

WORKDIR /usr/src/app

COPY . .

CMD [ "python", "./client-linux.py"]

