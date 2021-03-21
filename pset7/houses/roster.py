from cs50 import SQL
from sys import argv, exit

db = SQL("sqlite:///students.db")

if len(argv) != 2:
    print("Error")
    exit(1)

students = db.execute(f"SELECT first, middle, last, birth FROM students WHERE house = '{argv[1]}' ORDER BY last, first")

for row in students:

    first = row["first"]
    middle = row["middle"]
    last = row["last"]
    birth = row["birth"]

    if middle == None:
        print(f"{first} {last}, born {birth}")

    else:
        print(f"{first} {middle} {last}, born {birth}")
