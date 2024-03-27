create database queue;

use queue;

CREATE TABLE queue (
    eid INT NOT NULL,
    uid INT NOT NULL,
    status VARCHAR(255) default "Waiting",
    checkout_session_id VARCHAR(70),
    createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    readyAt TIMESTAMP NULL DEFAULT NULL,
    CONSTRAINT PRIMARY KEY (eid, uid),
    CONSTRAINT FOREIGN KEY (eid) REFERENCES event.event (eid),
    CONSTRAINT FOREIGN KEY (uid) REFERENCES user.user (uid)
);

DELIMITER //

CREATE TRIGGER before_queue_update
BEFORE UPDATE
ON queue FOR EACH ROW
BEGIN
    IF OLD.status = "Waiting" and NEW.status = "Ready" THEN
		SET NEW.ReadyAt = current_timestamp();
    END IF;
END//

DELIMITER ;


