# Usage: python rescore.py [rnn_model_file]
# coding='utf8'
import os
import sys
import re
import enchant
import csv

def main(argv):
    # Process I/O files
    sentences_file = '/tmp4/eric11220/sentences_timit_text.txt'
    sentences = open(sentences_file, 'U')
    junk, postfix = os.path.splitext(os.path.basename(sentences_file))[0].split('_', 1) 
    outfile = open("middle/output_without_id" + postfix + ".txt", 'w')
    best_s_outfile = open("middle/best_sentence_" + postfix, 'w')
    combined_outfile = open("csv/" + postfix + ".csv", 'w')

    rnn_model_file = '/tmp4/eric11220/rnn/simple-examples/models/3696.model.hidden100.class50.txt'
    rnnpath = "/tmp4/eric11220/rnn/simple-examples/rnnlm-0.2b"

    # Generate non-overlap tmp files
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
    
    # Build up timit.chmap dictionary
    checker = enchant.Dict("en_US")
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
            os.system(rnnpath + "/rnnlm -test " + tmp_n_sentences_file + " -rnnlm " + rnn_model_file + " -nbest -debug 0 > " + tmp_n_scores_file)
     
            # Read in the best sentence
            n_sentences = open(tmp_n_sentences_file, 'U')
            n_scores = open(tmp_n_scores_file, 'U')
            best_score = float('-inf')
            best_sentence = ''
            for sentence_line, score_line in zip(n_sentences, n_scores):
                sentence = sentence_line.strip().split(' ')
                score = float(score_line)     
                # If meet word not in Lexicon and dictionary, give penalty to that sentence
                '''
                for word in sentence:
                    try:
                        tmp = en_ch_dict[word]
                    except:
                        score += -10
                '''
                '''
                for word in sentence:
                    if not checker.check(word):
                        score += -10
                '''

                if score > best_score:
                    best_score = score
                    best_sentence = sentence
     
            # Map the best sentence to character-based sentence(Skip if not in dictionary)
            ch_sentence = ''
            output_string_list = []
            for word in best_sentence:
                try:
                   output_string_list.append(word)
                   ch_sentence += en_ch_dict[word]
                except:
                    continue
            idx += 1
            output_string = " ".join(output_string_list)
            best_s_outfile.write(str(idx) + ' ' + output_string + '\n')
            outfile.write(ch_sentence + '\n')
            print idx, output_string

            # Close files, open new tmp_n_sentences
            n_sentences.close()
            n_scores.close()
            tmp_n_sentences = open(tmp_n_sentences_file, 'w')
            continue
        
        tmp_n_sentences.write(line)
    
    # Combine outfile with sentence id
    best_s_outfile.close()
    outfile.close()

    sentence_file = open("middle/output_without_id" + postfix + ".txt", 'U')
    id_file = open('/tmp4/eric11220/MLDS_Final/mfcc/test_sentenceid_final.txt', 'U')
    fieldnames = ['id', 'sequence']
    writer = csv.DictWriter(combined_outfile, fieldnames=fieldnames)
    writer.writeheader()
    for id_line, sentence_line in zip(id_file, sentence_file):
        id_line = id_line.strip()
        sentence_line = sentence_line.strip()
        writer.writerow({'id': id_line, 'sequence': sentence_line})
    
if __name__ == "__main__":
    main(sys.argv)
