'''
@author: Sougata Saha
Institute: University at Buffalo
'''

from subprocess import list2cmdline
from tqdm import tqdm
from preprocessor import Preprocessor
from indexer import Indexer
from collections import OrderedDict
from linkedlist import LinkedList
import inspect as inspector
import sys
import argparse
import json
import time
import random
import flask
from flask import Flask
from flask import request
import hashlib

app = Flask(__name__)


class ProjectRunner:
    def __init__(self):
        self.preprocessor = Preprocessor()
        self.indexer = Indexer()

    def _merge(self, l1, l2):
        """ Implement the merge algorithm to merge 2 postings list at a time.
            Use appropriate parameters & return types.
            While merging 2 postings list, preserve the maximum tf-idf value of a document.
            To be implemented."""
        res = LinkedList()
        list1 = l1.start_node
        list2 = l2.start_node
        count = 0
        while list1 and list2:
            if list1.value == list2.value:

                res.insert_at_end(list1.value, max(list1.tf_idf, list2.tf_idf))
                list1 = list1.next
                list2 = list2.next
                count += 1
            elif list1.value > list2.value:
                list2 = list2.next
                count+=1
            else:
                list1 = list1.next
                count+=1
        return res, count

        
        # raise NotImplementedError

    def _daat_and(self, input_array):
        """ Implement the DAAT AND algorithm, which merges the postings list of N query terms.
            Use appropriate parameters & return types.
            To be implemented."""
        #DAAT and
        if not input_array:
            return [], 0
        count = 0

        # Taking first i/p in res and merging it from 2nd till nth
        res = self.indexer.get_index()[input_array[0]]

        for query in input_array[1:]:
            res, count = self._merge(res, self.indexer.get_index()[query])
            count += 1
        
        merged_list = res.traverse_list()
        return merged_list, count

        # raise NotImplementedError
    
    def _merge_skip(self, l1, l2):
        res = LinkedList()
        list1, list2 = l1.start_node, l2.start_node
        count = 0
        while list1 and list2:
            if list1.value == list2.value:
                res.insert_at_end(list2.value, max(list1.tf_idf, list2.tf_idf))
                list1, list2 = list1.next, list2.next
                count+=1
            elif list1.value>list2.value:
                if list2.skip_p and list2.skip_p.value <= list1.value:
                    while list2.skip_p and list2.skip_p.value<= list1.value:
                        list2 = list2.skip_p
                        count+=1
                else:
                    list2 = list2.next
                    count+=1
            else:
                if list1.skip_p and list1.skip_p.value <= list2.value:
                    while list1.skip_p and list1.skip_p.value <= list2.value:
                        list1 = list1.skip_p
                        count+=1
                else:
                    list1 = list1.next
                    count+=1
        return res, count


    def _daat_skip(self, input_array):
        if not input_array:
            return [], 0
        count = 0
        res = self.indexer.get_index()[input_array[0]]

        for query in input_array[1:]:
            res, count = self._merge_skip(res, self.indexer.get_index()[query])
            count += 1
        
        merged_skip_list = res.traverse_list()
        return merged_skip_list, count

    
    def _daat_tfidf(self, input_array):
        if not input_array:
            return [], 0
        count = 0
        
        res = self.indexer.get_index()[input_array[0]]

        for query in input_array[1:]:
            res, count = self._merge(res, self.indexer.get_index()[query])
            count += 1
        
        merged_list = res.traverse_for_tfidf()
        i = 0
        merged_list = sorted(merged_list, key = lambda x : x.tf_idf, reverse=True)
        o=0
        return [link_list.value for link_list in merged_list], count
    
    def _daat_tfidf_skip(self, input_array):
        if not input_array:
            return [], 0
        count = 0
        res = self.indexer.get_index()[input_array[0]]

        for query in input_array[1:]:
            res, count = self._merge_skip(res, self.indexer.get_index()[query])
            count += 1
        
        merged_skip_list = res.traverse_for_tfidf()
        merged_skip_list = sorted(merged_skip_list, key = lambda x : x.tf_idf, reverse=True)
        
        return [link_list.value for link_list in merged_skip_list], count
    
    def _get_postings(self, term):
        """ Function to get the postings list of a term from the index.
            Use appropriate parameters & return types.
            To be implemented."""
        postings = self.indexer.get_index()[term].traverse_list()
        skip_postings = self.indexer.get_index()[term].traverse_skips()
        return postings, skip_postings
        #raise NotImplementedError

    def _output_formatter(self, op):
        """ This formats the result in the required format.
            Do NOT change."""
        if op is None or len(op) == 0:
            return [], 0
        op_no_score = [int(i) for i in op]
        results_cnt = len(op_no_score)
        return op_no_score, results_cnt

    def run_indexer(self, corpus):
        """ This function reads & indexes the corpus. After creating the inverted index,
            it sorts the index by the terms, add skip pointers, and calculates the tf-idf scores.
            Already implemented, but you can modify the orchestration, as you seem fit."""
        with open(corpus, 'r') as fp:
            lines = sorted(fp.readlines(),key = lambda line:int(line.split()[0]))
            total_docs = 0
            for line in tqdm(lines):
                total_docs += 1
                doc_id, document = self.preprocessor.get_doc_id(line)
                tokenized_document = self.preprocessor.tokenizer(document)
                self.indexer.generate_inverted_index(doc_id, tokenized_document)
        #self.indexer.create_linked_list()
        self.indexer.sort_terms()
        self.indexer.add_skip_connections()
        self.indexer.calculate_tf_idf(total_docs)

    def sanity_checker(self, command):
        """ DO NOT MODIFY THIS. THIS IS USED BY THE GRADER. """

        index = self.indexer.get_index()
        kw = random.choice(list(index.keys()))
        return {"index_type": str(type(index)),
                "indexer_type": str(type(self.indexer)),
                "post_mem": str(index[kw]),
                "post_type": str(type(index[kw])),
                "node_mem": str(index[kw].start_node),
                "node_type": str(type(index[kw].start_node)),
                "node_value": str(index[kw].start_node.value),
                "command_result": eval(command) if "." in command else ""}

    def run_queries(self, query_list, random_command):
        """ DO NOT CHANGE THE output_dict definition"""
        output_dict = {'postingsList': {},
                       'postingsListSkip': {},
                       'daatAnd': {},
                       'daatAndSkip': {},
                       'daatAndTfIdf': {},
                       'daatAndSkipTfIdf': {},
                       'sanity': self.sanity_checker(random_command)}

        for query in tqdm(query_list):
            """ Run each query against the index. You should do the following for each query:
                1. Pre-process & tokenize the query.
                2. For each query token, get the postings list & postings list with skip pointers.
                3. Get the DAAT AND query results & number of comparisons with & without skip pointers.
                4. Get the DAAT AND query results & number of comparisons with & without skip pointers, 
                    along with sorting by tf-idf scores."""
            #raise NotImplementedError

            input_term_arr = self.preprocessor.tokenizer(query)  # Tokenized query. To be implemented.
            for term in input_term_arr:
                postings, skip_postings = self._get_postings(term)


                """ Implement logic to populate initialize the above variables.
                    The below code formats your result to the required format.
                    To be implemented."""

                output_dict['postingsList'][term] = postings
                output_dict['postingsListSkip'][term] = skip_postings

            and_op_no_skip, and_op_skip, and_op_no_skip_sorted, and_op_skip_sorted = None, None, None, None
            and_comparisons_no_skip, and_comparisons_skip, \
                and_comparisons_no_skip_sorted, and_comparisons_skip_sorted = None, None, None, None

            and_op_no_skip, and_comparisons_no_skip = self._daat_and(input_term_arr)
            and_op_skip, and_comparisons_skip = self._daat_skip(input_term_arr)
            and_op_no_skip_sorted, and_comparisons_no_skip_sorted = self._daat_tfidf(input_term_arr)
            and_op_skip_sorted, and_comparisons_skip_sorted = self._daat_tfidf_skip(input_term_arr)
            
            """ Implement logic to populate initialize the above variables.
                The below code formats your result to the required format.
                To be implemented."""
            and_op_no_score_no_skip, and_results_cnt_no_skip = self._output_formatter(and_op_no_skip)
            and_op_no_score_skip, and_results_cnt_skip = self._output_formatter(and_op_skip)
            and_op_no_score_no_skip_sorted, and_results_cnt_no_skip_sorted = self._output_formatter(and_op_no_skip_sorted)
            and_op_no_score_skip_sorted, and_results_cnt_skip_sorted = self._output_formatter(and_op_skip_sorted)

            output_dict['daatAnd'][query.strip()] = {}
            output_dict['daatAnd'][query.strip()]['results'] = and_op_no_score_no_skip
            output_dict['daatAnd'][query.strip()]['num_docs'] = and_results_cnt_no_skip
            output_dict['daatAnd'][query.strip()]['num_comparisons'] = and_comparisons_no_skip

            output_dict['daatAndSkip'][query.strip()] = {}
            output_dict['daatAndSkip'][query.strip()]['results'] = and_op_no_score_skip
            output_dict['daatAndSkip'][query.strip()]['num_docs'] = and_results_cnt_skip
            output_dict['daatAndSkip'][query.strip()]['num_comparisons'] = and_comparisons_skip

            output_dict['daatAndTfIdf'][query.strip()] = {}
            output_dict['daatAndTfIdf'][query.strip()]['results'] = and_op_no_score_no_skip_sorted
            output_dict['daatAndTfIdf'][query.strip()]['num_docs'] = and_results_cnt_no_skip_sorted
            output_dict['daatAndTfIdf'][query.strip()]['num_comparisons'] = and_comparisons_no_skip_sorted

            output_dict['daatAndSkipTfIdf'][query.strip()] = {}
            output_dict['daatAndSkipTfIdf'][query.strip()]['results'] = and_op_no_score_skip_sorted
            output_dict['daatAndSkipTfIdf'][query.strip()]['num_docs'] = and_results_cnt_skip_sorted
            output_dict['daatAndSkipTfIdf'][query.strip()]['num_comparisons'] = and_comparisons_skip_sorted

        return output_dict


