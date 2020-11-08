import os
import argparse
import sys 
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.lm import Vocabulary
import logging
logging.basicConfig(level=logging.INFO)

from utils.misc import validate_config
def load_arguments(parser):

	parser.add_argument('--path_vocab_src', type=str, default='None', help = 'vocab src dir') 	
	parser.add_argument('--vocab_path_out', type=str, default='None', help = 'Vocab path out')
	return parser

def building_vocab(path_vocab_src, vocab_path_out):
	vocab_src = open(path_vocab_src, "r")
	raw = vocab_src.read()
	tokenizer = RegexpTokenizer('\w+|\$[\d\.]+|\S+')
	tokens = tokenizer.tokenize(raw)
	vocab = Vocabulary(tokens, unk_cutoff=8)

	sorted_vocab = sorted(vocab)
	sorted_vocab.remove('.')
	sorted_vocab.remove('<UNK>')
	with open(vocab_path_out, "w") as f:
		f.write('<pad>' + '\n')
		f.write('<unk>' + '\n')
		f.write('<s>' + '\n')
		f.write('</s>' + '\n')
		f.write('.' + '\n')
		for item in sorted_vocab:
			f.write(item + '\n')


def main():
	# load config
	parser = argparse.ArgumentParser(description='Building vocab')
	parser = load_arguments(parser)
	args = vars(parser.parse_args())
	config = validate_config(args)

	path_vocab_src = config['path_vocab_src']
	vocab_path_out = config['vocab_path_out']
	print('2')
	building_vocab(path_vocab_src, vocab_path_out)

if __name__ == '__main__':
	main()
