create database queue;

use queue;

create table queue (
	eid int not null,
    uid int not null,
    stat varchar(255),
    createdAt timestamp default current_timestamp not null,
    readyAt timestamp,
    constraint primary key (eid,uid),
    constraint foreign key (eid) references event.event (eid),
	constraint foreign key (uid) references user.user (uid)

);

DELIMITER $$

CREATE TRIGGER before_queue_update
BEFORE UPDATE
ON queue FOR EACH ROW
BEGIN
    IF OLD.stat = "Waiting" and NEW.stat = "Ready" THEN
		SET NEW.ReadyAt = current_timestamp();
    END IF;
END$$

DELIMITER ;


