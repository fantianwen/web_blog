create table Users(
    `id` int primary key auto_increment,
    `username` varchar(30) not null,
    `password` varchar(30) not null
)engine=innodb default charset=utf8;


insert into user (host,user,password,select_priv,insert_priv,update_priv) values ('localhost','blog',password('Fantianwen09'),'y','y','y');


