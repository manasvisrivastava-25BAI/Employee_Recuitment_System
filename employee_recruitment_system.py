import mysql.connector as m 
import datetime
import time
import os
import sys

# Connect to MySQL server
mydb = m.connect(host='localhost', user='root', passwd='admin')
c = mydb.cursor()

# Create the EMP_RECRUIT database
c.execute("CREATE DATABASE IF NOT EXISTS EMP_RECRUIT")
mydb.close()

# Connect to the EMP_RECRUIT database
d = m.connect(host='localhost', user='root', passwd='admin', database='EMP_RECRUIT')
C = d.cursor()

# Create LOGIN/SIGNUP Table for Admin
C.execute("""CREATE TABLE IF NOT EXISTS loginad (
    adminid INT PRIMARY KEY,
    pass VARCHAR(255) NOT NULL)""")

# Create LOGIN/SIGNUP Table for Candidate
C.execute("""CREATE TABLE IF NOT EXISTS logincd (
    candid INT PRIMARY KEY,
    pass VARCHAR(255) NOT NULL)""")
# Create the vacancies table
C.execute("""CREATE TABLE IF NOT EXISTS vacancies(
    vacid INT PRIMARY KEY,
    org_name VARCHAR(30) NOT NULL,
    post VARCHAR(30) NOT NULL,
    min_exp VARCHAR(30) NOT NULL,
    max_salary DECIMAL(10,2) NOT NULL)""")
# Create the candidate table with a foreign key referencing the vacancies table
C.execute("""CREATE TABLE IF NOT EXISTS candidate (
 candid INT PRIMARY KEY,
 candname VARCHAR(30) NOT NULL,
 gender VARCHAR(30) NOT NULL,
 birthdate DATE NOT NULL,
 state VARCHAR(30) NOT NULL,
 university VARCHAR(100) NOT NULL,
 branch VARCHAR(50) NOT NULL,
 degree VARCHAR(50) NOT NULL,
 experience VARCHAR(30) NOT NULL,
 status VARCHAR(100) NOT NULL,
 vacid INT,
 idate DATE,
 iloc CHAR(100),
 FOREIGN KEY (vacid) REFERENCES vacancies(vacid))""")
d.close()
# Establishing the connection
d = m.connect(host='localhost', user='root', passwd='admin', database='EMP_RECRUIT')
C = d.cursor()

# Clear screen function
def clear_screen():
    time.sleep(2)  # Pause for 2 seconds before clearing the screen
    os.system('cls' if os.name == 'nt' else 'clear')

# LOGIN Functions
def admin_login(C, d):
    adminid = input("Enter Admin ID: ")
    password = input("Enter Password: ")
    query1 = "SELECT * FROM loginad WHERE adminid = %s AND pass = %s"
    C.execute(query1, (adminid, password))
    result = C.fetchone()
    if result:
        print("Admin login successful!")
        clear_screen()
        admin(C, d)
    else:
        print("Login failed. Invalid Admin ID or Password.")
        yn = input("Do you want to sign up with these credentials? (YES/NO): ")
        if yn.lower() == "yes":
            query2 = "INSERT INTO loginad (adminid, pass) VALUES (%s, %s)"
            C.execute(query2, (adminid, password))
            d.commit()
            print("You have successfully signed up. Please login again.")
            clear_screen()
            admin_login(C, d)
        else:
            clear_screen()
            main_program()

def candidate_login(C, d):
    candid = input("Enter Candidate ID: ")
    password = input("Enter Password: ")

    query3 = "SELECT * FROM logincd WHERE candid = %s AND pass = %s"
    C.execute(query3, (candid, password))
    result = C.fetchone()

    if result:
        print("Candidate login successful!")
        clear_screen()
        candidate(C, d, candid)
    else:
        print("Login failed. Invalid Candidate ID or Password.")
        yn = input("Do you want to sign up with these credentials? (YES/NO): ")
        if yn.lower() == "yes":
            query4 = "INSERT INTO logincd (candid, pass) VALUES (%s, %s)"
            C.execute(query4, (candid, password))
            d.commit()
            print("You have successfully signed up. Please login again.")
            clear_screen()
            candidate_login(C, d)
        else:
            clear_screen()
            main_program()
