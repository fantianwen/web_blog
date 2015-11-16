####服务器环境：centos 6.5


1、查看服务器是否已经安装了mysql

```
rpm -qa | grep mysql
```

如果已经安装了,会看见

>[root@iZ25i3ftaxaZ bin]# rpm -qa | grep mysql
mysql-5.1.73-5.el6_6.x86_64
mysql-libs-5.1.73-5.el6_6.x86_64
mysql-server-5.1.73-5.el6_6.x86_64

2、安装

```
yum install mysql-server
```

3、安装成功之后，需要重置root账户的密码

先启动mysql服务

```
chkconfig mysqld on
```

查看状态：

```
chkconfig --list mysqld
```

看到：
>mysqld         	0:关闭	1:关闭	2:启用	3:启用	4:启用	5:启用	6:关闭

表明可以启动了

启动

```
/etc/rc.d/init.d/mysqld start
```

启动成功之后，设置密码

```
/usr/bin/mysqladmin -u root password '新的密码'
```

4、修改mysql的字符编码

使用新的密码进入mysql之后，查看默认的字符编码

```sql
show variables like '%char%';
```

看到：


```
+--------------------------+----------------------------+
| Variable_name            | Value                      |
+--------------------------+----------------------------+
| character_set_client     | utf8                       |
| character_set_connection | utf8                       |
| character_set_database   | utf8                       |
| character_set_filesystem | binary                     |
| character_set_results    | utf8                       |
| character_set_server     | utf8                       |
| character_set_system     | utf8                       |
| character_sets_dir       | /usr/share/mysql/charsets/ |
+--------------------------+----------------------------+
```

这是已经设置成utf-8的了，如果你看到的和上面的不一致，你需要设置mysql编码

退出mysql，查看`/etc/my.cnf`文件

```
vim /etc/my.cnf
```

将该文本中新增如下：

```
[mysqld]
datadir=/var/lib/mysql
socket=/var/lib/mysql/mysql.sock
user=mysql
# Disabling symbolic-links is recommended to prevent assorted security risks
symbolic-links=0
default-character-set=utf8
[mysqld_safe]
log-error=/var/log/mysqld.log
pid-file=/var/run/mysqld/mysqld.pid
[mysql]
default-character-set=utf8
```
 
 保存，退出，重新启动mysql，并查看字符编码，会看到修改成功了。
 
 5、新建用户，并授权某数据库
 
 ```
 grant all privileges on blog.* to blog@localhost identified by '123456';
 ```
 
 以上将blog数据库下面所有表的权限交给一个名为blog的新用户，并指定新用户的密码为“123456”


 



