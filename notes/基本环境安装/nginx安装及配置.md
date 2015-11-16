####服务器环境：centos 6.5

#####安装
1、安装Nginx（enginee X）

```shell
yum install nginx
```

2、可能遇到无法安装的情况，需要安装epel

nginx不是官方库，需要安装第三方软件源的支持

#####配置

在`/etc/nginx/nginx.conf`中可以看见

``` python
# Load config files from the /etc/nginx/conf.d directory
# The default server is in conf.d/default.conf
```

所以，到`/etc/nginx/conf.d/default.conf`中进行配置

```shell
vim /etc/nginx/conf.d/default.conf
```

打开看见：

```vim
#
# The default server
#
server {
    listen       8080;                  
    server_name  radasm.me;
    root        /srv/web_blog;
    access_log  web_blog/web_blog/access_log;
    error_log   web_blog/web_blog/error_log;
    #charset koi8-r;

    #access_log  logs/host.access.log  main;

    # Load configuration files for the default server block.
    # include /etc/nginx/default.d/*.conf;
    # 处理静态文件/favicon.ico:
    location /favicon.ico {
        root /srv/web_blog;
    }

    # 处理静态资源:
    location ~ ^\/static\/.*$ {
        root /srv/web_blog;
    }
    
    location / {
        proxy_pass       http://127.0.0.1:5000;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        #root   /usr/share/nginx/html;
        #index  index.html index.htm;
    }

    error_page  404              /404.html;
    location = /404.html {
        root   /usr/share/nginx/html;
    }

    # redirect server error pages to the static page /50x.html
    #
    error_page   500 502 503 504  /50x.html;
    location = /50x.html {
        root   /usr/share/nginx/html;
    }
```

主要需要处理的是`server`模块和`location`模块中对静态资源和根路径的处理

其中


```vim 
    listen       8080;                  
    server_name  radasm.me;
    root        /srv/web_blog;
    access_log  web_blog/web_blog/access_log;
    error_log   web_blog/web_blog/error_log;
```

表明监听8080端口，根目录是 `/srv/web_blog`

access_blog 中会打印工程运行过程中的日志信息

需要注意的是，access_log和error_log的默认的根目录是`/usr/share/nginx`

```vim
location / {
        proxy_pass       http://127.0.0.1:5000;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        #root   /usr/share/nginx/html;
        #index  index.html index.htm;
    }
```

表明会将“/”转发到“http://127.0.0.1:5000”，即为本机的5000端口，这正是flask配置的运行的端口。















