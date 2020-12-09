# create DB
create database db_finance;

# create user
GRANT ALL ON *.* to 'finance'@'%' IDENTIFIED BY 'pwforfinance';

FLUSH PRIVILEGES;

