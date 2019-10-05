"""
Python Script to query the database and write them into an excel file.
Author: Sadeed Ahmad
Course: 2810ICT Software Technologies
Data Analysis and Visualisation - Trimester 2, 2019
"""


import sqlite3
import openpyxl



# read from the database "database.db" created in the first task
connection = sqlite3.connect("database.db")
cursor = connection.cursor()

# creating a new workbook
wb = openpyxl.Workbook()


# Rename the worksheet tile to ViolationTypes
sheet = wb.active
sheet.title = "ViolationTypes"


query_violations = """
SELECT  violation_code, violation_description, COUNT (violation_code) as violation_count
FROM violations
GROUP BY violation_description
ORDER BY violation_code
"""


result = cursor.execute(query_violations).fetchall()

# Setting the name of sheet columns
sheet['A1'] = "Code"
sheet['B1'] = "Description"
sheet['C1'] = "Count"

# setting the dimension of Column B as description is large than normal cell size
sheet.column_dimensions['B'].width = 100


# Writing the result from above query "query violations" into the worksheet
# Assigning the values to each of the three columns.
for index, row in enumerate(result):
    sheet["A" + str(index + 2)] = row[0]
    sheet["B" + str(index + 2)] = row[1]
    sheet["C" + str(index + 2)] = row[2]


# Saving the workbook with the name of "ViolationTypes.xlsx"
wb.save("ViolationTypes.xlsx")
connection.close()
