create database queue;

use queue;

CREATE TABLE queue (
    eid INT NOT NULL,
    uid INT NOT NULL,
    stat VARCHAR(255),
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
    IF OLD.stat = "Waiting" and NEW.stat = "Ready" THEN
		SET NEW.ReadyAt = current_timestamp();
    END IF;
END//

DELIMITER ;


