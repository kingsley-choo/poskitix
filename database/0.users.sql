create database user;
use user;
CREATE TABLE user (
	uid int NOT NULL AUTO_INCREMENT,
    username varchar(255) NOT NULL,
	email varchar(250) unique not null,
    primary key (uid)
);

insert into user (username, email) values ("chris","joshlife333+chris@gmail.com");
insert into user (username, email) values ("swetha","joshlife333+swetha@gmail.com");
insert into user (username, email) values ("nathan","joshlife333+nathan@gmail.com");
insert into user (username, email) values ("kingsley","joshlife333+kingsley@gmail.com");
insert into user (username, email) values ("germaine","joshlife333+germaine@gmail.com");
insert into user (username, email) values ("henry","joshlife333+henry@gmail.com");
insert into user (username, email) values ("zan","joshlife333+zan@gmail.com");
insert into user (username, email) values ("marco","joshlife333+marco@gmail.com");
insert into user (username, email) values ("sathwik","joshlife333+sathwik@gmail.com");
insert into user (username, email) values ("fern","joshlife333+fern@gmail.com");
insert into user (username, email) values ("john","joshlife333+john@gmail.com");
insert into user (username, email) values ("rachel","joshlife333+rachel@gmail.com");
insert into user (username, email) values ("neil","joshlife333+neil@gmail.com");
insert into user (username, email) values ("harry","joshlife333+harry@gmail.com");
insert into user (username, email) values ("spongebob","joshlife333+spongebob@gmail.com");

