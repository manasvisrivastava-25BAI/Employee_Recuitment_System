### EMPLOYEE RECRUITMENT SYSTEM

#### 

##### Purpose

This program automates the recruitment process for both employers (admins) and candidates. It allows users to register, view job vacancies, update details, and schedule interviews using a simple command-line interface connected to a MySQL database.



##### System Requirements

###### Software

* Python 3.7 or later
* MySQL 8.0 or later
* mysql-connector-python module

###### Hardware

* Minimum 512 MB RAM
* 1 GB Disk Space
* Windows 10/11 OS recommended



##### Required Installation

1. Install Python from [https://www.python.org./downloads/](https://www.python.org./downloads/)
2. Install MySQL and set up the root password.
3. Open Command Prompt and install the MySQL connector: **pip install mysql-connector-python**



##### How to set up the database

1. Open MySQL Workbench or MySQL Command line.
2. No manual setup is needed - the Python code automatically creates the database '**EMP\_RECUIT**' and its tables when you run it the first time.



##### How to run the program

1. Save the python file as recruitment\_system.py
2. Open Command prompt or VS code terminal
3. Navigate to the folder where the file is saved
4. Run the program with the command: python recruitment\_system.py



##### How to use the system

1. ###### Choose role



When the program starts, it will ask:

**"Are you an Admin or Candidate? (admin/candidate)"**

Type 'admin' if you are an employer or 'candidate' if you are a job seeker



###### 2\. Login or signup



If your ID and password exists, you'll log in automatically

Otherwise, the system will ask if you want to sign up with those credentials.

Type 'yes' to create a new account



###### 3\. Admin Options



1. **Add vacancy details**
2. **Check list of candidates**
3. **Back** 
4. **Exit**



###### Candidate Options

1. **Add Candidate Details**
2. **Update Details**
3. **View vacancy**
4. **Check interview status**
5. **Back**
6. **Exit**



##### Sample execution flow

* Run program
* Choose 'candidate'
* Enter candidate id and password
* Sign up if new
* Add candidate details (name, DOB, degree, experience, etc)
* View available vacancies
* Check interview status



##### Common errors and solution

**Error** : "mysql.connector not found

**Fix** : run "pip install mysql-connector-python



**Error** : "Access denied for user 'root'@'localhost'"

**Fix** : check your MySQL username and password in the connect() function.



**Error** : "Incorrect date format"

**Fix** : use YYYY-MM-DD format (e.g. 2025-10-27)



##### Closing note

The EMPLOYEE RECRUITMENT SYSTEM is designed for easy execution and clear database integration. It can be expanded by adding GUI or web-based interfaces in the future.





