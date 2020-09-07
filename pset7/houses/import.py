from csv import reader
from sys import argv
from cs50 import SQL


db = SQL("sqlite:///students.db")

#python import.py characters.csv
def main():
    if len(argv) != 2:
        print("Usage : python import.py characters.csv")
        exit(1)

    #open first file
    with open(argv[1], newline='') as file:
        reader1 = reader(file)
        for character in reader1:
            if character[0] == 'name':
                continue

            #split name
            charactername = character[0].split()


            if len(charactername) < 3:
                db.execute("insert into students(first, middle, last, house, birth) values (?, ?, ?, ?, ?)",
                           charactername[0], None, charactername[1], character[1], character[2])

            if len(charactername) == 3:
                db.execute("insert into students(first, middle, last, house, birth) values (?, ?, ?, ?, ?)",
                           charactername[0], charactername[1], charactername[2], character[1], character[2])

main()