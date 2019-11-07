SET sql_mode = '';

SET GLOBAL event_scheduler = ON;

CREATE TABLE temp_readings (
	id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	sensor_id INT,
	sensor_reading FLOAT,
	time timestamp
) ENGINE = MEMORY;

CREATE TABLE temp_readings_historical (
	id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	sensor_id INT,
	average_reading FLOAT,
	max_reading FLOAT,
	min_reading FLOAT,
	start_time timestamp,
	end_time timestamp
);

DROP PROCEDURE storeOldRows;

DELIMITER $$
CREATE PROCEDURE storeOldRows()
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
		DROP TABLE old_readings;
    END;
	
	START TRANSACTION;
	CREATE TEMPORARY TABLE old_readings AS (
		SELECT * FROM temp_readings WHERE time < DATE_SUB(NOW(), INTERVAL 1 MINUTE)
	);
	INSERT INTO temp_readings_historical(sensor_id, average_reading, max_reading, min_reading, start_time, end_time)
	SELECT sensor_id, AVG(sensor_reading), MAX(sensor_reading), MIN(sensor_reading), MIN(time), MAX(time) FROM temp_readings
	GROUP BY sensor_id;
	DELETE FROM temp_readings WHERE id IN (SELECT id FROM old_readings);
	SELECT * FROM temp_readings_historical;
	DROP TABLE old_readings;
	COMMIT;
END$$
DELIMITER ;

DROP EVENT store_readings;

CREATE EVENT store_readings
    ON SCHEDULE EVERY 5 SECOND
    DO
      CALL storeOldRows();