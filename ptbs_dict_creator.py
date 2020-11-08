from collections import Counter
import pickle
from utils.misc import validate_config
import argparse

def load_arguments(parser):
	parser.add_argument('--path_m2',type=str, default='None', help= 'source filepath')
	return parser

def make_word2ptbs(m2_file, min_cnt):
    '''Error Simulation
    m2: string. m2 file path.
    min_cnt: int. minimum count
    '''
    word2ptbs = dict()  # ptb: pertubation
    entries = open(m2_file, 'r').read().strip().split("\n\n")
    for entry in entries[:]:
        skip = ("noop", "UNK", "Um")
        S = entry.splitlines()[0][2:] + " </s>"
        words = S.split()
        edits = entry.splitlines()[1:]

        skip_indices = []
        for edit in edits:
            features = edit[2:].split("|||")
            if features[1] in skip:
                continue
            start, end = features[0].split()
            start, end = int(start), int(end)
            word = features[2]

            if start == end:  # insertion -> deletion
                ptb = ""
                if word in word2ptbs:
                    word2ptbs[word].append(ptb)
                else:
                    word2ptbs[word] = [ptb]
            elif start + 1 == end and word == "":  # deletion -> substitution
                ptb = words[start] + " " + words[start + 1]
                word = words[start + 1]
                if word in word2ptbs:
                    word2ptbs[word].append(ptb)
                else:
                    word2ptbs[word] = [ptb]
                skip_indices.append(start)
                skip_indices.append(start + 1)
            elif start + 1 == end and word != "" and len(word.split()) == 1:  # substitution
                ptb = words[start]
                if word in word2ptbs:
                    word2ptbs[word].append(ptb)
                else:
                    word2ptbs[word] = [ptb]
                skip_indices.append(start)
            else:
                continue

        for idx, word in enumerate(words):
            if idx in skip_indices: continue
            if word in word2ptbs:
                word2ptbs[word].append(word)
            else:
                word2ptbs[word] = [word]

    # pruning
    _word2ptbs = dict()
    for word, ptbs in word2ptbs.items():
        ptb2cnt = Counter(ptbs)

        ptb_cnt_li = []
        for ptb, cnt in ptb2cnt.most_common(len(ptb2cnt)):
            if cnt < min_cnt: break
            ptb_cnt_li.append((ptb, cnt))

        if len(ptb_cnt_li) == 0: continue
        if len(ptb_cnt_li) == 1 and ptb_cnt_li[0][0] == word: continue

        _ptbs = []
        for ptb, cnt in ptb_cnt_li:
            _ptbs.extend([ptb] * cnt)

        _word2ptbs[word] = _ptbs

    return _word2ptbs


def generate_ptbs(path_m2):
    ptbs = make_word2ptbs(path_m2, 4)
    save_obj(ptbs, 'common_errors_dict')

def save_obj(obj, name ):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def main():
        # load config
        parser = argparse.ArgumentParser(description='Building ptbs dictionary')
        parser = load_arguments(parser)
        args = vars(parser.parse_args())
        config = validate_config(args)

        path_m2 = config['path_m2']
        generate_ptbs(path_m2)

if __name__ == '__main__':
        main()
