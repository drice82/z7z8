#!/bin/sh

sed -ri "s/SETUP_USERNAME/$STATUS_USER/g" /usr/bin/srvstatus/client-linux.py
sed -ri "s/SETUP_SERVER_ADDRESS/$STATUS_ADDRESS/g" /usr/bin/srvstatus/client-linux.py
