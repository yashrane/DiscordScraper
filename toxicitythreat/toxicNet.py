from __future__ import unicode_literals, print_function, division
import csv
import torch
import glob
from io import open
import numpy
import string
import torch.nn as nn
from torch.autograd import Variable

#Load data
labels = ['toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate']
train = open('train.csv')
train_data = csv.reader(train)
validation = open('validation.csv')
validation_data = csv.reader(validation)
#TODO Load dictionary of common words
vocab = []
dic = open('./WordData/dictionary.csv')
dictionary = csv.reader(dic)
for row in dictionary:
	vocab.append(row[0])
word_to_ix = {word: i for i, word in enumerate(vocab)}
#character preprocessing
chars = "abcdefghijklmnopqrstuvwqyz'-"
numerals = "1234567890"
def letterToIndex(letter):
	if letter not in chars:
		if letter in numerals:
			return len(chars)
		else:
			return len(chars)+1
	return chars.find(letter)
def lineToTensor(line):
	tensor = torch.zeros(len(line), 1, 30)
	for li, letter in enumerate(line):
		tensor[li][0][letterToIndex(letter)] = 1
	return tensor

#DEEP LEARNING FUCKERY
#unk words LSTM
class characterwiseRNN(nn.Module):
	def __init__(self, input_size, embedding_size, c_hidden):
		super(characterwiseRNN, self).__init__()
		self.hidden_size = c_hidden
		self.lstm = nn.LSTM(input_size, c_hidden)
		self.output = nn.Linear(c_hidden, embedding_size)
	def forward(self, input, hidden):
		output, hidden = self.lstm(input, hidden)
		output_embed = self.output(output)
		return output_embed, hidden
	def initHidden(self):
		return (Variable(torch.zeros(1,1,self.hidden_size)),Variable(torch.zeros(1,1,self.hidden_size)))

#full sentence LSTM
class wordwiseRNN(nn.Module):
	def __init__(self, embedding_size, output_size, w_hidden):
		super(wordwiseRNN, self).__init__()
		self.hidden_size = w_hidden
		self.lstm = nn.LSTM(embedding_size,w_hidden)
		self.output = nn.Linear(w_hidden, output_size)
		self.squash = nn.Sigmoid()
	def forward(self, input, hidden):
		output, hidden = self.lstm(input, hidden)
		output_final = self.squash(self.output(output))
		return output_final, hidden
	def initHidden(self):
		return (Variable(torch.zeros(1,1,self.hidden_size)),Variable(torch.zeros(1,1,self.hidden_size)))

#known words embedding
class embeds(nn.Module):
	def __init__(self, vocab_size, embedding_size):
		super(embeds, self).__init__()
		self.embeddings = nn.Embedding(vocab_size, embedding_size)
	def forward(self, input):
		#print(input)
		embedding = self.embeddings(input)
		embedding = embedding.view((1,-1))
		return embedding

#TODO GET VOCAB SIZE
vocab_size = len(vocab)
num_characters = 30
c_hidden = 128
w_hidden = 1024
embedding_size = 200
output_size = 6
batch_size = 100


#Create models and losses
character_embedding = characterwiseRNN(num_characters, embedding_size, c_hidden)
sentence_model = wordwiseRNN(embedding_size, output_size, w_hidden)
word_in_vocab_model = embeds(vocab_size, embedding_size)
#Load save state
files = glob.glob('./*.pth')
if len(files) != 0:
	character_embedding.load_state_dict(torch.load('./character.pth'))
	sentence_model.load_state_dict(torch.load('./sentence.pth'))
	word_in_vocab_model.load_state_dict(torch.load('./embeds.pth'))

criterion = nn.MSELoss()

#Set rates of learning
learning_rate = .005
plot_every = 500 
print_every = 1000

current_loss = 0
losses = []

rmvpunc = str.maketrans('','','!"#$%&()*+,./:;<=>?@[\]^_`{|}~')
import time
def timeSince(since):
    now = time.time()
    s = now - since
    m = math.floor(s / 60)
    s -= m * 60
    return '%dm %ds' % (m, s)

def to_tensor(s):
	s = s.translate(rmvpunc)
	s = s.lower()
	words = s.split()
	tensors = []
	for word in words:
		if word in vocab:
			print(word, word_to_ix[word])
			tensors.append(word_in_vocab_model(Variable(torch.LongTensor([word_to_ix[word]]))))
		else:
			character_tensor = Variable(lineToTensor(word))
			hidden = character_embedding.initHidden()
			for i in range(character_tensor.size()[0]):
				output, hidden = character_embedding(character_tensor[i].view(1,1,-1), hidden)
			tensors.append(output)
	return tensors
def train(input, categorization_tensor,num):
	if num%batch_size == 0:
		character_embedding.zero_grad()
		sentence_model.zero_grad()
		word_in_vocab_model.zero_grad()

	hidden = sentence_model.initHidden()

	tensor_list = to_tensor(input)
	for tensor in tensor_list:
		output, hidden = sentence_model(tensor.view(1,1,-1), hidden)
	print(output)
	print(categorization_tensor)
	loss = criterion(output, categorization_tensor)
	loss.backward()
	if num%batch_size == 0:
		for p in character_embedding.parameters():
			p.data.add_(-learning_rate, p.grad.data)
		for p in sentence_model.parameters():
			p.data.add_(-learning_rate, p.grad.data)
		for p in word_in_vocab_model.parameters():
			p.data.add_(-learning_rate, p.grad.data)

	return output, loss.data[0]
iter = 1
start = time.time()
character_embedding.zero_grad()
sentence_model.zero_grad()
word_in_vocab_model.zero_grad()
for row in train_data:
	target = Variable(torch.from_numpy(numpy.array([int(row[2]),int(row[3]),int(row[4]),int(row[5]),int(row[6]),int(row[7])])).type(torch.FloatTensor))
	guess, loss = train(row[1], target, iter)
	current_loss += loss

	if iter % plot_every == 0:
		losses.append(current_loss/plot_every)
		current_loss = 0
	if iter % print_every == 0:
		print('%d %d%% (%s) %.4f %s / %s %s' % (iter, iter / len(train_data) * 100, timeSince(start), loss, row[0], guess, target))
	iter += 1
#Save the networks
torch.save(character_embedding.state_dict(), './character.pth')
torch.save(sentence_model.state_dict(), './sentence.pth')
torch.save(word_in_vocab_model.state_dict(), './embeds.pth')

#Evaluate the validation data
def is_correct(guess, target):
	correct = [0,0,0,0,0,0]
	for i in range(6):
		if((guess[i] < 0.5)^(target[i] < 0.5)) == True:
			correct[i] = 1
	return correct

total_correct = [0,0,0,0,0,0]
for row in validation_data:
	target = Variable(torch.from_numpy(numpy.array([int(row[2]),int(row[3]),int(row[4]),int(row[5]),int(row[6]),int(row[7])])).type(torch.FloatTensor))
	guess, loss = train(row[1],target, 1)
	yay = is_correct(guess, target)
	for i in range(6):
		if yay[i] == 1:
			total_correct[i] += 1


total = len(validation_data)
for i in range(6):
	print("{}: {}/{}, {}%".format(labels[i], total_correct[i], total, (total_correct/total)))
