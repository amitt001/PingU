#!/bin/bash

echo "Starting python package installation..."
pip install -r requirements.txt


# check mysql is present
FAILMSG="MySQL not present. Install MySQL with sudo apt-get/yum install mysql-server"
sudo service mysql status >/dev/null 2>&1 && echo "Check MySQL: Done" || echo $FAILMSG

#create database
echo "Creating database. Enter password when prompted for."
echo "create database msgapp" | mysql -u root -p

echo "Starting app..."
python app.py