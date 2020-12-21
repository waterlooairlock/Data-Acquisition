
DROP DATABASE IF EXISTS watlock;
CREATE DATABASE IF NOT EXISTS watlock;

CREATE USER IF NOT EXISTS 'watlock_user'@'localhost' IDENTIFIED BY 'elon_gated_musk_rat';
GRANT ALL PRIVILEGES ON watlock.* TO 'watlock_user'@'localhost';

FLUSH PRIVILEGES;
