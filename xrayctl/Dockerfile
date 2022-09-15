FROM teddysun/xray as xray
FROM golang:alpine as builder

WORKDIR /usr/src/app

COPY . .

RUN go mod download && go mod verify

RUN go build -o /usr/src/app/xrayctl main.go updateTraffic.go renewClients.go

FROM alpine

RUN apk add --update --no-cache tzdata && \
    cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    echo "Asia/Shanghai" > /etc/timezone && \
    rm -rf /var/cache/apk/* /tmp/* /var/tmp/* $HOME/.cache 

WORKDIR /app

COPY --from=xray /usr/bin/xray /usr/local/bin/
COPY --from=builder /usr/src/app/xrayctl /usr/local/bin/
COPY --from=builder /usr/src/app/xtls_inbounds.json /app
COPY --from=builder /usr/src/app/xtls_and_ss_inbounds.json /app

CMD ["xrayctl"]
