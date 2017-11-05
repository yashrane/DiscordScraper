import csv
import re

#parses a string to get all introduction data from it
#returns an array of introduction tuples
def get_intros(intros):
	pattern = re.compile('2.(.+)[,\/-](.+)[,\/-](.+)\s3.(.+)\s4.(.+)')
	result = pattern.findall(intros)
	if result is not None:
		return result
		
#prints introduction data to the screen and to introductions.csv
def log_to_file(intros):
	with open('introductions.csv', 'w') as f:
		csvwriter = csv.writer(f)
		for intro in intros:
			csvwriter.writerow(intro)
	

	
with open('intros.txt','r') as f:
	intros = get_intros(f.read())
	if intros is not None:
		for intro in intros:
			print(intro)
		log_to_file(intros)
	else:
		print('Something went wrong')
		
		
# with open('bad_intros.txt', 'r+') as f:
	# writer = open('introductions.csv', 'w')
	# csvwriter = csv.writer(writer)
	# for line in f:
		# csvwriter.writerow(line.lstrip())
		
		