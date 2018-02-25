import csv
import random
file1 = open('train.csv', 'r') 
data_reader = csv.reader(file1)
file2 = open('train1.csv', 'w')
train_writer = csv.writer(file2)
file3 = open('validation.csv', 'w')
valid_writer = csv.writer(file3)

num_valid = 12000

for row in data_reader:
	if random.randint(1,5) == 5 and num_valid > 0:
		valid_writer.writerow(row)
		num_valid -= 1
	else:
		train_writer.writerow(row)