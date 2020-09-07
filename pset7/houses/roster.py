from csv import reader, DictReader
from sys import argv
from cs50 import SQL


db = SQL("sqlite:///students.db")

def main():
    if len(argv) != 2:
        print("Usage : python roster.py [House Name]")
        exit(1)

    students = db.execute("select * from students where house = (?) order by last", argv[1])

    for student in students:

        if student['middle'] != None:
            print(f"{student['first']} {student['middle']} {student['last']}, born {student['birth']}")
        else:
            print(f"{student['first']} {student['last']}, born {student['birth']}")

main()
