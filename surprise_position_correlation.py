
import re
corpus = "wikipedia2text-extracted.txt"
import pdb
from collections import Counter
import math
from joblib import Parallel, delayed
import itertools
import time
import pickle
import csv
from random import shuffle
from nltk.util import ngrams

def main(n):
	'''input: 
			n: the number of loop through every first word, determine how surprising each set of words is.  Then determine the probability of surprise by position'''
	start_time = time.time()
	print start_time

	w = csv.writer(open("pos_info_30000sentences.csv", "w"))


	sentence_list, all_words = divide_into_sentences()
	#pdb.set_trace()

	time1 = time.time() - start_time
	print str(time1) + " time to divide into sentences"
	
	n_gram_list, n_grams_by_sentences = divide_into_grams(n,sentence_list)

	time2 = time.time() - time1
	print str(time2) + " time to divide into grams"

	#pdb.set_trace()
	# all_probs = generate_prob_list(n, n_gram_list, all_words, n_grams_by_sentences)

	time3 = time.time() - time2
	print str(time3) + " time to generate probability list"

	#pdb.set_trace()
	avg_info_start = []
	avg_info_end = []
	#pdb.set_trace()
	maxm = len(sentence_list[0].split())
	maxm = [len(sentence_list[i].split()) for i in range(len(sentence_list)) if len(sentence_list[i].split()) > len(sentence_list[i-1].split())]
	maxm = maxm[-1]
	y_start = []
	y_end = []
	x = []
	all_probs = dict()
	#pdb.set_trace()
	for word_pos in range(maxm):
		avg_info_start, avg_info_end, all_probs = calc_avg_surprise(n, sentence_list, word_pos, n_grams_by_sentences, n_gram_list, all_probs, all_words)
		y_start.append(avg_info_start)
		y_end.append(avg_info_end)
		x.append(word_pos)
	w.writerow(y_end)
	w.writerow(y_start)
	w.writerow(x)
	return x, y_start, y_end

	#surprise_values = 


def divide_into_sentences():
	'''produces a list of sentences, exluding parenthetical statements and quotations, from a corpus'''
	crs = open(corpus,'r')
	sentence_list = []
	all_words = []

	for raw in crs:
		raw = raw.lower()
		sentence_list.extend(re.split('[!?.]', raw.strip()))
	#sentence_list = [elm[:-1] for elm in sentence_list]
	#print sentence_list[:10]
	#sentence_list = sentence_list[:10]
	for ind in range(len(sentence_list)):
		sentence_list[ind].lower()
		sentence_list[ind] = re.sub(r'\([^)]*\)','',sentence_list[ind])
		sentence_list[ind] = re.sub(r'\"[^"]*\"','',sentence_list[ind])
		all_words.extend(sentence_list[ind].split())
	#print "length of all_words " + str(len(all_words))
	#print sentence_list
#	pdb.set_trace()

	#pdb.set_trace()
	sentence_list = [sentence for sentence in sentence_list if sentence != '' and sentence != ' ' and len(sentence.split()) > 1]
	sentence_list = shuffle(sentence_list)
	#print sentence_list
	sentence_list =  sentence_list[:30000]
	return sentence_list, all_words



def divide_into_grams(n,sentence_list):
	'''input:
			n is the number of words in a n_gram
			sentence_list is a list of all of the sentences in the corpus
		output:
			n_gram_list is the list of all n-grams in the corpus'''
	#split into sentences, then make lists of n-grams from the sentences, it should loop through len(sentences)-n, if that value is negative, skip
	n_grams_by_sentences = []
	n_gram_list = []

	# timea = time.time()
	# g = [ngrams(sentence.split(), n) for sentence in sentence_list[:10]]
	# timeb = time.time()
	# print timeb-timea
	# print len(sentence_list)
	# print (timeb - timea)*(len(sentence_list)/10)
	# pdb.set_trace()
	timea = time.time()
	#g = [ngrams(sentence.split(), n) for sentence in sentence_list[0:50000]]
	n_grams_by_sentences = Parallel(n_jobs=2)(delayed(ngrams)(sentence.split(), n) for sentence in sentence_list)
	#collect the words with fewer than n-1 words preceding them
	n_grams_by_sentences = [n_grams_by_sentences[i] for i in range(len(n_grams_by_sentences)) if n_grams_by_sentences[i]]
	split_sentences = [sentence.split() for sentence in sentence_list]
	split_sentences = [split_sentences[k] for k in range(len(split_sentences)) if split_sentences[k]]

	for j in range(n-1):
		for i in range(len(sentence_list)):
			n_grams_by_sentences[i] = [split_sentences[i][j:n-1]] + n_grams_by_sentences[i]
		#pdb.set_trace()
		#n_gram_list = [sentence.split()[j] for sentence in sentence_list]
	print time.time() - timea
	#pdb.set_trace()
	n_gram_list = [item for sublist in n_grams_by_sentences for item in sublist]

