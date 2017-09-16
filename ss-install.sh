dpkg-reconfigure tzdata 
apt-get update
apt-get install python-pip git python-m2crypto supervisor vnstat lftp fail2ban wget 
pip install cymysql
cd /
git clone -b manyuser https://github.com/drice82/shadowsocks.git
cd /shadowsocks
echo "[program:shadowsocks]" > /etc/supervisor/conf.d/shadowsocks.conf
echo "command=python /shadowsocks/server.py" >> /etc/supervisor/conf.d/shadowsocks.conf
echo "autorestart=true" >> /etc/supervisor/conf.d/shadowsocks.conf
echo "user=root" >> /etc/supervisor/conf.d/shadowsocks.conf

nano /shadowsocks/usermysql.json

service supervisor start 
supervisorctl reload
echo "ulimit -n 51200" >>/etc/profile
echo "ulimit -Sn 4096" >>/etc/profile
echo "ulimit -Hn 8192" >>/etc/profile
echo "ulimit -n 51200" >>/etc/default/supervisor
echo "ulimit -Sn 4096" >>/etc/default/supervisor
echo "ulimit -Hn 8192" >>/etc/default/supervisor
