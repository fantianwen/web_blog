阿里云主机安装的是centos 6.5的系统，默认已经安装了python2.x。

###Python3.5 的编译安装
通过ssh连接阿里云服务器，已经是是已root在运行了。
下面的命令如果非root用户，使用`sudo`运行，或者事先进入root用户`su root`

1、下载 python3.5的源代码

```shell
wget https://www.python.org/ftp/python/3.5.0/Python-3.5.0.tgz
```
在云环境中还是挺快的，一会就下载好了

2、解压缩

```shell
tar zxvf Python-3.5.0.tgz
```

3、进入解压缩后的文件

```shell
cd Python-3.5.0
```

4、指定编译成功后安装的目录

```shell
./configure --prefix=/usr/local/python3
```

5、编译和安装

```shell
make -j8 && make install 
```

这里的`-j8`指的使用8个线程进行编译，一般是`电脑的核心数*2`

6、如果编译并安装成功了，设置python3的环境变量

查看PATH环境变量

```shell
echo $APTH
```

设置

```shell
PATH=$PATH:/PYTHON_HOME/bin
```

再次查看,检查是否已经添加

```shell
echo $PATH
```

7、出现的问题

>linux安装python时无法configure

需要安装`gcc`

```shell
yum install gcc
```



>Ignoring ensurepip failure: pip 7.1.2 req
No package openssl-devel available.

最后的python安装阶段出现了这样的问题，根据提示安装`openssl-devel`

在`centos`中使用`yum`进行安装

```shell
yum install openssl-devel
```

安装成功后，重新编译安装，成功！














