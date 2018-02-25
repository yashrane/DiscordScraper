from __future__ import unicode_literals, print_function, division
import csv
import torch
from io import open
import glob
import numpy
import string
import torch.nn as nn
from torch.autograd import Variable

train = open('train.csv')
train_data = csv.reader(train)
validation = open('validation.csv')
validation_data = csv.reader(validation)

chars = "abcdefghijklmnopqrstuvwqyz'-"
numerals = "1234567890"
def letterToIndex(letter):
	if letter not in chars:
		if letter in numerals:
			return len(chars)
		else:
			return len(chars)+1
	return all_letters.find(letter)
def lineToTensor(line):
	tensor = torch.zeros(len(line), 1, n_letters)
	for li, letter in enumerate(line):
		tensor[li][0][letterToIndex(letter)] = 1
	return tensor

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

num_characters = 30
c_hidden = 128
w_hidden = 1024
embedding_size = 200
output_size = 6
batch_size = 100
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

class embeds(nn.Module):
	def __init__(self, vocab_size, embedding_size):
		super(embeds, self).__init__()
		self.embeddings = nn.Embedding(vocab_size, embedding_size)
	def forward(self, input):
		embedding = self.embeddings(input).view((1,-1))
		return embedding

#TODO GET VOCAB SIZE

character_embedding = characterwiseRNN(num_characters, embedding_size, c_hidden)
sentence_model = wordwiseRNN(embedding_size, output_size, w_hidden)
word_in_vocab_model = embeds(vocab_size, embedding_size)

criterion = nn.MSELoss()
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
			tensors.append(word_in_vocab_model(Variable(torch.LongTensor(word_to_ix[w]))))
		else:
			character_tensor = Variable(lineToTensor(word))
			hidden = character_embedding.initHidden()
			for i in range(character_tensor.size()[0]):
				output, hidden = characterwiseRNN(character_tensor[i].view(1,1,-1), hidden)
			tensors.append(output)
	return tensors
def train(input, categorization_tensor):
	character_embedding.zero_grad()
	sentence_model.zero_grad()
	word_in_vocab_model.zero_grad()

	hidden = sentence_model.initHidden()

	tensor_list = to_tensor(input)
	for tensor in tensor_list:
		output, hidden = sentence_model(tensor.view(1,1,-1), hidden)
	loss = criterion(output, categorization_tensor)
	loss.backward()

	for p in character_embedding.parameters():
		p.data.add_(-learning_rate, p.grad.data)
	for p in sentence_model.parameters():
		p.data.add_(-learning_rate, p.grad.data)
	for p in word_in_vocab_model.parameters():
		p.data.add_(-learning_rate, p.grad.data)

	return output, loss.data[0]
iter = 1
start = time.time()
for row in train_data:
	target = torch.from_numpy(numpy.array(row[1],row[2],row[3],row[4],row[5],row[6]))
	guess, loss = train(row[0])
	current_loss += loss

	if iter % plot_every == 0:
		losses.append(current_loss/plot_every)
		current_loss = 0
	if iter % print_every == 0:
		print('%d %d%% (%s) %.4f %s / %s %s' % (iter, iter / len(train_data) * 100, timeSince(start), loss, row[0], guess, target))
	iter += 1


is_correct(guess, target):


for row in validation_data:
	target = torch.from_numpy(numpy.array(row[1],row[2],row[3],row[4],row[5],row[6]))
	guess, loss = train(row[0])
	yay = is_correct(guess, target)
