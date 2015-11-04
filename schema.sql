create table Users(
    `id` int primary key auto_increment,
    `username` varchar(30) not null,
    `password` varchar(30) not null
)engine=innodb default charset=utf8;
