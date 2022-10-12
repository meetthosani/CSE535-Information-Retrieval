'''
@author: Sougata Saha
Institute: University at Buffalo
'''

import math


class Node:

    def __init__(self, value=None, next=None, skip_p = None, tf = None, tf_idf = None):
        """ Class to define the structure of each node in a linked list (postings list).
            Value: document id, Next: Pointer to the next node
            Add more parameters if needed.
            Hint: You may want to define skip pointers & appropriate score calculation here"""
        self.value = value
        self.next = next
        self.skip_p = skip_p
        self.tf = tf
        self.tf_idf = 0


class LinkedList:
    """ Class to define a linked list (postings list). Each element in the linked list is of the type 'Node'
        Each term in the inverted index has an associated linked list object.
        Feel free to add additional functions to this class."""
    def __init__(self):
        self.start_node = None
        self.end_node = None
        self.length, self.n_skips, self.idf = 0, 0, 0.0
        self.skip_length = None
    
    
  
    def printLL(self):
      current = self.start_node
      while(current):
        print(current.value)
        current = current.next

    def traverse_list(self):
        traversal = []
        if self.start_node is None:
            return
        else:
            """ Write logic to traverse the linked list.
                To be implemented."""
            curr = self.start_node
            while curr is not None:
                traversal.append(curr.value)
                curr = curr.next
            #raise NotImplementedError
            return traversal
    
    def traverse_for_tfidf(self):
        traversal = []
        if self.start_node is None:
            return
        else:
            curr = self.start_node
            # Start traversal from head, and go on till you reach None
            while curr is not None:
                traversal.append(curr)
                curr = curr.next
            return traversal
    
    def add_idf_scores(self,tf_idf_scores):
        curr = self.start_node
        for score in tf_idf_scores:
            curr.tf_idf = score
            curr = curr.next
    
    def traverse_skips(self):
        traversal = []
        if self.start_node is None:
            return
        else:
            """ Write logic to traverse the linked list using skip pointers.
                To be implemented."""
            curr = self.start_node
            while curr is not None:
                traversal.append(curr.value)
                curr = curr.skip_p
            #raise NotImplementedError
            return traversal

    def add_skip_connections(self):
        n_skips = math.floor(math.sqrt(self.length))
        if n_skips * n_skips == self.length:
            n_skips = n_skips - 1
        """ Write logic to add skip pointers to the linked list. 
            This function does not return anything.
            To be implemented."""
        if n_skips==0:
            return
        self.skip_length = round(math.sqrt(self.length), 0)
        
        if (self.start_node is None):
            return 
        
        if (not self.skip_length>=1):
            return
        
        curr, prev = self.start_node, self.start_node
        while curr:
            i, prev = 0, curr
            while i<self.skip_length and prev is not None:
                prev = prev.next
                i+=1
            curr.skip_p = prev
            curr = curr.skip_p

        """if n_skips*n_skips == self.skip_length:
            i=1
            while i<n_skips and curr:
                for sp in range(self.skip_length+1):
                    if curr:
                        curr = curr.next
                    else:
                        break
                if curr:
                    prev.skip_p = curr
                    prev = prev.skip_p
                    i+=1
                    #print(i, skip_p.data)
                else:
                    prev.skip_p = None
                    break
        else:
            while curr:
                for sp in range(self.skip_length+1):
                    if curr:
                        curr = curr.next
                    else:
                        break
                if curr:
                    prev.skip_p = curr
                    prev = prev.skip_p
                    
                else:
                    prev.skip_p = None
                    break """
        #raise NotImplementedError

    def insert_at_end(self, value, tf):
        """ Write logic to add new elements to the linked list.
            Insert the element at an appropriate position, such that elements to the left are lower than the inserted
            element, and elements to the right are greater than the inserted element.
            To be implemented. """
        newNode = Node(value)
        self.length+=1
        if(self.start_node):
            current = self.start_node
            while(current.next):
                current = current.next
            current.next = newNode
            self.end_node = newNode
            self.end_node.tf = tf
        else:
            self.start_node = newNode
            self.end_node = newNode
            self.end_node.tf = tf


    def cal_tf_idf(self, total_docs):
        curr, curr_len = self.start_node, self.start_node
        if curr is None:
            return
        self.idf = total_docs/self.length
        # print("idf scores are ---> ", self.idf)
        count = 0
        while curr_len:
            count+=1
            curr_len = curr_len.next
        # print("len of posting list ",count)
        while curr:
            tf = curr.tf / count
            #print("TF --> ",tf, "self.idf--->", self.idf)
            curr.tf_idf = tf * self.idf
            # print("tf-idf --->",curr.tf_idf)
            curr = curr.next
            
        

        

