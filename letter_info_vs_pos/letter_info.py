
import re
import pdb
from collections import Counter
import math
from joblib import Parallel, delayed
import itertools
import time
import pickle
import csv
import itertools
from nltk.corpus import brown
from random import shuffle
from nltk.util import ngrams

def main(n):
	'''input: 
			n: the number of loop through every first word, determine how surprising each set of words is.  Then determine the probability of surprise by position'''
	start_time = time.time()
	print start_time

	w = csv.writer(open("pos_info_letters_tri.csv", "w"))


	#sentence_list, all_words = divide_into_sentences()
	#pdb.set_trace()
	#sentence_list = list(brown.sents())
	all_words = brown.words()
	#pdb.set_trace()
	#all_letters = [list(word) for word in all_words]
	all_words = [list(word) for word in all_words if word != ',' and word != '.' and word != '?' and word != '!' and word != []]
	shuffle(all_words)

	#shorten the list to decrease computational load
	#all_words = [all_words[d] for d in range(len(all_words)) if len(all_words[d]) == 3]
	all_words = all_words[:10000]
	all_letters = itertools.chain.from_iterable(all_words)
	all_letters = list(all_letters)
	#get rid of punctuation in sentences
	#for i in range(len(all_words)):
	#	all_words[i] = filter(lambda a: a != ',' and a != '``' and a != '\'\'' and a != '.' and a != '(' and a != ')' and a != '?' and a != '!', sentence_list[i]) 

	#sentence_list = [sent for sent in sentence_list if len(sent) == 4]


	time1 = time.time() - start_time
	print str(time1) + " time to divide into sentences"
	
	n_gram_list, n_grams_by_words = divide_into_grams(n,all_words)

	time2 = time.time() - time1
	print str(time2) + " time to divide into grams"

	#pdb.set_trace()
	# all_probs = generate_prob_list(n, n_gram_list, all_words, n_grams_by_sentences)

	time3 = time.time() - time2
	print str(time3) + " time to generate probability list"

	#pdb.set_trace()
	avg_info_start = []
	avg_info_end = []
	all_info_values = []
	positions =[]
	#pdb.set_trace()
	maxm = len(all_words[0])
	for i in range(len(all_words)):
		if len(all_words[i]) > maxm:
			maxm = len(all_words[i])
	y_start = []
	y_end = []
	x = []
	all_probs = dict()
	#pdb.set_trace()
	for letter_pos in range(maxm):
		avg_info_start, avg_info_end, all_probs, info_values, pos_list = calc_avg_surprise(n, all_words, letter_pos, n_grams_by_words, n_gram_list, all_probs, all_letters)
		y_start.append(avg_info_start)
		y_end.append(avg_info_end)
		x.append(letter_pos)
		all_info_values.extend(info_values)
		positions.extend(pos_list)
	w.writerow(y_end)
	w.writerow(y_start)
	w.writerow(x)
	w.writerow(all_info_values)
	w.writerow(positions)
	return x, y_start, y_end



def divide_into_grams(n,all_words):
	'''input:
			n is the number of words in a n_gram
			all_words is a list of all of the words in the corpus
		output:
			n_gram_list is the list of all n-grams in the corpus'''
	#split into sentences, then make lists of n-grams from the sentences, it should loop through len(sentences)-n, if that value is negative, skip
	n_grams_by_words = []
	n_gram_list = []
	gram_dict = dict()

	timea = time.time()
	n_grams_by_words = Parallel(n_jobs=2)(delayed(ngrams)(word, n) for word in all_words)
	#collect the words with fewer than n-1 words preceding them
	# n_grams_by_sentences = [n_grams_by_sentences[i] for i in range(len(n_grams_by_sentences)) if n_grams_by_sentences[i]]
	# split_sentences = [sentence.split() for sentence in sentence_list]
	# split_sentences = [split_sentences[k] for k in range(len(split_sentences)) if split_sentences[k]]

	#removes empty lists
	for word_grams in n_grams_by_words:
		word_grams = [x for x in word_grams if x]

	#add grams shorter than n
	for i in range(len(all_words)):
		if str(all_words[i]) in gram_dict:
			n_grams_by_words[i] = gram_dict[str(all_words[i])]
		else:
			for j in range(n-2,-1, -1):
				n_grams_by_words[i] = [tuple(all_words[i][0:j+1])] + n_grams_by_words[i]
			gram_dict[str(all_words[i])] = n_grams_by_words[i]
			#print j, n_grams_by_words[i]

	print time.time() - timea
	n_gram_list = [item for sublist in n_grams_by_words for item in sublist]
	#pdb.set_trace()




	return n_gram_list, n_grams_by_words


