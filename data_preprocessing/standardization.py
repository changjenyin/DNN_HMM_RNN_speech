import sys
import numpy as np

if len(sys.argv) != 2:
    print 'Usage python standardization.py file'
    exit()

f = sys.argv[1]

# compute mean and std
all_idx   = []
all_feats = []
with open(f, 'U') as inf:
    for line in inf:
        line = line.strip()
        idx, other = line.split(' ', 1)
        all_idx.append(idx)

        feats = other.split(' ')
        all_feats.append(feats)

all_feats = np.asarray(all_feats, dtype=np.float32)
std  = np.std(all_feats, axis=0)
mean = np.mean(all_feats, axis=0)

# Record down mean and std for use on testing data
with open(f+'_std&mean', 'w') as outf:
    for val in mean:
        outf.write(str(val) + ' ')
    outf.write('\n')
    for val in std:
        outf.write(str(val) + ' ')
    outf.write('\n')

all_feats = (all_feats - mean) / std

#Create standardized file
with open(f+'_stdized', 'w') as outf: 
    for idx, feats in zip(all_idx, all_feats):
        # append idx back 
        buf = idx
        for feat in feats:
            buf = buf + ' ' + str(feat)

        outf.write(buf + '\n')
       

