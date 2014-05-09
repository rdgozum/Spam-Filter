from __future__ import division
from math import log
import os

# --- GLOBAL VARIABLES -------------------------------------------------------------------------------------------------

directory = {
			'ham':"./dataset/training/ham/",
			'spam': "./dataset/training/spam/",
			'test': "./dataset/test/",
			'ham2':"./dataset2/training/ham/",
			'spam2': "./dataset2/training/spam/",
			'test2': "./dataset2/test/"
			}

data =	{
		'spam_msg':0,
		'ham_msg':0,
		'total_msg':0,
		'spam_words':0,
		'ham_words':0
		}

word_pool = {} # word: [ham,spam]

results = {}

# --- FUNCTIONS --------------------------------------------------------------------------------------------------------

def train(directory, category):
	if category == 0:
		print "Training ham..."
	if category == 1:
		print "Training spam..."

	# get all files in directory
	for file in os.listdir(directory):
	    if file.endswith(".txt"):
	    	# open file and get content
	        filename = directory + file
	        msg = open(filename, "r+")
	        lines = msg.readlines()

	        for line in lines:
		        words = line.split(" ") # list of all words in msg
		        for word in words:
		        	learn(word, category)

			if category == 0:
				data['ham_msg'] += 1
			else:
				data['spam_msg'] += 1	

	        msg.close()

def learn(word, category):
	try:
		word_pool[word][category] += 1
	except KeyError:
		word_pool[word] = [1-category, category]
	
	if category == 0:
		data['ham_words'] += 1
	else:
		data['spam_words'] += 1

def test(directory):
	# for each file in directory, get message and test if spam or ham
	print "Testing dataset..."
	for file in os.listdir(directory):
		if file.endswith(".txt"):
			# open file and get content
			filename = directory + file
			msg = open(filename, "r+")
			lines = msg.readlines()

	        for line in lines:
		        words = line.split(" ") # list of all words in msg
		        result = categorize(words, file)

	        msg.close()

def categorize(words, file):
	k = 1
	spam_probability = data["spam_msg"]/data['total_msg']
	ham_probability = data["ham_msg"]/data['total_msg']

	p_spam = 1
	p_ham = 1

	# get p_spam and p_ham
	for word in word_pool:
		ham_value = 1
		spam_value = 1

		if word in words: #1
			spam_value *= (word_pool[word][1]+k)/(data['total_msg'])
			ham_value *= (word_pool[word][0]+k)/(data['total_msg'])

		p_spam += log(spam_value, 10)
		p_ham += log(ham_value, 10)

	# use bayes rule
	bayes = ((p_ham ** 10)*ham_probability)/((p_ham ** 10)*ham_probability + (p_spam ** 10)*spam_probability)
	if bayes < 0.5:
		ans = "ham"
	elif bayes > 0.5:
		ans = "spam"
	else:
		ans = "ham"

	# print file, ans, bayes
	results[file] = [bayes, ans]
	# print file, results[file]


# --- MAIN -------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
	dataset = raw_input("> Which dataset do you want to test? Choose 1 or 2: ")
	dataset = int(dataset)

	if dataset == 1:
		train(directory['ham'], 0)
		train(directory['spam'], 1)
		data['total_msg'] = data['spam_msg'] + data['ham_msg']
		test(directory['test'])

	elif dataset == 2:
		train(directory['ham2'], 0)
		train(directory['spam2'], 1)
		data['total_msg'] = data['spam_msg'] + data['ham_msg']
		test(directory['test2'])

	keys = results.keys()
	keys.sort()
	output = open("results/output.txt", "w")
	bayes_output = open("results/bayes_output.txt", "w")
	for key in keys:
		output.write(key + " - " + results[key][1] + "\n")
		bayes_output.write(key + " - " + str(results[key][0]) + " " + str(results[key][1]) + " \n")

	bayes_output.close()
	output.close()

	print "Done! Please run accuracy.py to test the accuracy of our results."