#	n_gram_list = [ngrams(sentence.split(), n) for sentence in sentence_list]
	#for sentence in sentence_list:

		# word_list = []
		# n_gram = []
		# #print sentence
		# #print "current sentence is " + str(sentence)
		# word_list = sentence.split()

		# if len(sentence) > n:
		# 	for word_num in range(len(word_list)):
		# 		n_gram = []
		# 		for num_prior in range(n):
		# 			if num_prior <= word_num:
		# 				n_gram.append(word_list[word_num - num_prior])
		# 			else:
		# 				break
		# 		n_gram_list.append(n_gram)
		# n_grams_by_sentences.append(n_gram_list)


	return n_gram_list, n_grams_by_sentences

def generate_prob_list(n, n_gram_list, all_words, n_grams_by_sentences):
	'''Generates a list of probabilities of each word given the preceding n-1 words. A list of lists for each sentence. Each element in each inner list corresponds to the probability of that word given the preceding words.
	Generates a dictionary in which each ngram maps to a probability'''
	#counter cannot work with lists of lists, so I make lists strings
	new_n_gram_list = [str(elm) for elm in n_gram_list]
	n_gram_freqs = Counter(new_n_gram_list)
	word_freqs = Counter(all_words)
	n_grams_unique = list(n_gram_list)
	n_grams_unique.sort()
	n_grams_unique = list(gram for gram,_ in itertools.groupby(n_gram_list))


		#list(frozenset(n_gram_list))

	for ngram in n_grams_unique:
		if len(ngram) < n:
			#print n_gram, str(n_gram), n_gram_freqs[str(n_gram)]
			#if you have a short ngram, count grams that include it at the beginning as adding to its frequency
			n_gram_freqs[str(ngram)] = n_gram_freqs[str(ngram)] + sum([1 for ng in n_gram_list if ngram == ng[0:len(ngram)] and len(ng) > len(ngram)])

	all_probs = []
	for n_grams in n_grams_by_sentences:
		prob_list = []
		for n_gram in n_grams:
			prob_list.append(float(n_gram_freqs[str(n_gram)])/word_freqs[n_gram[0]])
		all_probs.append(prob_list)



	#pdb.set_trace()

			# for word_num in range(len(word_list)):
			# 	# n_gram = []
			# 	for num_prior in range(n):
			# 		if num_prior <= word_num:
			# 			if len(n_gram_list[])
			# 			prob_list[sentence_ind].append(n_gram_freqs[sentence[word_num]])
			# 			# n_gram.append(word_list[word_num - num_prior])
			# 		else:
			# 			break


			# for word_num in range(len(sentence)):
			# 	if word_num >= (n-1):
			# 		#fix the following line so that it loops through n times
			# 		prob_list.append(n_gram_freqs[sentence[word_num - 1]+' '+sentence[word_num]]/word_freqs[sentence[word_num]])
			# 	else:
			# 		#fix this line as wellsentence_
			# 		prob_list.append(n_gram_freqs[sentence[word_num]]/word_freqs[sentence[word_num]])
	return all_probs


