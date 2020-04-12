#!/bin/sh

sed -ri "s/MYSQL_HOST/$MYSQL_HOST/g" /usr/bin/v2muser/v2muser.py
sed -ri "s/MYSQL_PORT/$MYSQL_PORT/g" /usr/bin/v2muser/v2muser.py
sed -ri "s/MYSQL_USER/$MYSQL_USER/g" /usr/bin/v2muser/v2muser.py
sed -ri "s/MYSQL_PASSWORD/$MYSQL_PASSWORD/g" /usr/bin/v2muser/v2muser.py
sed -ri "s/MYSQL_DBNAME/$MYSQL_DBNAME/g" /usr/bin/v2muser/v2muser.py
sed -ri "s/SETMUL/$SETMUL/g" /usr/bin/v2muser/v2muser.py


