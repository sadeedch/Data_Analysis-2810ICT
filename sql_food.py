"""
Python Scripts to Query the Database
Author: Sadeed Ahmad
Course: 2810ICT Software Technologies
Data Analysis and Visualisation - Trimester 2, 2019
"""


import sqlite3
# importing tabulate to print the data in tables.
from tabulate import tabulate


# read from the database "database.db" created in the first task
connection = sqlite3.connect("database.db")
cursor = connection.cursor()

# Database query to select the name, address, zip and city of
# those businesses which have at least one violations
# ordered alphabetically.
query_business_details = """

SELECT i.facility_name, i.facility_address, i.facility_zip, i.facility_city
FROM inspections i, violations v
WHERE i.serial_number = v.serial_number
GROUP BY i.facility_name
HAVING COUNT(DISTINCT v.serial_number) >= 1
ORDER BY i.facility_name
"""

# Executing the above query and assigning the result to result variable
result = cursor.execute(query_business_details).fetchall()


# query to create a table named previous violations
create_previous_violations = """
CREATE TABLE IF NOT EXISTS previous_violations (
    facility_name TEXT,
    facility_address TEXT,
    facility_zip TEXT,
    facility_city TEXT
)
"""
# Executing the above query
cursor.execute(create_previous_violations)


# Defining the check to see if the previous_violations table is empty.
check_previous_violations = "SELECT * FROM previous_violations"
check_previous_violations_data = cursor.execute(check_previous_violations).fetchall()

# This query will execute if the previous violations table is empty
if check_previous_violations_data == []:
    # Inserting the data into the previous_violations table with the businesses
    # which have at least 1 violations
    previous_violations_data_insert = """INSERT INTO previous_violations VALUES"""
    for row in result:
        previous_violations_data_insert +=  """("{}", "{}", "{}", "{}"), """.format(
            row[0], row[1], row[2], row[3]
        )

    previous_violations_data_insert = previous_violations_data_insert[:-2]

    cursor.execute(previous_violations_data_insert) # Executing the above data insert query
    connection.commit()

# this block of code prints the names of those businesses on console which
# have at least one violation. Python library tabulate is used here to format
# the data into nicely looking table with grid formatting.
result_data = []
for row in result:
    result_data.append([row[0]])
print(tabulate(result_data, headers=["Businesses with at least 1 violations"], tablefmt="grid"))


# Database query to select the business name and count of violations against
# that business ordered by count of violations.
query_violations_count = """
SELECT COUNT (DISTINCT v.serial_number) serial_number_count, i.facility_name 
FROM inspections i, violations v
WHERE i.serial_number = v.serial_number
GROUP BY i.facility_name
HAVING serial_number_count >= 1
ORDER BY serial_number_count DESC
"""

# Executing the above query
result_count = cursor.execute(query_violations_count)

# this block of code prints the names of those businesses on console which
# have at least one violation along with the count of violations.
# Python library tabulate is used here to format the data into nicely looking table with grid formatting.

result_count_data = []
for row in result_count:
    result_count_data.append([row[0], row[1]])

print(tabulate(result_count_data, headers=["Violations count", "Business Name"], tablefmt="grid"))

connection.close()




