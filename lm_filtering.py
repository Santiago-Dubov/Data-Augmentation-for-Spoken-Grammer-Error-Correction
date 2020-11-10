import argparse
import kenlm
from utils.misc import validate_config

def load_arguments(parser):
	parser.add_argument('--src',type=str, default='None', help= 'source filepath')
	parser.add_argument('--tgt',type=str, default='None', help= 'target filepath')
	parser.add_argument('--lm', type=str, default='None', help= 'language model path')
	parser.add_argument('--threshold', type=int, default='None', help= 'perplexity threshold value')
	return parser

def process(src, tgt, lm, threshold):
	model=kenlm.LanguageModel(lm)
	input_src = open(src, "r")
	input_tgt = open(tgt, "r")
	src_lines = input_src.readlines()
	tgt_lines = input_tgt.readlines()


	with open(src + '.filtered', "w") as f:
		with open(tgt + '.filtered', "w") as g:
			for i in zip(src_lines,tgt_lines):
				#filter using the source sentences
				if model.perplexity(i[0]) < threshold:
					f.write(i[0])
					g.write(i[1])

def main():
	# load config
	parser = argparse.ArgumentParser(description='filtering using a language model')
	parser = load_arguments(parser)
	args = vars(parser.parse_args())
	config = validate_config(args)

	src = config['src']
	tgt = config['tgt']
	threshold = config['threshold']
	lm = config['lm']
	process(src, tgt, lm, threshold)

if __name__ == '__main__':
	main()
