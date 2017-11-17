import csv
import sys

nonToxic = open('nonToxic.csv','w')
csvNonToxic = csv.writer(nonToxic)
toxic = open('toxic.csv','w')
csvToxic = csv.writer(toxic)

with open('toxicTrain.csv',encoding="latin-1") as f:
    message = csv.reader(f)
    for row in message:
        if row[1] == 'n':
            csvNonToxic.writerow((row[0],'n'))
        elif row[1] == 't':
            csvToxic.writerow((row[0],'t'))
