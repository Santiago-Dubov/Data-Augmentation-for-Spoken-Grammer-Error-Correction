# to be used after a ptbs dictionary has been created in the current directory containing the most common errors
from collections import Counter
import pickle
from utils.misc import validate_config
import argparse
from nltk import pos_tag
from pattern.en import conjugate, pluralize, singularize
import logging
import multiprocessing
import random
import re, os


def load_arguments(parser):
    parser.add_argument('--input',type=str, default='None', help= 'input corpus source file path')
    parser.add_argument('--output',type=str, default='None', help= 'output file path ')
    return parser

def load_obj(name ):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)

PREPOSITIONS = [
    '', 'of', 'with', 'at', 'from', 'into', 'during', 'including', 'until', 'against', 'among', 'throughout',
    'despite', 'towards', 'upon', 'concerning', 'to', 'in', 'for', 'on', 'by', 'about', 'like',
    'through', 'over', 'before', 'between', 'after', 'since', 'without', 'under', 'within', 'along',
    'following', 'across', 'behind', 'beyond', 'plus', 'except', 'but', 'up', 'out', 'around', 'down'
    'off', 'above', 'near']

VERB_TYPES = ['inf', '1sg', '2sg', '3sg', 'pl', 'part', 'p', '1sgp', '2sgp', '3sgp', 'ppl', 'ppart']

def change_type(word, tag, change_prob):
    global PREPOSITIONS, VERB_TYPES
    if tag == "IN":
        if random.random() < change_prob:
            word = random.choice(PREPOSITIONS)
    elif tag == "NN":
        if random.random() < change_prob:
            word = pluralize(word)
    elif tag == "NNS":
        if random.random() < change_prob:
            word = singularize(word)
    elif "VB" in tag:
        if random.random() < change_prob:
            verb_type = random.choice(VERB_TYPES)
            word = conjugate(word, verb_type)
    return word

def apply_perturbation(words, word2ptbs, word_change_prob, type_change_prob):
    '''For every word in a sentence, if word is in the error dictionary there is a 0.9 prob of being replaced with a random word from its confusion set
    For words not in error dictionary, 0.1 probability of type error
    '''
    word_tags = pos_tag(words)

    sent = []
    for (_, t), w in zip(word_tags, words):
        if w in word2ptbs and random.random() > 1-word_change_prob:
            oris = word2ptbs[w]
            w = random.choice(oris)
        else:
            w = change_type(w, t, type_change_prob)
        sent.append(w)

    try:
        sent = " ".join(sent)
        sent = re.sub("[ ]+", " ", sent)
    except:
        return None

    return sent

def corrupt_corpus(input, output):
    ptbs = load_obj('common_errors_dict')
    with open(output,'w') as f:
        for line in open(input, 'r'):
            words = line.strip().split()
            perturbation = line.strip()
            i = 0
            while perturbation.split() == words and i <= 3:
                # iterates until a perturbation is added
                perturbation = apply_perturbation(words, ptbs, 0.9, 0.1)
                i += 1 # try a maximum of 3 times to create an error
            f.write(perturbation + "\n")


def main():
    # load config
    parser = argparse.ArgumentParser(description='Corrupting corpus')
    parser = load_arguments(parser)
    args = vars(parser.parse_args())
    config = validate_config(args)

    input = config['input']
    output = config['output']
    corrupt_corpus(input, output)

if __name__ == '__main__':
        main()
