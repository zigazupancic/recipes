import csv

with open('glavni_recepti.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)
