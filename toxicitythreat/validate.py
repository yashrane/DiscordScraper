from __future__ import unicode_literals, print_function, division
import csv
import torch
import glob
from io import open
import numpy
import string
import torch.nn as nn
from torch.autograd import Variable
import math

#Load data
labels = ['toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate']
train = open('train.csv')
train_data = csv.reader(train)
validation = open('validation2.csv')
validation_data = csv.reader(validation)
file = open('validation_results.csv', 'a')
wfile = csv.writer(file)
#TODO Load dictionary of common words
vocab = []
dic = open('./WordData/dictionary.csv')
dictionary = csv.reader(dic)
for row in dictionary:
	vocab.append(row[0])
word_to_ix = {word: i for i, word in enumerate(vocab)}
#character preprocessing
chars = "abcdefghijklmnopqrstuvwqyz-"
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
		self.lstm = nn.LSTM(input_size, c_hidden,2)
		self.output = nn.Linear(c_hidden, embedding_size)
	def forward(self, input, hidden):
		output, hidden = self.lstm(input, hidden)
		output_embed = self.output(output)
		return output_embed, hidden
	def initHidden(self):
		return (Variable(torch.zeros(2,1,self.hidden_size)),Variable(torch.zeros(2,1,self.hidden_size)))

#full sentence LSTM
class wordwiseRNN(nn.Module):
	def __init__(self, embedding_size, output_size, w_hidden):
		super(wordwiseRNN, self).__init__()
		self.hidden_size = w_hidden
		self.lstm = nn.LSTM(embedding_size,w_hidden,2)
		self.result = nn.Linear(w_hidden, output_size)
		self.squash = nn.LogSoftmax(dim=1)
	def forward(self, input, hidden):
		output, hidden = self.lstm(input, hidden)
		output = self.result(output).view(-1,2)
		output_final = self.squash(output)
		return output_final, hidden
	def initHidden(self):
		return (Variable(torch.zeros(2,1,self.hidden_size)),Variable(torch.zeros(2,1,self.hidden_size)))

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
w_hidden = 512
embedding_size = 128
output_size = 12
batch_size = 50


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
	print('loaded')


#Set rates of learning
learning_rate = .005
#plot_every = 50 
print_every = 10

current_loss = 0
losses = []

rmvpunc = str.maketrans('','','!"#$%\'&()*+,./:;<=>?@[\]^_`{|}~')
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
			tensors.append(word_in_vocab_model(Variable(torch.LongTensor([word_to_ix[word]]))))
		else:
			character_tensor = Variable(lineToTensor(word))
			hidden = character_embedding.initHidden()
			for i in range(character_tensor.size()[0]):
				output, hidden = character_embedding(character_tensor[i].view(1,1,-1), hidden)
			tensors.append(output)
	return tensors
def calc(input, categorization_tensor,num):

	hidden = sentence_model.initHidden()

	tensor_list = to_tensor(input)
	for tensor in tensor_list:
		output, hidden = sentence_model(tensor.view(1,1,-1), hidden)
	# print(output)
	# print(categorization_tensor)
	return output


iter = 1
start = time.time()

def toxic(target):
	return 1 if 1 in target else 0
for row in validation_data:
	target = Variable(torch.from_numpy(numpy.array([int(row[2]),int(row[3]),int(row[4]),int(row[5]),int(row[6]),int(row[7])])).type(torch.LongTensor))
	guess = calc(row[1], target, iter)
	wfile.writerow((toxic(target), guess[0][1].item()))

	# if iter % plot_every == 0:
	# 	losses.append(current_loss/plot_every)
	# 	current_loss = 0
	if iter % print_every == 0:
		print('%d %d%% (%s)\n%s \n%s %s' % (iter, iter / 100000 * 100, timeSince(start), row[1], guess, target))
	iter += 1
# def get_rank(elem):
# 	return elem[1]
# guesses.sort(key = get_rank, reverse=True)
# #Evaluate the validation data

# P = sum(toxic(pair) for pair in guesses)
# p = P
# N = sum(abs(toxic(pair)-1) for pair in guesses)
# n = N
# area = 0
# for pair in guesses:
# 	is_toxic = pair[0]
# 	if is_toxic == 1: 
# 		area += n
# 	elif is_toxic == 0:
# 		n-=1
# ROC = area/(P*N)
# print(ROC)