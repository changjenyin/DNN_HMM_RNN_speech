import re
idxPhoneDic = {}
with open('/tmp4/eric11220/MLDS_Final/conf/48-idx.map', 'U') as inf:
    for line in inf:
        phone, idx = line.strip().split(' ')
        idxPhoneDic[int(idx)] = phone

        
theirMapDic = {}
with open('/tmp4/eric11220/MLDS_Final/conf/48_idx_chr.map', 'U') as inf:
    for line in inf:
        line = line.strip()
        line = re.split('\t| +', line)
        first, sec, third = line
        theirMapDic[first] = int(sec)

outf = open('predict_results', 'w')
with open('7models.txt', 'U') as inf:
    inf.readline()
    for line in inf:
        idx, label = line.strip().split(',')
        outf.write(str(theirMapDic[label]) + '\n')


