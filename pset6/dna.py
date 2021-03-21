from sys import argv, exit
import csv

def result(sequence, dna):
    MAX = 0
    for i in range(len(dna)):
        repeated = 0

        while (str(dna[i: i + len(sequence)]) == sequence):
            repeated +=1
            i += len(sequence)

        if repeated > MAX:
            MAX = repeated

    return MAX

if len(argv) != 3:
    print("Usage: python dna.py data.csv sequence.txt")
    exit(1)

with open(argv[1]) as csvfile:
    reader = csv.reader(csvfile)

    sequenceDict = {}
    dnaList = []

    for row in reader:
        sequenceDict[row[0]] = row[1:]

f = open(argv[2], 'r')
n = f.read()

shortTandemRepeat = sequenceDict["name"]

for i in shortTandemRepeat:
    tmpSequence = result(i, n)
    dnaList.append(str(tmpSequence))

for i in sequenceDict:
    if dnaList == sequenceDict[i]:
        print(i)
        exit()

print("No Match")
