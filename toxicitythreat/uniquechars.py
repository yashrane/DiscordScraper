file = open('train_copy.csv')
text = file.read()
u_chars = {}
for char in text:
	if char in u_chars:
		pass
	else:
		u_chars[char] = 1

file = open('test.csv')
text = file.read()
u_chars_v = {}
for char in text:
	if char in u_chars_v:
		pass
	else:
		u_chars_v[char] = 1

overlap = []
for char in u_chars.keys():
	if char in u_chars_v:
		pass
	else:
		overlap.append(char)
print('unique to train_copy')
print(overlap)

overlap = []
for char in u_chars_v.keys():
	if char in u_chars:
		pass
	else:
		overlap.append(char)
print('unique to test')
print(overlap)