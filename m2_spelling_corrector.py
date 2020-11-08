# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 09:02:45 2020

@author: santiago
"""


import argparse
from utils.misc import validate_config

def load_arguments(parser):
    parser.add_argument('--path_m2', type=str, default='None', help = 'M2 filepath')
    parser.add_argument('--path_src', type=str, default='None', help = 'Source filepath')
    return parser



def get_all_coder_ids(edits):
    coder_ids = set()
    for edit in edits:
        edit = edit.split("|||")
        coder_id = int(edit[-1])
        coder_ids.add(coder_id)
    coder_ids = sorted(list(coder_ids))
    return coder_ids

def m2_to_parallel(m2_file, cor, drop_unchanged_samples, all):
    #Given an M2 file and a source filepath this function will produce a file with the spelling and punctuation errors corrected
    cor_fout = open(cor, 'w')

    # Do not apply edits with these error types
    spell_punct = {'R:SPELL', 'M:PUNCT'}
    entries = open(m2_file).read().strip().split("\n\n")
    for entry in entries:
        lines = entry.split("\n")
        ori_sent = lines[0][2:]  # Ignore "S "
        cor_tokens = lines[0].split()[1:]  # Ignore "S "
        edits = lines[1:]
        offset = 0

        coders = get_all_coder_ids(edits) if all == True else [0]
        for coder in coders:
            for edit in edits:
                edit = edit.split("|||")
                if edit[1] not in spell_punct: continue
                coder_id = int(edit[-1])
                if coder_id != coder: continue  # Ignore other coders
                span = edit[0].split()[1:]  # Ignore "A "
                start = int(span[0])
                end = int(span[1])
                cor = edit[2].split()
                cor_tokens[start + offset:end + offset] = cor
                offset = offset - (end - start) + len(cor)

            cor_sent = " ".join(cor_tokens)
            if drop_unchanged_samples and ori_sent == cor_sent:
                continue

            cor_fout.write(cor_sent + "\n")



def main():
        # load config
        parser = argparse.ArgumentParser(description='Building vocab')
        parser = load_arguments(parser)
        args = vars(parser.parse_args())
        config = validate_config(args)

        path_m2 = config['path_m2']
        path_src = config['path_src']
        print('2')
        m2_to_parallel(path_m2, path_src, False, True)

if __name__ == '__main__':
        main()
