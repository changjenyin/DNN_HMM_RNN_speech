import os

idfile = open('../mfcc/train_sentenceid_final.txt', 'U')
for line in idfile:
    line = line.strip()
    os.system('cp ../wav/' + line + '.wav ../train_wav')
