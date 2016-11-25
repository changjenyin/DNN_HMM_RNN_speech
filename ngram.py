# Usage: python rescore.py [rnn_model_file]
# coding='utf8'
import os
import sys
import re

def main(argv):
    # Process I/O files
    sentences_file = '/tmp4/eric11220/sentences_100_no_smooth_500.txt'
    sentences = open(sentences_file, 'U')
    outfile = open("middle/output_without_id_100_no_smooth_500ngram.txt", 'w')

    idx = 0
    tmp_n_sentences_file = sentences_file + str(idx) + '_tmp_n_sentences.txt'
    tmp_n_scores_file = sentences_file + str(idx) + '_tmp_n_scores.txt'
    while os.path.isfile(tmp_n_sentences_file):
        tmp_n_sentences_file = sentences_file + str(idx) + '_tmp_n_sentences.txt'
        tmp_n_scores_file = sentences_file + str(idx) + '_tmp_n_scores.txt'
        idx += 1

    os.system('rm ' + tmp_n_sentences_file)
    os.system('rm ' + tmp_n_scores_file)
    os.system("sed -i -- ':a;N;$!ba;s/\\n\{2,\}/\\n/g' " + sentences_file)
    rnn_model_file = '/tmp4/eric11220/rnn/simple-examples/models/swb.ngram.model'
    rnnpath = "/tmp4/eric11220/rnn/simple-examples/rnnlm-0.2b"
    
    # Build up timit.chmap dictionary
    timit_chmap = open('/tmp4/eric11220/MLDS_Final/conf/timit.chmap', 'r')
    en_ch_dict = {}
    for line in timit_chmap:
        line_list = line.strip().split(' ') # remove \n, ' '
        line_en_ch = line_list[0].split('\t') # remove \t to separate en-ch
        en_ch_dict[line_en_ch[0]] = line_en_ch[1]

    # Chunk n sentences for tmp
    idx = 0
    tmp_n_sentences = open(tmp_n_sentences_file, 'w')
    for line in sentences:
        if(line == '<s>\n'):
            tmp_n_sentences.close()
            sort_file = tmp_n_sentences_file + '_sort.txt'
            os.system("sort " + tmp_n_sentences_file + " | uniq > " + sort_file) 
            os.system('mv ' + sort_file + ' ' + tmp_n_sentences_file)
            os.system("~/Deep/final/srilm-1.5.10/i686-m64/ngram -lm /tmp4/eric11220/rnn/simple-examples/models/swb.ngram.model -ppl " + tmp_n_sentences_file + " -debug 1 > " + tmp_n_scores_file)

            # Parse logp
            inf = open(tmp_n_scores_file, 'U')
            content = inf.read()
            matches = re.finditer(r'logprob= (.*?) ', content)
            result = [match.group(1) for match in matches]

            with open(tmp_n_scores_file + '_parsed.txt', 'w') as outf:
                for prob in result[:-1]:
                    outf.write(prob + '\n')
     
            # Read in the best sentence
            n_sentences = open(tmp_n_sentences_file, 'U')
            n_scores = open(tmp_n_scores_file + '_parsed.txt', 'U')
            best_score = float('-inf')
            best_sentence = ''
            for sentence_line, score_line in zip(n_sentences, n_scores):
                sentence = sentence_line.strip().split(' ')
                score = float(score_line)     
                # If meet word not in dictionary, give penalty to that sentence
                #for word in sentence:
                #    try:
                #        tmp = en_ch_dict[word]
                #    except:
                #        score *= -10

                if score > best_score:
                    best_score = score
                    best_sentence = sentence
     
            # Map the best sentence to character-based sentence(Skip if not in dictionary)
            ch_sentence = ''
            idx += 1
            print idx, best_sentence
            for word in best_sentence:
                try:
                   ch_sentence += en_ch_dict[word]
                except:
                    continue
            outfile.write(ch_sentence + '\n')

            # Close files, open new tmp_n_sentences
            n_sentences.close()
            n_scores.close()
            tmp_n_sentences = open(tmp_n_sentences_file, 'w')
            continue
        
        tmp_n_sentences.write(line)

if __name__ == "__main__":
    main(sys.argv)
