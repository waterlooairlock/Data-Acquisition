-- This was written by Austin W. Milne, He has no idea what he is doing.

SET sql_mode = '';

CREATE TABLE IF NOT EXISTS sensor_readings (
    id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    arduino_name CHAR(30),
    sensor_type CHAR(30),
    sensor_id INT,
    reading FLOAT,
    time timestamp
)
