create database event;
use event;

CREATE TABLE event (
    EID INT auto_increment PRIMARY KEY,
    EVENTNAME VARCHAR(255) not null,
    Date datetime not null,
    Location VARCHAR(255) not null,
    description VARCHAR(255),
    Capacity INT not null,
    Price FLOAT not null
);

insert into event (eventname, date, location, description, capacity, price) values (
	"Eras Tour",
    "2024-04-15 13:00:00",
    "National Stadium", 
    "I love taylor",
    10,
    15.00);
    
insert into event (eventname, date, location, description, capacity, price) values (
	"Nathan Tour",
    "2024-04-16 13:00:00",
    "International Stadium,Malaysia", 
    "I love Nathan",
    14,
    30.00)
    
    
