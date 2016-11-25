import sys
import numpy as np

if len(sys.argv) != 3:
    print 'Usage python standardization.py std_mean_file file'
    exit()

mean_std = sys.argv[1]
f = sys.argv[2]

inf = open(mean_std, 'U')
mean= inf.readline().strip().split(' ')
std = inf.readline().strip().split(' ') 
inf.close()

#Create standardized file
with open(f, 'U') as inf:
    with open(f+'_stdized', 'w') as outf: 
        for line in inf:
            line = line.strip()
            idx, other = line.split(' ', 1)
            feats = other.split(' ')
            for i in range(0, len(feats)):
                feats[i] = (float(feats[i]) - float(mean[i])) / float(std[i])

            buf = idx
            for feat in feats:
                buf = buf + ' ' + str(feat)
    
            outf.write(buf + '\n')
       

