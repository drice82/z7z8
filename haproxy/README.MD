docker run -d --name haproxy \
 -v /home/haproxy:/usr/local/etc/haproxy \
 -p 2222:2222 \
 haproxy:alpine 
