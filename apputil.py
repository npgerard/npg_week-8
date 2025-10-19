from collections import defaultdict

import numpy as np
import pandas as pd
import requests
import re
from collections import Counter, defaultdict


class MarkovText(object):

    def __init__(self, corpus):
        self.corpus = corpus
        self.term_dict = None  # you'll need to build this


    def get_term_dict(self):
        '''
            Returns a dictionary representing the Markov chain built from the corpus.
            Each key is a term from the corpus, and its value is a list of terms that can follow it.
            There are no limits on the number of terms that can follow a given term 
                (i.e., if a term appears multiple times followed by the same term, 
                that term should appear multiple times in the list). 
            The only exception is that terms that end a sentence (i.e., end with '.', '!', or '?')
                should not have any following terms in the dictionary because the sentence has ended.
                Words that follow the end of a sentence are not probabilistically linked to the prior term.
        '''


        # tokenize the corpus after lowering case so that keys do not repeat.
        tokens = self.corpus.lower().split()


        # instantiate term_dict dictionary defaultdict so we don't have to check for key existence
        term_dict = defaultdict(list)

        # Step 2: Build the Markov chain
        for i in range(len(tokens) - 1):
            current_token = tokens[i]
            next_token = tokens[i + 1]

            # Skip tokens that end a sentence
            if current_token[-1] in ".!?":
                continue

            term_dict[current_token].append(next_token)


        # output
        self.term_dict = term_dict

        return self.term_dict


    def generate(self, seed_term=None, term_count=15):

        # your code here ...
        # if we have not yet built the term_dict, build it now
        if self.term_dict is None:
            self.get_term_dict()
        
        # if no seed term is provided, randomly select one from the keys of the term_dict
        if seed_term is None:
            seed_term = np.random.choice(list(self.term_dict.keys()))

        # generate starting with the seed/first random term; make sure to lower case the seed term to match the keys in the term_dict
        current_term = seed_term.lower()
        
        # first item in the list is the current term
        output_terms = [current_term]

        for _ in range(term_count - 1):
            next_terms = self.term_dict.get(current_term)
            if not next_terms:
                break
            current_term = np.random.choice(next_terms)
            output_terms.append(current_term)
        return ' '.join(output_terms)

        