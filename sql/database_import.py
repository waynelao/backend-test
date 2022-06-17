# Import required modules
import csv
import sqlite3
from dateutil import parser
import pdb



# Connecting to the sqlite database
# connection = sqlite3.connect('netflix.sql')
connection = sqlite3.connect('sql/netflix.sqlite3')

# Creating a cursor object to execute
# SQL queries on a database table
cursor = connection.cursor()

# Table definition
create_table = '''CREATE TABLE netflixshows(
               showid INTEGER PRIMARY KEY AUTOINCREMENT,
               type TEXT NOT NULL, title TEXT,
               director TEXT, cast TEXT,
               country TEXT, dateadded TIMESTAMP,
               releaseyear INTEGER, rating TEXT,
               duration TEXT, listedin TEXT,
               description TEXT)
               '''

# Creating the table into our database
cursor.execute(create_table)

# SQL query to insert data into the netflixshows table
insert_records = '''
                INSERT INTO netflixshows (
                   type, title, director, 
                   cast, country, dateadded,
                   releaseyear, rating, 
                   duration, listedin, 
                   description) VALUES
                   (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                   '''

# Importing the contents of the file
# into our netflixshows table
with open("sql/netflix_titles.csv", 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    # This skips the first row of the CSV file.
    next(csvreader)
    for row in csvreader:
        if row[6]:
            row[6] = parser.parse(row[6])
        cursor.execute(insert_records, (row[1], row[2], row[3], row[4], row[5], 
                             row[6], row[7], row[8], row[9], row[10], row[11]))


# SQL query to retrieve all data from
# the netflixshows table To verify that the
# data of the csv file has been successfully
# inserted into the table
# select_all = "SELECT * FROM netflixshows"
# rows = cursor.execute(select_all).fetchall()
# index = 0

# display the first ten data points
# for row in rows:
#    print(row)
#    index += 1
#    if (index >= 10):
#        break

# Committing the changes
connection.commit()
 
# closing the database connection
connection.close()

