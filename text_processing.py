from typing import List

import string
import re
import unicodedata
import contractions

from num2words import num2words
from text_to_num import alpha2digit
from spellchecker import SpellChecker

from nltk import pos_tag
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer, PorterStemmer


class TextProcessing:
	@classmethod
	def process(cls, txt: str):
		# Convert to lowercase
		txt = txt.lower()

	    # Remove all accented characters from a string, eg: é, Á. ó
		# txt = TextProcessing.remove_accented_chars(txt)

		# Expand contractions, eg: "cannot, I'm" => "can not, I am"
		txt = TextProcessing.expand_contractions(txt)

		# Separates numbers from words or other characters
		txt = TextProcessing.sep_num_words(txt)

		# Convert words to numbers
		txt = TextProcessing.words_to_num(txt)

		# Remove leading zeroes from numbers TODO: Do not remove "0"
		# txt = TextProcessing.remove_leading_zeroes(txt)

		# Remove punctuations
		txt = txt.translate(str.maketrans('', '', string.punctuation))

		# Tokenize into words
		words = word_tokenize(txt)

		# Correct word spelling
		# words = TextProcessing.correct_spelling(words)
		
		# Remove stopwords
		words = TextProcessing.remove_stopwords(words)
		
		# Lemmatize words
		words = TextProcessing.lemmatize(words)

		# Stem words
		# words = TextProcessing.stem(words)

		# Merge words list into a string
		txt = ' '.join(words)

	    # Remove extra whitespaces
		# txt = TextProcessing.remove_extra_whitespaces(txt)

		return txt


	@classmethod
	def remove_stopwords(cls, words: List[str]) -> List[str]:
		new_words = []
		
		for word in words:
			if word not in stopwords.words('english'):
				new_words.append(word)
		
		return new_words
	
    # Remove all accented characters from a string, eg: é, Á. ó
	@classmethod
	def remove_accented_chars(cls, text):
		return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')
	
	@classmethod
	def remove_extra_whitespaces(cls, text):
		return re.sub(r'^\s*|\s\s*', ' ', text).strip()

	# eg: "cannot, I'm" => "can not, I am"
	@classmethod
	def expand_contractions(cls, text):
		return contractions.fix(text)
	
	# Separates numbers from words or other characters, excluding ordinal numbers.
	@classmethod
	def sep_num_words(cls, text):
		return re.sub(r"(?<!\d)(\d+)(st|nd|rd|th)", r" \1\2", text).strip()

	# Remove leading zeroes from numbers TODO: Do not remove "0"
	@classmethod
	def remove_leading_zeroes(cls, text):
		pattern = r'\b0+([0-9]*)\b'
		return re.sub(pattern, r'\1', text)

	# Convert words to numbers
	@classmethod
	def words_to_num(cls, text):
		return alpha2digit(text, "en", True, ordinal_threshold=0)

	# Convert Numbers to Words
	@classmethod
	def num_to_words(cls, text):
		after_spliting = text.split()

		for index in range(len(after_spliting)):
			if after_spliting[index].isdigit():
				after_spliting[index] = num2words(after_spliting[index])
		numbers_to_words = ' '.join(after_spliting)
		return numbers_to_words

	@classmethod
	def correct_spelling(cls, tokens: List[str]) -> List[str]:
		spell = SpellChecker()
		misspelled = spell.unknown(tokens)
		for i, token in enumerate(tokens):
			if token in misspelled:
				corrected = spell.correction(token)
				if corrected is not None:
					tokens[i] = corrected
		return tokens

	@classmethod
	def lemmatize(cls, words: List[str]) -> List[str]:
		def get_wordnet_pos(tag_parameter):

			tag = tag_parameter[0].upper()
			tag_dict = {"J": wordnet.ADJ,
						"N": wordnet.NOUN,
						"V": wordnet.VERB,
						"R": wordnet.ADV}
			
			return tag_dict.get(tag, wordnet.NOUN)
		
		# POS tagging
		pos_tags = pos_tag(words)

		lemmatizer = WordNetLemmatizer()
		lemmatized_words = [lemmatizer.lemmatize(word, pos=get_wordnet_pos(tag)) for word, tag in pos_tags]

		return lemmatized_words

	@classmethod
	def stem(cls, words: List[str]) -> List[str]:
		stemmer = PorterStemmer()
		stemmed_words = [stemmer.stem(word) for word in words]
		return stemmed_words
