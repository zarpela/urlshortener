create database if not exists URLShortener;

use URLShortener;

create table if not exists url( 
	originalURL varchar(2048) not null,
    shortID char(8) not null unique
);


