import csv
import string
from collections import OrderedDict
from operator import itemgetter
types = ['toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate']
rmvpunc = str.maketrans('','','!"#$%&()\'*+,./:;<=>?@[\]^_`{|}~')

def split_line(text, dic):
	words = text.split()
	for word in words:
		word = word.translate(rmvpunc)
		word = word.lower()
		if word in dic:
			dic[word] = dic[word] + 1
		else:
			dic[word] = 1
for index, type in enumerate(types):
	for i in range(2):
		with open('train.csv', 'r') as file:
			data = csv.reader(file)
			listofwords = {}
			if i == 1:
				filename = type + '_yes.csv'
			else:
				filename = type + '_no.csv'
			for row in data:
				if(row[index+2] == str(i)):
					split_line(row[1], listofwords)
			d= OrderedDict(sorted(listofwords.items(), key=itemgetter(1), reverse=True))
			print(listofwords)
			with open(filename, 'w') as writefile:
				writefreq = csv.writer(writefile)
				for key in d:
					writefreq.writerow((key, d[key]))
