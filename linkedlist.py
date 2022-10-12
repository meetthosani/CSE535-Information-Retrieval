'''
@author: Sougata Saha
Institute: University at Buffalo
'''

import math


class Node:

    def __init__(self, value=None, next=None, skip_p = None):
        """ Class to define the structure of each node in a linked list (postings list).
            Value: document id, Next: Pointer to the next node
            Add more parameters if needed.
            Hint: You may want to define skip pointers & appropriate score calculation here"""
        self.value = value
        self.next = next
        self.skip_p = skip_p


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
            while curr:
                traversal.append(curr.value)
                curr = curr.next
            #raise NotImplementedError
            return traversal

    def traverse_skips(self):
        traversal = []
        if self.start_node is None:
            return
        else:
            """ Write logic to traverse the linked list using skip pointers.
                To be implemented."""
            curr = self.start_node
            while curr:
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
        self.skip_length = int(round(math.sqrt(self.length), 0))
        curr, prev = self.start_node, self.start_node
        if n_skips*n_skips == self.skip_length:
            i=1
            while i<n_skips and curr:
                for sp in range(self.skip_length+1):
                    if curr:
                        curr = curr.next
                    else:
                        break
                if curr:
                    prev.skip_p = curr
                    prev = prev.next
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
                    prev = prev.next
                    
                else:
                    prev.skip_p = None
                    break
        #raise NotImplementedError

    def insert_at_end(self, value):
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
        else:
            self.start_node = newNode
        

