'''
@author: Sougata Saha
Institute: University at Buffalo
'''

import collections
from nltk.stem import PorterStemmer
import re
from nltk.corpus import stopwords
import nltk
nltk.download('stopwords')


class Preprocessor:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.ps = PorterStemmer()

    def get_doc_id(self, doc):
        """ Splits each line of the document, into doc_id & text.
            Already implemented"""
        arr = doc.split("\t")
        #arr = re.split('\n', doc.strip().replace('\t'," ").lower())
        return int(arr[0]), arr[1]

    def tokenizer(self, text):
        """ Implement logic to pre-process & tokenize document text.
            Write the code in such a way that it can be re-used for processing the user's query.
            To be implemented."""
    
        list_of_words_without_sw = []
        result = []
        string = text.lower()
        string = re.sub(r"[^a-zA-Z0-9]", " ", string)
        string = string.lstrip(" ")
        string = string.rstrip(" ")
        string = " ".join(string.split())
        string = string.split()
        for word in string:
            if word not in self.stop_words:
                list_of_words_without_sw.append(word)
        for words in list_of_words_without_sw:
            result.append(self.ps.stem(words))
        return result

        """string = text
        string = re.sub(r"[^a-zA-Z0-9 ]", "", string.strip().lower())
        list_of_words = (re.sub(' +', ' ', string)).split()
        list_of_words_without_sw = []
        for word in list_of_words:
            if word not in self.stop_words:
                list_of_words_without_sw.append(self.ps.stem(word))
        return list(set(list_of_words_without_sw))"""

        #raise NotImplementedError
