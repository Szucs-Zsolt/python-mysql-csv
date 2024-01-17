## Conversion of MySQL database tables into csv files

After the program connected to the database it will show its tables.
The user can select which one of them should be saved in csv format.
Each table will be written into a csv file using its own name.

# Installation
1. Cloning GitHub repository 
```
git clone https://github.com/Szucs-Zsolt/python-mysql-csv.git
```

2. Creating the virtual environment
- the program uses Python 3.9 
- the list of the necessary modules is in the requirements.txt file. (mysql-connector-python==8.2.0, numpy==1.26.2, Pillow==10.1.0, protobuf==4.21.12, six==1.16.0, wxPython==4.2.1)
```
cd python-mysql-csv
py -3.9 -m venv venv
.\venv\Scripts\activate
python -m pip install -r requirements.txt
```

3. In the .\config\mysql_connection.cfg are the necessary date to connect to the database. These are:
- First line: server IP
- Second line: name of the database 
- Third line: name of the user
- Fourth line: password

Example:
```
192.168.0.120
name_of_the_database
name_of_the_user
password
```
4. After started the program connects to the database and show its tables.
```
python main.py
```
- You can use the first column to mark the table you want to save as a csv file.
- In the second column is the name of the table.
- The Save button is at the top of the window.
- The content of each of the selected tables will be saved in a csv file with the same name.


## MySQL server used during the development process
---------------------------------------------------
- Debian: debian 6.1.0-12-amd64
- MySQL/MariaDB: mariadb  Ver 15.1 Distrib 10.11.4-MariaDB

5) Commands used to create the database in the server
-----------------------------------------------------
```
    sudo apt update
    sudo apt install mariadb-server

    sudo mysql -u root -p
	
    CREATE DATABASE test;
    SHOW DATABASES;
    CREATE TABLE test.employee (
        employee_id  INTEGER  PRIMARY KEY  AUTO_INCREMENT,
 	name VARCHAR(80),
	age INTEGER
    );
    USE test;
    SHOW TABLES;
    DESC test.employee;
	
    INSERT INTO test.employee (nev, kor) VALUES ("John Smith", 30);
    INSERT INTO test.employee (nev, kor) VALUES ("John Doe", 31);
    SELECT * FROM test.employee;

    CREATE TABLE test.fruits (
        fruit_id INTEGER  PRIMARY KEY  AUTO_INCREMENT,
	name VARCHAR(60),
	amount INTEGER);
    INSERT INTO test.fruits (nev, mennyiseg) values ("apple", 1);
    INSERT INTO test.fruits (nev, mennyiseg) values ("banana", 2);
    INSERT INTO test.fruits (nev, mennyiseg) values ("chestnuts", 3);
    SELECT *  FROM test.fruits;
```
6) Creating user with read-only rights
--------------------------------------

    CREATE USER 'test_user'@'%'   IDENTIFIED BY 'test_password';

    SELECT user,host FROM mysql.user;

    GRANT SELECT ON test.*   TO 'test_user'@'%'
    SHOW GRANTS FOR 'test_user'@'%';

    EXIT;	


7) The server configuration has beeen changed (as a default only localhost can use it)
-------------------------------------------------------------------------------
```
    sudo vim /etc/mysql/my.cnf
        [mysqld]
            bind-address = 0.0.0.0
```

Restart
```
    sudo systemctl restart mariadb
```

This configuration allows the database to be used from everywhere, so it is strongly advised to check all incoming connection for IP or MAC address.