def calc_avg_surprise(n, sentence_list, word_pos, n_grams_by_sentences, n_gram_list, probs, all_words):
	'''input:
			n: number of words in a gram.  
			sentence_list: a list of all the sentences in the corpus
			word_num:  the index, in the split up sentence(?), of the word whose information content is being examined
			probs:  a dictionary containing the 
	n_grams_by_sentences is a list with an element for each sentence.  Each element is a list of the n-grams in that sentence.
	'''
	print 'calculating probability of surprise given position'
	count_end = 0
	count_start = 0
	cumulative_sum = 0

	#debugging
	if len(sentence_list) != len(n_grams_by_sentences):
		pdb.set_trace()

	#get probs

	sum_start = 0
	sum_end = 0
	#loop through sentences and check the info of a word at a given distance from start and end
	#first check whether it already knows the probability, otherwise, compute it and add it to a dict
	probs = dict()
	new_n_gram_list = [str(elm) for elm in n_gram_list]
	#n_gram_freqs = Counter(new_n_gram_list)
	word_freqs = Counter(all_words)
	n_grams_unique = list(n_gram_list)
	n_grams_unique.sort()
	n_grams_unique = list(gram for gram,_ in itertools.groupby(n_gram_list))
	#print time.time()
	#if you have a short ngram, count grams that include it at the beginning as adding to its frequency
	n_gram_freqs = {}
	for ng in n_gram_list:
		for i in range(len(ng)):
			current = n_gram_freqs.get(str(list(ng[0:i+1])),0)
			n_gram_freqs[str(list(ng[0:i+1]))] = current + 1
	#pdb.set_trace()

#	n_gram_freqs[str(ngram)] = [n_gram_freqs[str(ngram)] + sum([1 for ng in n_gram_list if ngram == ng[0:len(ngram)] and len(ng) > len(ngram)]) for ngram in n_grams_unique if len(ngram) < n]
	print time.time()
	# for ngram in n_grams_unique:
	# 	if len(ngram) < n:
	# 		#print n_gram, str(n_gram), n_gram_freqs[str(n_gram)]
	# 		n_gram_freqs[str(ngram)] = n_gram_freqs[str(ngram)] + sum([1 for ng in n_gram_list if ngram == ng[0:len(ngram)] and len(ng) > len(ngram)])

	#loops through each sentence, then through each n
	for i in range(len(sentence_list)):
		#print "loop da loop" +str(time.time())
		#print word_pos, i
		if len(sentence_list[i].split()) - 1 >= word_pos:
			#pdb.set_trace()
			if str(list(n_grams_by_sentences[i][word_pos])) in probs:
				#if str(n_grams_by_sentences[i][-word_pos]) == '(\'"covert\', \'propaganda\')':
					#print word_pos, i
					#print n_grams_by_sentences[i][word_pos]
					#pdb.set_trace()
				sum_start += -math.log(probs[str(list(n_grams_by_sentences[i][word_pos]))])
				count_start += 1
			else:
				#pdb.set_trace()
				probs[str(list(n_grams_by_sentences[i][word_pos]))] = float(n_gram_freqs[str(list(n_grams_by_sentences[i][word_pos]))])/word_freqs[n_grams_by_sentences[i][word_pos][-1]]#the las word in the gram
			if str(list(n_grams_by_sentences[i][-word_pos])) in probs:
				sum_end += -math.log(probs[str(list(n_grams_by_sentences[i][-word_pos]))])
				count_end += 1
			else:
				probs[str(list(n_grams_by_sentences[i][-word_pos]))] = float(n_gram_freqs[str(list(n_grams_by_sentences[i][word_pos]))])/word_freqs[n_grams_by_sentences[i][word_pos][-1]]#the las word in the gram


				


	# for i in range(len(sentence_list)):
	# 	if len(sentence_list[i]) >= word_pos:
	# 		count += 1
	# 		print i
	# 		if i == 100:
	# 			print i
	# 			#pdb.set_trace()
	# 		sum_start += -math.log(probs[i][word_pos])
	# 		sum_end += -math.log(probs[i][-word_pos])
	return sum_start/count_start, sum_end/count_end, probs

		# '''I'll count from the beginning and also from the end
		# you shouldn't average all of the fourth words together because sometimes those words are earlier in the sentence, sometimes later

		# divide by number of things summed'''




main(2)