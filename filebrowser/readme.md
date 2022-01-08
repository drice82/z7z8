```
docker run -d \
    --name filebrowser \
    --restart always \
    -v /home/filebrowser/srv:/srv \
    -v /home/filebrowser/database:/database \
    -v /home/filebrowser/config:/config \
    -p 80:80 \
    filebrowser/filebrowser:s6
```
