import csv
import sys

prevOpt = 'x'
save_line = open('line1.txt', 'r')
line = int(save_line.readline())
countWords = int(save_line.readline())
save_line.close()
save_line = open('line1.txt', 'w')
count = 0
topWords = open('topWords.csv', 'a')
csvTopWords = csv.writer(topWords)
while countWords < 2001:
    wordFreq = open('wordFreq.csv')
    csvWordFreq = csv.reader(wordFreq)
    for row in csvWordFreq:
        if(count >= line):
            print("\n>>\t" + row[0] + "\n")
            keep = input('t for high frequency word to keep, u to undo, s for skip, q to quit: ')
            if keep == 'q':
                save_line.write(str(count)+'\n')
                print('Saving at line ' + str(count))
                save_line.write(str(countWords))
                print('Saved ' + str(countWords) + ' words to dictionary')
                sys.exit()
            elif keep == 't':
                csvTopWords.writerow((row[0],row[1]))
                countWords = countWords + 1
            elif keep == 'u':
                line = count - 1
                count = 0
                if(countWords > 0 and prevOpt == 't'):
                    countWords = countWords - 1
                    topWords.close()
                    #Rewrite the file such that the last line is popped
                    f = open('topWords.csv', 'r')
                    lines = f.readlines()
                    lines = lines[:-1]
                    f.close()
                    f = open('topWords.csv', 'w')
                    for lin in lines:
                        f.write(lin)
                    f.close()
                    #Reopen file so that it can be appended to from the undoed line
                    topWords = open('topWords.csv', 'a')
                    csvTopWords = csv.writer(topWords)
                wordFreq.close()
                break
            prevOpt = keep;
        count = count + 1
    if(keep != 'u'):
        break
