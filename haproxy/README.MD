docker run -d --name haproxy \
 -v /home/haproxy:/usr/local/etc/haproxy \
 --net=host \
 haproxy:alpine 
