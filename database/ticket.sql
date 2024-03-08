create database ticket;
use ticket;

CREATE TABLE ticket_event(
     EID INT auto_increment PRIMARY KEY,
     constraint foreign key (EID) references event.event (eid),
     tickets_left int not null
);

CREATE TABLE ticket (
     EID INT,
     constraint foreign key (EID) references ticket_event (eid),
     UID int, 
     constraint foreign key (UID) references user.user (uid),
	 constraint primary key (eid,uid),
	 TID varchar(36) DEFAULT (UUID())
);

DELIMITER $$

create trigger `add_ticket_trigger` 
    after insert on `ticket` 
    for each row 
    begin
        update `ticket_event` set `tickets_left` = `tickets_left` - 1 where `eid` = new.eid;
    end$$
    
DELIMITER ;
    
insert into ticket_event (tickets_left) values (10), (14);