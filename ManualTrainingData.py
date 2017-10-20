import csv
import sys

save_line = open('line.txt', 'r')
line = int(save_line.readline())
save_line.close()
save_line = open('line.txt', 'w')
count = 0
toxicTrain = open('toxicTrain.csv', 'a')
csvToxicTrain = csv.writer(toxicTrain)
with open('messages.csv') as messages:
    csvMessages = csv.reader(messages)
    for row in csvMessages:
        print("\n" + row[3] + "\n")
        if(count >= line):
            Toxicity = input('t for toxic, n for not toxic, s for skip, q to quit: ')
            if Toxicity == 'q':
                save_line.write(str(count))
                print('Saving at line ' + str(count))
                sys.exit()
            elif Toxicity == 't':
                csvToxicTrain.writerow((row[3], 't'))
            elif Toxicity == 'n':
                csvToxicTrain.writerow((row[3], 'n'))
        count = count + 1