# Admin Function
def admin(C, d):
    print("{:>60}".format("-->>ADMIN PAGE<<--"))
    while True:
        x = int(input("""Choose the following options:
1. Add Vacancy Details
2. Check List of Candidates
3. Back
4. Exit
Enter your option (1/2/3/4): """))
        print(f"User selected option: {x}")
        if x == 1:
            vacancy_details(C, d)
        elif x == 2:
            loc_details(C, d)
        elif x == 3:
            clear_screen()
            main_program()
        elif x == 4:
            print("Thank You for Using Employee Recruitment System!!!")
            d.close()  
            time.sleep(3)
            sys.exit()
        else:
            print("Invalid Entry. Please Try Again")
            clear_screen()
# Candidate Function
def candidate(C, d, candid):
    print("{:>60}".format("-->>CANDIDATE PAGE<<--"))
    while True:
        x = int(input("""Choose the following options:
1. Add Candidate Details
2. Update Details
3. View Vacancies
4. Check Interview Status
5. Back
6. Exit
Enter your option (1/2/3/4/5/6): """))
        if x == 1:
            cand_details(C, d, candid)
        elif x == 2:
            update_details(C, d, candid)
        elif x == 3:
            post = input("Enter your post: ")
            exp = input("Enter your experience: ")
            query5 = "SELECT * FROM vacancies WHERE post = %s AND min_exp <= %s"
            C.execute(query5, (post, exp))
            result = C.fetchall()
            if not result:
                print("No vacancies available")
            for row in result:
                print("Vacancy ID:",row[0])
                print("Name of Organization:",row[1])
                print("Post:",row[2])
                print("Minimum Experience:",row[3])
                print("Maximum Salary:",row[4])
            clear_screen()
        elif x == 4:
            query6 = "SELECT status, idate, vacid, iloc FROM candidate WHERE candid = %s"
            C.execute(query6, (candid,))
            result = C.fetchone()
            if result and result[0] == "Chosen for Interview":
                print("Congratulations! You are selected for the Interview")
                print(f"Your interview is on {result[1]}")
                print(f"Interview Location is at {result[3]}")
                query7 = "SELECT * FROM vacancies WHERE vacid = %s"
                C.execute(query7, (result[2],))
                vac_info = C.fetchone()
                vacid, org, post, minexp, maxsal = vac_info
                print("Interview for post:")
                print("Vacancy ID:", vacid)
                print("Name of Organization/Company:", org)
                print("Post:", post)
                print("Minimum Experience Required:", minexp)
                print("Maximum Salary:", maxsal)
                print("\n")
                time.sleep(4)
                clear_screen()
            else:
                print("You are not yet chosen for an interview.")
                clear_screen()
        elif x == 5:
            clear_screen()
            main_program()
        elif x == 6:
            print("Thank You for Using Employee Recruitment System!!!")
            d.close()  
            time.sleep(3)
            sys.exit()
        else:
            print("Invalid Choice")
            clear_screen()
# Function to check if DATE format is valid
def parse_date(date_str):
    try:
        return datetime.date.fromisoformat(date_str)
    except ValueError:
        print("Incorrect format for date. Please enter in this format (YYYY-MM-DD)")
        new_date = input("Enter Date: ")
        return parse_date(new_date)

# Function to check if Candidate ID exists
def candid_check(C, candid):
    C.execute("SELECT * FROM candidate WHERE candid = %s", (candid,))
    if C.fetchone():
        return True
    return False
# Function to check if Vacancy ID exists
def vacid_check(C, vacid):
    C.execute("SELECT * FROM vacancies WHERE vacid = %s", (vacid,))
    if C.fetchone():
        return True
    return False
# Function to add candidate details
def cand_details(C, d, candid):
    print("{:>60}".format("-->>Candidate Details<<--"))
    if candid_check(C, candid):
        print("Candidate Id already exists. You can only update your details.")
        x = input("Do you want to update your details? YES/NO: ")
        if x.lower() == "yes":
            update_details(C, d, candid)
        else:
            clear_screen()
            candidate(C, d, candid)
    else:
        p = input("Enter Candidate Name: ")
        g = input("Enter Gender: ")
        while g.lower() not in ["male", "female"]:
            print("Invalid Gender")
            g = input("Enter Gender: ")

        bd = input("Enter Date of Birth: ")
        bd = parse_date(bd)
        s = input("Enter State: ")
        u = input("Enter University of Highest Degree: ")
        br = input("Enter Branch: ")
        dg = input("Enter the highest degree you achieved: ")
        exp = input("Enter Years of Experience: ")

        query8 = """INSERT INTO candidate 
(candid, candname, gender, birthdate, state, university, branch, degree, experience, status) 
 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 'Applied')"""
        C.execute(query8, (candid, p, g, bd, s, u, br, dg, exp))
        d.commit()
        print("Details added successfully.")
        clear_screen()
        candidate(C, d, candid)
