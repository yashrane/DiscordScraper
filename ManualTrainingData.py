import csv
import sys

save_line = open('line.txt', 'r')
line = int(save_line.readline())
save_line.close()
save_line = open('line.txt', 'w')
count = 0
toxicTrain = open('toxicTrain.csv', 'a')
csvToxicTrain = csv.writer(toxicTrain)
while True:
    messages = open('messages.csv')
    csvMessages = csv.reader(messages)
    for row in csvMessages:
        if(count >= line):
            print("\n>>\t" + row[3] + "\n")
            Toxicity = input('t for toxic, n for not toxic, u to undo, s for skip, q to quit: ')
            if Toxicity == 'q':
                save_line.write(str(count))
                print('Saving at line ' + str(count))
                sys.exit()
            elif Toxicity == 't':
                csvToxicTrain.writerow((row[3], 't'))
            elif Toxicity == 'n':
                csvToxicTrain.writerow((row[3], 'n'))
            elif Toxicity == 'u':
                line = count - 1
                count = 0
                toxicTrain.close()
                #Rewrite the file such that the last line is popped
                f = open('toxicTrain.csv', 'r')
                lines = f.readlines()
                lines = lines[:-1]
                f.close()
                f = open('toxicTrain.csv', 'w')
                for lin in lines:
                    f.write(lin)
                f.close()
                #Reopen file so that it can be appended to from the undoed line
                toxicTrain = open('toxicTrain.csv', 'a')
                csvToxicTrain = csv.writer(toxicTrain)
                messages.close()
                break
        
        count = count + 1
    if(Toxicity != 'u'):
        break
