FROM v2fly/v2fly-core:latest as builder

FROM alpine:latest

COPY --from=builder /usr/bin/v2ray/v2ctl /usr/bin/v2ray/

RUN apk update && \
    apk add --no-cache docker-cli python3 && \
    rm -rf /var/cache/apk/* /tmp/* /var/tmp/* $HOME/.cache

WORKDIR /usr/src/app

COPY . .

CMD [ "python3", "./v2cli.py" ]
