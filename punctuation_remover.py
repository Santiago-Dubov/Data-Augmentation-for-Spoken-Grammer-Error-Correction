import argparse
from utils.misc import validate_config
import re 

def load_arguments(parser):
	parser.add_argument('--input',type=str, default='None', help= 'source filepath')
	parser.add_argument('--output', type=str, default='None', help= 'output path')
	return parser

def building_vocab(path_src, path_src_no_punct):
	vocab_src = open(path_src, "r")
	raw = vocab_src.read()
	raw = raw.lower()
	without_punctuation = raw.translate(str.maketrans('', '', '!#$%&()*+,-./:;<=>?@[\]^_{|}~' ))
	no_double_space = re.sub(' +', ' ', without_punctuation)
	with open(path_src_no_punct, "w") as f:
		f.write(no_double_space)
def main():
	# load config
	parser = argparse.ArgumentParser(description='Building vocab')
	parser = load_arguments(parser)
	args = vars(parser.parse_args())
	config = validate_config(args)

	path_src = config['input']
	path_src_no_punct = config['output']
	print('2')
	building_vocab(path_src, path_src_no_punct)

if __name__ == '__main__':
	main()
