import csv
import string
from collections import OrderedDict
from operator import itemgetter
rmvpunc = str.maketrans('','','.,")(}{][/?><~=+-_;:!@#$%^&`*')

def split_line(text, dic):
	words = text.split()
	for word in words:
		if ((word[0] != '<' or word[-1] != '>') and len(word) < 15 and word[0] != '@'):
			word = word.translate(rmvpunc)
			word = word.lower()
			if word in dic:
				dic[word] = dic[word] + 1
			else:
				dic[word] = 1

listofwords = {}
messages = open('messages.csv')
csvMessages = csv.reader(messages)
for row in csvMessages:
	split_line(row[3], listofwords)

d= OrderedDict(sorted(listofwords.items(), key=itemgetter(1), reverse=True))
wordfreq = open('wordFreq.csv', 'w')
csvwordfreq = csv.writer(wordfreq)
for key in d:
	csvwordfreq.writerow((key, d[key]))
