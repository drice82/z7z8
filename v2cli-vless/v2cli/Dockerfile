FROM v2fly/v2fly-core:latest as builder

FROM alpine 

RUN apk add --update --no-cache python3 docker-cli && \
    rm -rf /var/cache/apk/* /tmp/* /var/tmp/* $HOME/.cache

WORKDIR /usr/src/app

COPY --from=builder /usr/bin/v2ray/v2ctl /usr/bin/v2ray/
COPY . .

CMD [ "python3", "./v2cli.py" ]
