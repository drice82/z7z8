FROM teddysun/v2ray as builder

FROM alpine 

RUN apk add --update --no-cache python3 docker-cli && \
    rm -rf /var/cache/apk/* /tmp/* /var/tmp/* $HOME/.cache

WORKDIR /usr/src/app

COPY --from=builder /usr/bin/v2ctl /usr/bin/
COPY . .

CMD [ "python3", "./v2cli.py" ]
