FROM phusion/baseimage:0.11 as builder

RUN apt-get update
RUN apt-get install curl -y
RUN curl -L -o /tmp/go.sh https://install.direct/go.sh
RUN chmod +x /tmp/go.sh
RUN /tmp/go.sh

FROM phusion/baseimage:0.11

COPY --from=builder /usr/bin/v2ray/v2ray /usr/bin/v2ray/
COPY --from=builder /usr/bin/v2ray/v2ctl /usr/bin/v2ray/
COPY --from=builder /usr/bin/v2ray/geoip.dat /usr/bin/v2ray/
COPY --from=builder /usr/bin/v2ray/geosite.dat /usr/bin/v2ray/

# 设置正确的环境变量.
ENV PATH /usr/bin/v2ray:$PATH

# 生成SSH keys,baseimage-docker不包含任何的key,所以需要你自己生成.你也可以注释掉这句命令,系统在启动过程中,会生成一个.
#RUN /etc/my_init.d/00_regen_ssh_host_keys.sh
RUN rm -rf /etc/service/sshd /etc/my_init.d/00_regen_ssh_host_keys.sh

# 初始化baseimage-docker系统
CMD ["/sbin/my_init"]

# 这里可以放置你自己需要构建的命令
RUN apt-get update \
    && apt-get install -y iproute2 nginx \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* 

#copy app and config
COPY /root/v2ray /etc/v2ray/
COPY /root/v2muser /usr/bin/v2muser/
COPY /root/nginx /etc/nginx/conf.d/ 
COPY /root/www /var/www/html
COPY /root/cert /etc/nginx/cert/
COPY /root/serverstatus/client-linux.py /usr/bin/srvstatus/

#copy init
COPY /init /etc/my_init.d/

#copy scripts
COPY /runit /etc/service/

#文件权限
RUN chmod u+x /etc/service/v2ray/run \
    && chmod u+x /etc/service/nginx/run \
    && chmod u+x /etc/service/v2muser/run \
    && chmod u+x /etc/service/srvstatus/run \
    && chmod u+x /etc/my_init.d/* 

EXPOSE 80 443 8081
