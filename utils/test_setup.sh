#!/bin/sh

apt-get install mysql-server
mysqladmin -u root password password
mysql -u root -ppassword < ../samples/data_dump.sql
