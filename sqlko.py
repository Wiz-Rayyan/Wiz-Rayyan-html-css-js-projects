
'''
    import pymysql

    con = pymysql.connect(host="localhost", user="root", passwd="0nbh6mysql")
    cur = con.cursor()
    cur.execute("show databases")
    for i in cur:
        print(i)
        '''
'''
import pymysql

# Connect to MySQL
con = pymysql.connect(host="localhost", user="root", passwd="0nbh6mysql")
cur = con.cursor()

# Create a new database
cur.execute("CREATE DATABASE IF NOT EXISTS my_database")

# Show databases to confirm creation
cur.execute("SHOW DATABASES")
for db in cur.fetchall():
    print(db)

# Close connection
con.close()
'''

'''
import pymysql

# Connect to MySQL and select the database
con = pymysql.connect(host="localhost", user="root", passwd="0nbh6mysql", database="my_database")
cur = con.cursor()
cur.execute("""
    CREATE TABLE IF NOT EXISTS student (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        age INT
    )
""")
con.commit()
print("Table 'student' created successfully!")
'''

'''
import pymysql

# Connect to MySQL
con = pymysql.connect(host="localhost", user="root", passwd="0nbh6mysql", database="my_database")
cur = con.cursor()

# Drop the table (if it already exists)
cur.execute("DROP TABLE IF EXISTS student")

# Create the table again with correct schema
cur.execute("""
    CREATE TABLE student (
        rollNo INT PRIMARY KEY,
        name VARCHAR(100),
        age INT
    )
""")
con.commit()
print("Table 'student' created successfully!")

# Insert data
cur.execute("INSERT INTO student (rollNo, name, age) VALUES (1, 'Alice', 22)")
cur.execute("INSERT INTO student (rollNo, name, age) VALUES (2, 'Bob', 24)")
cur.execute("INSERT INTO student (rollNo, name, age) VALUES (3, 'Charlie', 21)")
con.commit()
print("Data inserted successfully!")

# Retrieve and display data
cur.execute("SELECT * FROM student")
rows = cur.fetchall()

print("Data in student table:")
for row in rows:
    print(row)

# Close connection
con.close()
'''
'''
import pymysql
import os

# Database Connection
try:
    con = pymysql.connect(host="localhost", user="root", passwd="0nbh6mysql", database="my_database")
    cur = con.cursor()
    print("✅ Connected to database successfully!")
except Exception as e:
    print(f"❌ Database Connection Failed: {e}")
    exit()

# Function to Update Student Record (Using Correct Column Names)
def update_student(rollNo, new_name, new_father_name, new_sub, new_grade):
    try:
        cur.execute("""
            UPDATE student SET name=%s, father_name=%s, sub=%s, grade=%s WHERE rollNo=%s
        """, (new_name, new_father_name, new_sub, new_grade, rollNo))
        con.commit()
        if cur.rowcount > 0:
            print(f"✅ Student Roll No {rollNo} Updated Successfully!")
        else:
            print(f"⚠️ No record found for Roll No {rollNo}")
    except Exception as e:
        print(f"❌ Error updating record: {e}")

# Example Usage (Modify as needed)
update_student(1, "Rahul Sharma", "Mr. Sharma", "Mathematics", "A+")

# Rename `student.py` after updates
try:
    if os.path.exists("student.py"):
        os.rename("student.py", "student_backup.py")
        print("✅ student.py renamed to student_backup.py")
    else:
        print("⚠️ student.py not found!")
except Exception as e:
    print(f"❌ Error renaming file: {e}")

# Close Database Connection
try:
    cur.close()
    con.close()
    print("✅ Database connection closed successfully!")
except Exception as e:
    print(f"❌ Error closing database connection: {e}")
'''
'''
import pymysql

def setup_database():
    try:
        # Connect to MySQL (no specific DB yet)
        con = pymysql.connect(host="localhost", user="root", passwd="0nbh6mysql")
        cur = con.cursor()

        # Create database if it doesn't exist
        cur.execute("CREATE DATABASE IF NOT EXISTS my_database")
        print("Database `my_database` checked/created.")

        # Switch to our new database
        cur.execute("USE my_database")

        # Create table if it doesn't exist
        cur.execute("""
        CREATE TABLE IF NOT EXISTS student (
            rollNo INT PRIMARY KEY,
            name VARCHAR(100),
            fname VARCHAR(100),
            sub VARCHAR(100),
            grade VARCHAR(10)
        )
        """)
        print("Table `student` checked/created.")

        con.commit()
        con.close()
        print("✅ Setup completed successfully.")

    except Exception as e:
        print(f"❌ Error during setup: {e}")

if __name__ == "__main__":
    setup_database()

'''

'''
import pymysql

# Connect to MySQL
con = pymysql.connect(host="localhost", user="root", passwd="0nbh6mysql", database="my_database")
cur = con.cursor()

# Create the table with correct columns if it does not exist
cur.execute("""
    CREATE TABLE IF NOT EXISTS student (
        rollNo INT PRIMARY KEY, 
        name VARCHAR(255), 
        fname VARCHAR(255), 
        sub VARCHAR(255), 
        grade VARCHAR(10)
    )
""")

# Check if 'fname' column exists, if not, add it
cur.execute("SHOW COLUMNS FROM student")
columns = [column[0] for column in cur.fetchall()]

if "fname" not in columns:
    cur.execute("ALTER TABLE student ADD COLUMN fname VARCHAR(255)")

# Commit and close connection
con.commit()
con.close()

print("Database setup completed successfully!")
'''

import pymysql

# Connect to MySQL
con = pymysql.connect(host="localhost", user="root", passwd="0nbh6mysql", database="my_database")
cur = con.cursor()

# Create the table with correct columns if it does not exist
cur.execute("""
    CREATE TABLE IF NOT EXISTS student (
        rollNo INT PRIMARY KEY, 
        name VARCHAR(255), 
        fname VARCHAR(255), 
        sub VARCHAR(255), 
        grade VARCHAR(10)
    )
""")

# Check existing columns in 'student' table
cur.execute("SHOW COLUMNS FROM student")
columns = [column[0] for column in cur.fetchall()]

# Add missing columns dynamically
missing_columns = {
    "fname": "VARCHAR(255)",
    "sub": "VARCHAR(255)",
    "grade": "VARCHAR(10)"
}

for column, datatype in missing_columns.items():
    if column not in columns:
        cur.execute(f"ALTER TABLE student ADD COLUMN {column} {datatype}")

# Commit and close connection
con.commit()
con.close()

print("Database setup completed successfully! All required columns are now in place.")
