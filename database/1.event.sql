create database event;
use event;

CREATE TABLE event (
    EID INT auto_increment PRIMARY KEY,
    EVENTNAME VARCHAR(255) not null,
    Date datetime not null,
    SalesDate datetime not null,
    Location VARCHAR(255) not null,
    description VARCHAR(255),
    Capacity INT not null,
    Price FLOAT not null
);

insert into event (eventname, date, salesdate, location, description, capacity, price) values (
	"Joshua Tour",
    "2024-04-15 13:00:00",
    "2024-03-20 13:00:00",
    "National Stadium", 
    "I love taylor (not really)",
    10,
    15.00);
    
insert into event (eventname, date, salesdate, location, description, capacity, price) values (
	"Nathan Tour Night 1(Cat 1)",
    "2024-04-16 13:00:00",
    "2024-03-20 13:00:00",
    "International Stadium, Malaysia", 
    "Get up close with Nathan",
    14,
    30.00);

insert into event (eventname, date, salesdate, location, description, capacity, price) values (
	"Nathan Tour Night 1(Cat 2)",
    "2024-04-16 13:00:00",
    "2024-03-20 13:00:00",
    "International Stadium, Malaysia", 
    "I love Nathan but not enough for Cat 1!",
    20,
    15.00);

insert into event (eventname, date, salesdate, location, description, capacity, price) values (
	"Kingsley Tour Night (Free Seating)",
    "2024-05-16 13:00:00",
    "2024-04-03 17:00:00",
    "Germaine's Stadium, Myanmmar", 
    "I love Nathan",
    30,
    69.00);
    
    
