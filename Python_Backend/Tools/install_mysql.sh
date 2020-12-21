#!/bin/bash

sudo apt update
sudo apt upgrade -y
sudo apt install mariadb-server
sudo /etc/init.d/mysql start
sudo mysql_secure_installation