@app.route("/execute_query", methods=['POST'])
def execute_query():
    """ This function handles the POST request to your endpoint.
        Do NOT change it."""
    start_time = time.time()

    queries = request.json["queries"]
    random_command = request.json["random_command"]

    """ Running the queries against the pre-loaded index. """
    output_dict = runner.run_queries(queries, random_command)

    """ Dumping the results to a JSON file. """
    with open(output_location, 'w') as fp:
        json.dump(output_dict, fp)

    response = {
        "Response": output_dict,
        "time_taken": str(time.time() - start_time),
        "username_hash": username_hash
    }
    return flask.jsonify(response)


if __name__ == "__main__":
    """ Driver code for the project, which defines the global variables.
        Do NOT change it."""

    output_location = "project2_output.json"
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--corpus", type=str, help="Corpus File name, with path.", default="./data/input_corpus.txt")
    parser.add_argument("--output_location", type=str, help="Output file name.", default=output_location)
    parser.add_argument("--username", type=str,
                        help="Your UB username. It's the part of your UB email id before the @buffalo.edu. "
                             "DO NOT pass incorrect value here", default = "meetpiyu")

    argv = parser.parse_args()

    corpus = argv.corpus
    output_location = argv.output_location
    username_hash = hashlib.md5(argv.username.encode()).hexdigest()

    """ Initialize the project runner"""
    runner = ProjectRunner()

    """ Index the documents from beforehand. When the API endpoint is hit, queries are run against 
        this pre-loaded in memory index. """
    runner.run_indexer(corpus)

    app.run(host="0.0.0.0", port=9999)
