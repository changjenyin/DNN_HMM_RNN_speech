import sys
import os

if len(sys.argv) != 2:
    print 'Usage: python getPhone.py'
    exit()
folder = sys.argv[1]


sents = []
with open('/tmp4/eric11220/MLDS_Final/mfcc/test_sentenceid_final.txt') as inf:
    for line in inf:
        sent = line.strip()
        sents.append(sent)

sixty_48 = {}
with open('/tmp4/eric11220/MLDS_Final/conf/phones.60-48-39.map', 'U') as inf:
    for line in inf:
        sixty, forty_eight, thirty_nine = line.strip().split('\t')
        sixty_48[sixty] = forty_eight

with open('std_ans', 'w') as outf:
    for root, dirs, files in os.walk(folder):
        for f in files:
            name, ext = os.path.splitext(f)

            if ext != '.phn':
                continue

            name = root.rsplit('/', 1)[1] + '_' + name
            if name not in sents:
                continue
    
            outf.write(name + ' ')
            with open(root + '/' + f, 'U') as inf:
                for line in inf:
                    try:
                        label = sixty_48[line.strip().rsplit(' ', 1)[1]]
                    else:
                        label = line.strip().rsplit(' ', 1)[1]

                    outf.write(label + ' ')
                outf.write('\n')

