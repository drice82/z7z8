FROM teddysun/xray as builder

FROM alpine:3.16

RUN apk add --update --no-cache python3 py3-pip && \
    rm -rf /var/cache/apk/* /tmp/* /var/tmp/* $HOME/.cache

RUN pip install pymysql

WORKDIR /app

COPY --from=builder /usr/bin/xray /usr/bin/
COPY . .

CMD [ "python3", "-u", "./v2cli.py" ]
