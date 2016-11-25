infile = open('../mfcc/train.ark_stdized', 'U')
lines = infile.readlines()
outfile = open('../mfcc/train_sentenceid_final.txt', 'w')

# current_s is the first sentence
first_frameid, first_tmp = lines[0].strip().split(' ', 1)
speaker, sentence, frame = first_frameid.split('_')
current_s = speaker + '_' + sentence

for line in lines[1:]:
    frameid, tmp = line.strip().split(' ', 1)
    speaker, sentence, frame = frameid.split('_')
    sentence = speaker + '_' + sentence

    if sentence != current_s:
        outfile.write(current_s + '\n')
        current_s = sentence

# the last sentence
outfile.write(current_s + '\n')
