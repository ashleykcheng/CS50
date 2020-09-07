from csv import reader, DictReader
from sys import argv

def main():
    if len(argv) != 3:
        print("Usage : python dna.py data.csv. sequence.txt")
        exit(1)

    #open first file
    with open(argv[1]) as database:
        people = reader(database)
        for row in people:
            dnarow = row
            dnarow.pop(0)
            break

    #open second file
    with open(argv[2]) as txt:
        dnareader = reader(txt)
        for row in dnareader:
            dnalist = row

    #string
    sequence = dnalist[0]
    #dictionary
    sequences = {}


    #transfer from txt to arrary
    for item in dnarow:
        sequences[item] = 1


    for key in sequences:
        l = len(key)
        Maxlength = 0
        x = 0
        for i in range(len(sequence)):
            #avoid recounting sequence
            while x > 0:
                x -= 1
                continue

            #if match add one
            if sequence[i: i + l] == key:
                while sequence[i - l: i] == sequence[i: i + l]:
                    x += 1
                    i += l

                if x > Maxlength:
                    Maxlength = x

        sequences[key] += Maxlength

    #compare database with array
    with open(argv[1], newline='') as database:
        people = DictReader(database)
        for person in people:
            match = 0

            #add match every time new sequence
            for sequence in sequences:
                if sequences[sequence] == int(person[sequence]):
                    match += 1
            if match == len(sequences):
                print(person['name'])
                exit()

        print("No match")

main()