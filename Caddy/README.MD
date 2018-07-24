#Docker 运行带PHP的Caddy

```
docker run -d \
    -v /home/caddy/Caddyfile:/etc/Caddyfile \
    -v /home/caddy/.caddy:/root/.caddy \
    -v /home/caddy/www:/srv \
    -p 80:80 -p 443:443 -p 2015:2015\
    abiosoft/caddy:php

```
Caddyfile 配置文件
/root/.caddy 证书存放
/srv 网站文件

Caddyfile示例
```
example.com {
    gzip
    root    /srv
fastcgi / 127.0.0.1:9000 php # php variant only
on startup php-fpm7 # php variant only
}
```
