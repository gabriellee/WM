
import re
corpus = "wikipedia2text-extracted.txt"
import pdb
from collections import Counter
import math
import itertools

def main(n):
	'''input: 
			n: the number of loop through every first word, determine how surprising each set of words is.  Then determine the probability of surprise by position'''
	sentence_list, all_words = divide_into_sentences()
	n_gram_list, n_grams_by_sentences = divide_into_grams(n,sentence_list)

	#pdb.set_trace()
	all_probs = generate_prob_list(n, n_gram_list, all_words, n_grams_by_sentences)
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
	#pdb.set_trace()
	for word_pos in range(maxm):
		avg_info_start, avg_info_end = calc_avg_surprise(n, sentence_list, word_pos, all_probs, n_grams_by_sentences)
		y_start.append(avg_info_start)
		y_end.append(avg_info_end)
		x.append(word_pos)
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
	print sentence_list[:10]
	sentence_list = sentence_list[:10]
	for ind in range(len(sentence_list)):
		sentence_list[ind].lower()
		sentence_list[ind] = re.sub(r'\([^)]*\)','',sentence_list[ind])
		sentence_list[ind] = re.sub(r'\"[^"]*\"','',sentence_list[ind])
		all_words.extend(sentence_list[ind].split())
	print "length of all_words " + str(len(all_words))
	#print sentence_list
#	pdb.set_trace()

	#pdb.set_trace()
	sentence_list = [sentence for sentence in sentence_list if sentence != '']
	#print sentence_list
	#sentence_list =  sentence_list[:10]
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

	for sentence in sentence_list:
		print 'mew!'
		if type(sentence) != 'string':
			print sentence
		word_list = []
		n_gram = []
		#print sentence
		print "current sentence is " + str(sentence)
		word_list = sentence.split()
		# if len(sentence) > n:
		# 	for start_ind in range(len(word_list[:-n])):
		# 		n_gram = []
		# 		for word_num in range(n):
		# 			n_gram.append(word_list[start_ind + word_num])
		# 		n_gram_list.append(n_gram)
		# n_grams_by_sentences.append(n_gram_list)
		if len(sentence) > n:
			for word_num in range(len(word_list)):
				n_gram = []
				for num_prior in range(n):
					if num_prior <= word_num:
						n_gram.append(word_list[word_num - num_prior])
					else:
						break
				n_gram_list.append(n_gram)
		n_grams_by_sentences.append(n_gram_list)
	#	pdb.set_trace()
	print 'helloooo'

	return n_gram_list, n_grams_by_sentences

def generate_prob_list(n, n_gram_list, all_words, n_grams_by_sentences):
	'''Generates a list of probabilities of each word given the preceding n-1 words. Alist of lists for each sentence. Each element in each inner list corresponds to the probability of that word given the preceding words.
	'''
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


def calc_avg_surprise(n, sentence_list, word_pos, probs, n_grams_by_sentences):
	'''input:
			n: number of words in a gram.  
			sentence_list: a list of all the sentences in the corpus
			word_num:  the index, in the split up sentence(?), of the word whose information content is being examined
			probs:  a dictionary containing the 
	n_grams_by_sentences is a list with an element for each sentence.  Each element is a list of the n-grams in that sentence.
	'''
	count = 0
	cumulative_sum = 0

	#debugging
	if len(sentence_list) != len(n_grams_by_sentences):
		pdb.set_trace()

	#get probs

	sum_start = 0
	sum_end = 0

	for i in range(len(sentence_list)):
		if len(sentence_list[i]) >= word_pos:
			count += 1
			sum_start += -math.log(probs[i][word_pos])
			sum_end += -math.log(probs[i][-word_pos])
	return sum_start/count, sum_end/count

		# '''I'll count from the beginning and also from the end
		# you shouldn't average all of the fourth words together because sometimes those words are earlier in the sentence, sometimes later

		# divide by number of things summed'''




main(2)