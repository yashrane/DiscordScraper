import csv

file = open('train.csv')
write = open('train_d.csv', 'w')
data = csv.reader(file)
writefile = csv.writer(write)
for row in data:
	writefile.writerow(row)
	for i in range(2,8):
		if row[i] == '1':
			writefile.writerow(row)