def calc_avg_surprise(n, all_words, letter_pos, n_grams_by_words, n_gram_list, probs, all_letters):
	''' input:
			n: number of words in a gram.
			word_list: a list of all the words in the corpus. Within each list is a list of letters in that word.
			letter_pos: specifies which letters are being examined. The number of letter into the sentence that the letter is.
			probs: a dictionary containing the probabilities of a letter given the preceding letters())
			n_grams_by_words is a list with an element for each word. Each element is a list of the n-grams in that w.ord

		Runtime:
			sum_start: the sum of information values for all words at word_pos in each sentence.
			sum_end: the sum of information values for all words at -word_pos in each sentence.
	'''
	print 'calculating probability of surprise given position'
	count_end = 0
	count_start = 0
	cumulative_sum = 0


	sum_start = 0
	sum_end = 0
	info_values = []
	pos_list = []
	probs = dict()
	new_n_gram_list = [str(elm) for elm in n_gram_list]
	letter_freqs = Counter(all_letters)
	n_grams_unique = list(n_gram_list)
	n_grams_unique.sort()
	n_grams_unique = list(gram for gram,_ in itertools.groupby(n_gram_list))
	#print time.time()

	#Create dictionary of ngram frequencies
	#if you have a short ngram, count grams that include it at the beginning as adding to its frequency
	n_gram_freqs = {}
	for ng in n_gram_list:
		for i in range(len(ng)):
			current = n_gram_freqs.get(str(list(ng[0:i+1])),0)
			n_gram_freqs[str(list(ng[0:i+1]))] = current + 1
	#pdb.set_trace()

#	n_gram_freqs[str(ngram)] = [n_gram_freqs[str(ngram)] + sum([1 for ng in n_gram_list if ngram == ng[0:len(ngram)] and len(ng) > len(ngram)]) for ngram in n_grams_unique if len(ngram) < n]
	print time.time()
	
	#Compute average information values for words at word_pos from the beginning and end of the sentence
	#loops through each sentence, collecting information values for words at word_pos from the beginning and end of the sentence
	#when it calculate information value, it checks whether the probability of seeing that word given the preceding word is already known
	#if it is known, it uses that probability to calculate the average surprise value. Otherwise it calculates that probability, stores it in a dictionary, and uses it to calculate the surprise value.
	for i in range(len(all_words)):
		#print "loop da loop" +str(time.time())
		#print word_pos, i
		if len(all_words[i]) - 1 >= letter_pos:
			print i, len(all_words), all_words[i], len(n_grams_by_words)
			print 'n_grams_by_sentences', n_grams_by_words[i]
			if str(list(n_grams_by_words[i][letter_pos])) in probs:
				sum_start += -math.log(probs[str(list(n_grams_by_words[i][letter_pos]))])
				count_start += 1
				info_values.append(-math.log(probs[str(list(n_grams_by_words[i][letter_pos]))]))
				pos_list.append(letter_pos)
			else:
				print n_grams_by_words[i][letter_pos]
				print letter_freqs[n_grams_by_words[i][letter_pos][-1]]#
				probs[str(list(n_grams_by_words[i][letter_pos]))] = float(n_gram_freqs[str(list(n_grams_by_words[i][letter_pos]))])/letter_freqs[n_grams_by_words[i][letter_pos][-1]]#the las word in the gram
				sum_start += -math.log(probs[str(list(n_grams_by_words[i][letter_pos]))])
				count_start += 1
				info_values.append(-math.log(probs[str(list(n_grams_by_words[i][letter_pos]))]))
				pos_list.append(letter_pos)


			if str(list(n_grams_by_words[i][-letter_pos - 1])) in probs:
				#pdb.set_trace()
				sum_end += -math.log(probs[str(list(n_grams_by_words[i][-letter_pos - 1]))])
				count_end += 1
			else:
				probs[str(list(n_grams_by_words[i][-letter_pos - 1]))] = float(n_gram_freqs[str(list(n_grams_by_words[i][-letter_pos - 1]))])/letter_freqs[n_grams_by_words[i][-letter_pos - 1][-1]]#the las letter in the gram
				sum_end += -math.log(probs[str(list(n_grams_by_words[i][-letter_pos - 1]))])
				count_end += 1
			if sum_start == 0:
				print letter_pos, probs[str(list(n_grams_by_words[i][letter_pos]))], letter_freqs[n_grams_by_words[i][letter_pos][-1]]



	return sum_start/count_start, sum_end/count_end, probs, info_values, pos_list





main(3)