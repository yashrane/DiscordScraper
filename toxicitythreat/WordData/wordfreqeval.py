import csv
import glob

words = []

def add_to_dic(word):
	if word not in words:
		words.append(word)
	else:
		pass

for name in glob.glob('./*.csv'):
	with open(name, 'r') as file:
		data = csv.reader(file)
		#print("{} : {}".format(name, sum(1 for row in data if int(row[1]) > 25)))
		for row in data:
			if int(row[1]) > 25:
				add_to_dic(row[0])
print(len(words), words)
with open('dictionary.csv','w') as file:
	dic = csv.writer(file)
	for word in words:
		if word != '':
			dic.writerow([word])