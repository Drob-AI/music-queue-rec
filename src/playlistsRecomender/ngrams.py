import os
import kenlm

class Ngrams:
	def __init__(self):
		LM = os.path.join(os.path.dirname(__file__), 'binary_ngram_data.klm')
		self.model = kenlm.Model(LM)

	def scoreFromStringWithSpacesBetweenIds(self, str):
		# e.g. '251 249 32 56'
		words = ['<s>'] + str.split() + ['</s>']
		return self.model.score(str) / len(words) - 1

	def scoreFromOneDimensionalArrayOfNumbers(self, arr):
		# e.g. [251, 249, 32, 56]
		arr = ' '.join(str(x) for x in arr)
		words = ['<s>'] + arr.split() + ['</s>']
		return self.model.score(arr) / len(words) - 1