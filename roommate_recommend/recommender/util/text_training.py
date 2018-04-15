"""
This file trains the text with word2vec - google pre-trained
doc GoogleNews-vectors-negative300.bin and analyzes the text
similarity using cosine_similarity function from sklearn
library.
"""

import gensim
import os
import gensim.models.keyedvectors as word2vec
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import re
import json


def word2vec_training(path):
    """This method train the model using pre-trained GoogleNews-vectors-negative300.bin document"""
    #os.path.join(os.path.dirname(__file__), 'GoogleNews-vectors-negative300.bin')
    model = word2vec.KeyedVectors.load_word2vec_format(path, binary=True)
    return model


def sentence_to_list(sentence):
    """convert sentence to list of words"""
    return re.findall(r'\w+', sentence)


def get_similarity(curr_sentence, target_sentence, model):
    """Get the similarity between two sentences using word2vec and cosine similarity"""
    curr_word_list = sentence_to_list(curr_sentence)
    target_word_list = sentence_to_list(target_sentence)
    #sum the word vector
    curr_word_vector = 0
    target_word_vector = 0
    for word in curr_word_list:
        if word in model: curr_word_vector += model[word]
    for word in target_word_list:
        if word in model: target_word_vector += model[word]
    if type(curr_word_vector) is np.ndarray and type(target_word_vector) is np.ndarray:
        return cosine_similarity([list(curr_word_vector)], [list(target_word_vector)])
    else:
        return 0



if __name__ == "__main__":
    a = 0
    print(get_similarity('i love you', 'i hate you'))
    print(get_similarity('I love animals and I love cat, besides, I play basketball and quiet', 'I like to be alone'))
    print(get_similarity('I love animals and I love cat, besides, I play basketball and quiet', 'I like sports'))
