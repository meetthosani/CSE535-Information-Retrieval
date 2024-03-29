'''
@author: Sougata Saha
Institute: University at Buffalo
'''

#from typing import Counter
from linkedlist import LinkedList
from collections import OrderedDict
from collections import Counter


class Indexer:
    def __init__(self):
        """ Add more attributes if needed"""
        self.inverted_index = OrderedDict({})
        self.num_of_tokens = OrderedDict({})

    def get_index(self):
        """ Function to get the index.
            Already implemented."""
        return self.inverted_index

    def generate_inverted_index(self, doc_id, tokenized_document):
        """ This function adds each tokenized document to the index. This in turn uses the function add_to_index
            Already implemented."""
        tf = Counter(tokenized_document)
        self.num_of_tokens[doc_id] = len(tokenized_document)
        tokenized_document = list(set(tokenized_document))
        for t in tokenized_document:
            self.add_to_index(t, doc_id, tf[t])

    def add_to_index(self, term_, doc_id_, tf):
        """ This function adds each term & document id to the index.
            If a term is not present in the index, then add the term to the index & initialize a new postings list (linked list).
            If a term is present, then add the document to the appropriate position in the posstings list of the term.
            To be implemented."""
        

        if term_ in self.inverted_index:
            self.inverted_index.get(term_).insert_at_end(doc_id_, tf)

        else:
            self.inverted_index[term_] = LinkedList()
            self.inverted_index[term_].insert_at_end(doc_id_, tf)
        # print(self.inverted_index)
            #self.inverted_index[term_] = [int(doc_id_)]
        
        #for key, value in self.inverted_index.items():
         #   self.inverted_index[key] = sorted(value)
        

    def sort_terms(self):
        """ Sorting the index by terms.
            Already implemented."""
        sorted_index = OrderedDict({})
        for k in sorted(self.inverted_index.keys()):
            sorted_index[k] = self.inverted_index[k]
        self.inverted_index = sorted_index

    def add_skip_connections(self):
        """ For each postings list in the index, add skip pointers.
            To be implemented."""
        
        for key, value in self.inverted_index.items():
            value.add_skip_connections()

        
        #raise NotImplementedError

    def calculate_tf_idf(self, total_docs):
        """ Calculate tf-idf score for each document in the postings lists of the index.
            To be implemented."""
        for key, value in self.inverted_index.items():
            value.cal_tf_idf(total_docs, self.num_of_tokens)
            
        #raise NotImplementedError