# Function to update candidate details
def update_details(C, d, candid):
    print("{:>60}".format("-->>Update Candidate Details<<--"))
    nd = int(input("Enter the number of details to be changed: "))
    for i in range(nd):
        xd = input("Enter Detail to be changed (state/university/branch/degree/experience): ")
        newd = input("Enter New Detail: ")
        query9 = f"UPDATE candidate SET {xd.lower()} = %s WHERE candid = %s"
        C.execute(query9, (newd, candid))
        d.commit()
    print("Successfully Updated")
    clear_screen()
    candidate(C, d, candid)
# Function to add vacancy details
def vacancy_details(C, d):
    print("{:>60}".format("-->>Add Vacancy Details<<--"))
    vacid = int(input("Enter Vacancy ID: "))
    if vacid_check(C, vacid):
        print("Vacancy ID already exists.")
    else:
        org_name = input("Enter Organization Name: ")
        post = input("Enter Post: ")
        min_exp = input("Enter Minimum Experience: ")
        max_salary = float(input("Enter Maximum Salary: "))
        query9 = """INSERT INTO vacancies (vacid, org_name, post, min_exp, max_salary) VALUES (%s, %s, %s, %s, %s)"""
        C.execute(query9, (vacid, org_name, post, min_exp, max_salary))
        d.commit()
        print("Vacancy details added successfully.")
    clear_screen()
    admin(C, d)
# Function to check candidate details
def loc_details(C, d):
    branch = input("Enter Branch: ")
    degree = input("Enter Required Degree (e.g., B.Sc): ").lower()
    exp = input("Enter Experience: ")

    degree_hierarchy = ["b.sc", "b.tech", "b.ba", "ba", "b.e", "m.ba", "ma", "m.sc", "m.tech", "m.e", "ph.d"]

    if degree in degree_hierarchy:
        degree_index = degree_hierarchy.index(degree)
        higher_degrees = tuple(degree_hierarchy[degree_index:])
    else:
        print("Invalid Degree. Try Again")
        return loc_details(C, d)

    try:
        #Correct query using dynamic placeholders for tuple
        placeholders = ','.join(['%s'] * len(higher_degrees))
        query11 = f"""SELECT * FROM candidate 
                      WHERE branch = %s 
                      AND degree IN ({placeholders}) 
                      AND experience >= %s"""
        params = (branch, *higher_degrees, exp)
        C.execute(query11, params)
        result = C.fetchall()

        if not result:
            print("No candidate with the above-mentioned qualifications is available.")
            yn = input("Do you want to check with other qualifications? (Yes/No): ")
            if yn.lower() == "yes":
                loc_details(C, d)
            else:
                return admin(C, d)
        else:
            m = 1
            for i in result:
                print("Candidate No:", m)
                print("Candidate ID:", i[0])
                print("Candidate Name:", i[1])
                print("State:", i[4])
                print("University:", i[5])
                print("Post:", i[6])
                print("Degree:", i[7])
                print("Experience(years):", i[8])
                m += 1
                print("\n")

            n = int(input("Enter the number of vacancies: "))
            for i in range(n):
                x = input("Enter Candidate ID: ")
                v = input("Enter Vacancy ID: ")
                idate = input("Enter the interview date in format (YYYY-MM-DD): ")
                idate = parse_date(idate)
                iloc = input("Enter Interview Location: ")

                query12 = "UPDATE candidate SET status = %s WHERE candid = %s"
                query13 = "UPDATE candidate SET vacid = %s WHERE candid = %s"
                query14 = "UPDATE candidate SET idate = %s WHERE candid = %s"
                query15 = "UPDATE candidate SET iloc = %s WHERE candid = %s"

                C.execute(query12, ("Chosen for Interview", x))
                C.execute(query13, (v, x))
                C.execute(query14, (idate, x))
                C.execute(query15, (iloc, x))
                print("Successfully Updated!")
        d.commit()
        clear_screen()
        admin(C, d)

    except Exception as e:
        print("Error executing query:", e)

def main_program():
    print("{:>60}".format("-->>WELCOME TO EMPLOYEE RECRUITMENT SYSTEM<<--"))
    while True:
        role = input("Are you an Admin or Candidate? (admin/candidate): ").lower()
        if role == 'admin':
            admin_login(C, d)
        elif role == 'candidate':
            candidate_login(C, d)
        else:
            print("Invalid role. Please try again.")
            clear_screen()
# Start the program
main_program()
