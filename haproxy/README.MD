```
global
        maxconn 25600

defaults
        mode tcp
        timeout connect 5000ms
        timeout client 50000ms
        timeout server 50000ms

frontend da-in
        bind *:2222
        default_backend da-source
backend da-source
        server server1 139.99.47.81:2222 maxconn 3200

frontend web80-in
        bind *:80
        default_backend web80-source
backend web80-source
        server server1 139.99.47.81:80 maxconn 3200

frontend web443-in
        bind *:443
        default_backend web443-source
backend web443-source
        server server1 139.99.47.81:443 maxconn 3200

frontend ftp-in
        bind *:20-21
        default_backend ftp-source
backend ftp-source
        server server1 139.99.47.81 maxconn 3200

frontend ftp-passive_ports-in
        bind *:35000-35999
        default_backend ftp-passive_ports-source
backend ftp-passive_ports-source
        server server1 139.99.47.81 maxconn 3200
```
