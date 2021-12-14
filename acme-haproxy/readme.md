```
docker-compose run acme.sh --register-account  -m xxx@gmail.com --server zerossl
docker-compose run acme.sh --issue -d www.xxx.com --dns dns_cf --server zerossl
docker-compose run acme.sh --deploy -d www.xxx.com --deploy-hook haproxy
```
reference to
https://github.com/acmesh-official/acme.sh/wiki/deploy-to-docker-containers

For Haproxy:
https://github.com/acmesh-official/acme.sh/wiki/deployhooks
