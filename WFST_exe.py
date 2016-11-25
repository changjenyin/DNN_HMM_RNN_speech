import os
import sys

def main(argv):
    # Process I/O files
    seq_file = 'seq_timit_text.txt'
    tmp_file = seq_file + '_tmp.txt'
    tmp_sentence_file = seq_file + '_sentence.txt'

    junk, postfix = os.path.splitext(os.path.basename(seq_file))[0].split('_', 1)
    seqs = open('/home/master/03/eric11220/Deep/final/Lexicon_WFST/' + seq_file, 'U')
    n_sentences = open('/tmp4/eric11220/sentences_' + postfix + '.txt', 'w')
    n_best = sys.argv[1]

    idx = 0
    for line in seqs:
        # After a bunch of n-sequences, output a '\n'
        if line == '\n':
            continue
        if line == '<s>\n':
            n_sentences.write('<s>\n')
            continue

        # Generate a tmp file for each seq
        tmp = open('/home/master/03/eric11220/Deep/final/Lexicon_WFST/' + tmp_file, 'w')
        tmp.write(line)
        tmp.close()
        idx += 1
        print idx, line

        # Run WFST
        os.chdir('/home/master/03/eric11220/Deep/final/Lexicon_WFST/')
        os.system('./run.sh ' + tmp_file + ' ' + n_best + ' > ' + tmp_sentence_file)

        # Write each sentence for RNNLM
        tmp_sentence = open(tmp_sentence_file, 'U')
        for line in tmp_sentence:
            n_sentences.write(line)

    n_sentences.write('<s>\n')
        
if __name__ == '__main__':
    main(sys.argv)
