FROM teddysun/v2ray as builder

FROM alpine 

RUN apk add --update --no-cache python3 docker-cli py3-pip && \
    rm -rf /var/cache/apk/* /tmp/* /var/tmp/* $HOME/.cache

RUN pip install pymysql

WORKDIR /app

COPY --from=builder /usr/bin/v2ctl /usr/bin/
COPY ./v2cli.py .

CMD [ "python3", "./v2cli.py" ]
