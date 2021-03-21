import csv
from sys import argv, exit
from cs50 import SQL

if len(argv) != 2:
    print("Error")
    exit(1)

db = SQL("sqlite:///students.db")

with open(argv[1], "r") as file:
    reader = csv.DictReader(file)

    for row in reader:

        name = row["name"]
        n = name.split()

        if len(n) == 2:

            first = n[0]
            last = n[1]

            db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES (?,?,?,?,?)", first, None, last, row["house"], row["birth"])

        elif len(n) == 3:
            first = n[0]
            middle = n[1]
            last = n[2]

            db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES (?,?,?,?,?)", first, middle, last, row["house"], row["birth"])
