-- proxy database
drop database if exists proxy;
create database proxy default charset utf8;

-- create table
use proxy;
drop table if exists ip;
create table ip(id bigint(32) primary key auto_increment,
                ip varchar(15) not null,
                alive bool default 0,
                location varchar(63) default null comment '位置',
                port int not null comment '端口号',
                alive_time varchar(10) default null comment '存活时间',
                open bool default 0 comment '是否开放',
                proxy bool default false,
                create_time datetime DEFAULT now(),
                update_time datetime DEFAULT now() comment '更新时间',
                anonymous enum('高匿名','匿名','透明') not null comment '匿名程度',
                protocol enum('http','https','socks4','socks5','all_http','all_socks','all') default 'http' comment '支持协议',
                method enum('GET','POST','ALL') default 'ALL' comment '访问支持',
                speed double default 0.0 comment '速度',
                unique key(`ip`,`port`))

