docker run -d \
--name=nginx-status \
--restart=always \
-p 80:80 \
-p 443:443 \
-v /home/nginx-status:/etc/nginx/conf.d \
-e STATUS_ADDRESS=status.com \
-e STATUS_USER=s02 \
nginx-status:v1
