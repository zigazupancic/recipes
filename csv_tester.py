import csv

with open('glavni_recepti.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        print(len(row))
        if len(row) > 0:
            print(row[0])

with open('razne_mere.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)
        print(len(row))
