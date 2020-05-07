FROM python:alpine

RUN apk add --update gcc libc-dev linux-headers iproute2 procps && \
    rm -rf /var/cache/apk/* /tmp/* /var/tmp/* $HOME/.cache

RUN pip install psutil

WORKDIR /usr/src/app

COPY . .

CMD [ "python", "./client-psutil.py"]

