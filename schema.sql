create table Users(
    `id` int primary key auto_increment,
    `username` varchar(30) not null,
    `password` varchar(30) not null
)engine=innodb default charset=utf8;


insert into user (host,user,password,select_priv,insert_priv,update_priv) values ('localhost','blog',password('Fantianwen09'),'y','y','y');


create table users(
	`id` varchar(50) primary key not null,
	`email` varchar(50) not null,
	`passwd` varchar(50) not null,
	`admin` bool not null,
	`name` varchar(50) not null,
	`image` varchar(500) not null,
	`created_at` real not null,
	unique key `idx_email` (`email`),
	key `idx_created_at` (`created_at`)
)engine=innodb default charset=utf8;



create table blogs(
	`id` varchar(50) primary key not null,
	`user_id` varchar(50) not null,
	`user_name` varchar(50) not null,
	`user_image` varchar(500) not null,
	`name` varchar(50) not null,
	`summary` varchar(200) not null,
	`content` mediumtext not null,
	`created_at` real not null,
	key `idx_created_at` (`created_at`)
)engine=innodb default charset=utf8;

create table comments(
	`id` varchar(50) primary key not null,
	`blog_id` varchar(50) not null,
	`user_id` varchar(50) not null,
	`user_name` varchar(50) not null,
	`user_image` varchar(500) not null,
	`content` mediumtext not null,
	`created_at` real not null,
	key `idx_created_at` (`created_at`)
)engine=innodb default charset=utf8;