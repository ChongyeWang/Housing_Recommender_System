import gensim
import os
import gensim.models.keyedvectors as word2vec
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import re
import json


def word2vec_training():
    """This method train the model using pre-trained GoogleNews-vectors-negative300.bin document"""
    model = word2vec.KeyedVectors.load_word2vec_format(os.path.join(os.path.dirname(__file__), 'GoogleNews-vectors-negative300.bin'), binary=True)
    return model


def sentence_to_list(sentence):
    """convert sentence to list of words"""
    return re.findall(r'\w+', sentence)


def get_similarity(curr_sentence, target_sentence):
    """Get the similarity between two sentences using word2vec and cosine similarity"""
    model = word2vec_training()
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
    print(get_similarity('i love you', 'Tarzan'))
