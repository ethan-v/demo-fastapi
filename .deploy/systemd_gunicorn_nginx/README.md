
# Deploy Production

Use Sytemd Service, Gunicorn & Nginx 

## Systemd

Start & enable the service.

```shell
$ sudo systemctl start fastapi_demo
$ sudo systemctl enable fastapi_demo
```

To verify if everything works run the following command.

```shell
$ sudo systemctl status fastapi_demo
```

## Nginx

sudo nano /etc/nginx/sites-available/fastapi_demo


```
server {

    listen 80;

    server_name your_domain www.your_domain;



    location / {

        proxy_pass http://unix:/home/demo/fastapi_demo/gunicorn.sock;

    }

}
```