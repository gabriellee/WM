
import re
corpus = "wikipedia2text-extracted.txt"
import pdb
from collections import Counter
import math

def main(n):
	'''input: 
			n: the number of loop through every first word, determine how surprising each set of words is.  Then determine the probability of surprise by position'''
	sentence_list, all_words = divide_into_sentences()
	n_gram_list, n_grams_by_sentences = divide_into_grams(n,sentence_list)

	#pdb.set_trace()
	prob_list = generate_prob_list(n_gram_list, all_words)
	pdb.set_trace()
	avg_position_info = []
	for word_num in range(max(len(sentence_list[:]))):
		avg_position_info = calc_avg_surprise(sentence_list, word_num, probs)

	#surprise_values = 


def divide_into_sentences():
	'''produces a list of sentences, exluding parenthetical statements and quotations, from a corpus'''
	crs = open(corpus,'r')
	sentence_list = []
	all_words = []

	for raw in crs:
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
		'''generate list of probabilities for words given the preceding word(s).  Each element is a list containing the probabilities for all words in the sentence'''
		n_gram_freqs = Counter(n_gram_list)
		word_freqs = Counter(all_words)
		n_grams_unique = list(set(n_grams))

		test_probs = []
		for n_grams in n_grams_by_sentences:
			prob_list = []
			for n_gram in n_grams:
				if n_gram < n:
					n_gram_freqs[n_gram] += [1 for ng in n_gram_list if n_gram == ng[0:len(n_gram)] and len(ng) > len(n_gram)]
				prob_list.append(n_gram_freqs[n_gram]/word_freqs[n_gram[1]])





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
		return probs_list


	def calc_avg_surprise(n, sentence_list, word_num, probs, n_grams_by_sentences):
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



		for i in range(sentence_list):
			if len(sentence_list[i]) >= word_num:
				count += 1
				sum_start += -math.log(probs[sentence_list[word_num]])
				sum_end += -math.log(probs[sentence[bleg]])

			'''I'll count from the beginning and also from the end
			you shouldn't average all of the fourth words together because sometimes those words are earlier in the sentence, sometimes later'''




main(3)