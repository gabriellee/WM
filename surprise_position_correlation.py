
import re
corpus = "wikipedia2text-extracted.txt"
import pdb
from collections import Counter
import math

def main(n):
	'''loop through every first word, determine how surprising each set of words is.  Then determine the probability of surprise by position'''
	sentence_list = divide_into_sentences()
	n_gram_list, n_grams_by_sentences = divide_into_grams(n,sentence_list)

	

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
		sentence_list.extend(raw.strip().split('./?/!'))

	for ind in len(sentence_list):
		sentence_list[ind] = re.sub(r'\([^)]*\)','',sentence_list[ind])
		sentence_list[ind] = re.sub(r'\"[^"]*\"','',sentence_list[ind])
		all_words.extend(sentence_list.split())

	#pdb.set_trace()
	sentence_list = [sentence_list for sentence in sentence_list if sentence != []]
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
		word_list = []
		n_gram = []
		word_list = sentence.split()
		if len(sentence) < n:
			for start_ind in len(word_list[:-n]):
				for word_num in range(n):
					n_gram.extend(word_list[start_ind + word_num])
				n_gram_list.append(n_gram)
		n_grams_by_sentences.append(n_gram_list)

	return n_gram_list, n_grams_by_sentences

	def generate_prob_list(n_gram_list, all_words):
	''' generate list of probabilities for words given the preceding word.  Each element is a list containing the probabilities for all words in the sentence
	'''
		n_gram_freqs = Counter(n_gram_list)
		word_freqs = Counter(all_words)

		test_probs = []
		for sentence in sentence_list:
			prob_list = []
			for word_num in range(len(sentence)):
				if word_num != 0:
					prob_list.append(n_gram_freqs[sentence[word_num - 1]+' '+sentence[word_num]]/word_freqs[sentence[word_num]])
				else:
					prob_list.append(n_gram_freqs[sentence[word_num]]/word_freqs[sentence[word_num]])




	def calc_avg_surprise(n, sentence_list, word_num, probs, n_grams_by_sentences):
		'''n_grams_by_sentences is a list with an element for each sentence.  Each element is a list of the n-grams in that sentence.
		'''
		count = 0
		cumulative_sum = 0

		#debugging
		if len(sentence_list) != len(n_grams_by_sentences):
			pdb.set_trace()

		#get probs



		for i in range(sentence_list):
			if len(sentence_list[i]) !< word_num:
				count += 1
				sum_start += -math.log(probs[sentence_list[word_num]])
				sum_end += -math.log(probs[sentence[]])

			'''I'll count from the beginning and also from the end
			you shouldn't average all of the fourth words together because sometimes those words are earlier in the sentence, sometimes later'''




main(2)