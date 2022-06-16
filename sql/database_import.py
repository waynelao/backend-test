# Import required modules
import csv
import sqlite3

# Connecting to the sqlite database
# connection = sqlite3.connect('netflix.sql')
connection = sqlite3.connect('netflix.sqlite3')

# Creating a cursor object to execute
# SQL queries on a database table
cursor = connection.cursor()

# Table definition
create_table = '''CREATE TABLE netflixshows(
               showid TEXT PRIMARY KEY,
               type TEXT NOT NULL, title TEXT,
               director TEXT, cast TEXT,
               country TEXT, dateadded TEXT,
               releaseyear INTEGER, rating TEXT,
               duration TEXT, listedin TEXT,
               description TEXT)
               '''

# Creating the table into our database
cursor.execute(create_table)

# Opening the person-records.csv file
file = open('netflix_titles.csv')

# Reading the contents of the csv file
contents = csv.reader(file)

# SQL query to insert data into the netflixshows table
insert_records = '''
                INSERT INTO netflixshows (
                   showid, type, title, director, 
                   cast, country, dateadded,
                   releaseyear, rating, 
                   duration, listedin, 
                   description) VALUES
                   (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                   '''

# Importing the contents of the file
# into our netflixshows table
cursor.executemany(insert_records, contents)

# SQL query to retrieve all data from
# the netflixshows table To verify that the
# data of the csv file has been successfully
# inserted into the table
select_all = "SELECT * FROM netflixshows"
rows = cursor.execute(select_all).fetchall()
index = 0

# display the first ten data points
for row in rows:
    print(row)
    index += 1
    if (index >= 10):
        break

# Committing the changes
connection.commit()
 
# closing the database connection
connection.close()

