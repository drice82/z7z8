FROM alpine

RUN apk add --update coreutils python3 iproute2 procps && \
    rm -rf /var/cache/apk/* /tmp/* /var/tmp/* $HOME/.cache

WORKDIR /usr/src/app

COPY . .

CMD [ "python3", "-u", "./client-linux.py"]

