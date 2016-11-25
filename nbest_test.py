import sys
import re
import csv

def post_process(seq):
    # Trimming
    real_output = []
    real_output.append(seq[0])
    current_p = seq[0]
    for p in seq:
        if p != current_p:
            real_output.append(p)
            current_p = p

    # Remove head and tail 'sil' ('pau' in 60 phones)
    if real_output[0] == 'sil':
        real_output.remove(real_output[0])
    if real_output[-1] == 'sil':
        real_output.pop()

    real_output = " ".join(real_output) # join list back into string
    return real_output

def main(argv):
    # Process I/O files
    raw_seq_file = open('/home/master/03/eric11220/Deep/final/HMM/raw_seq.txt', 'U')
    hw2_upload = open('hw2_upload.csv', 'w')
    fieldnames = ['id', 'phone_sequence']
    writer = csv.DictWriter(hw2_upload, fieldnames=fieldnames)
    writer.writeheader()
    
    # Build map_48_39
    map_48_39 = {}
    map_60_48_39 = open('/tmp4/eric11220/MLDS_Final/conf/phones.60-48-39.map', 'U')
    for line in map_60_48_39:
        line = line.strip().split('\t')
        map_48_39[line[1]] = line[2]

    # Build map_48_chr
    map_48_chr = {}
    map_48_idx_chr = open('/tmp4/eric11220/MLDS_Final/conf/48_idx_chr.map', 'U')
    for line in map_48_idx_chr:
        line = line.strip()
        line = re.split('\t|      ', line)
        map_48_chr[line[0]] = line[2]
    
    # Read in test_sentenceid.txt
    test_sentenceid = open('/tmp4/eric11220/MLDS_Final/mfcc/test_sentenceid_7gram.txt', 'U')
    test_sentenceid_lines = test_sentenceid.readlines()
    sentence_ids = []
    for line in test_sentenceid_lines:
        line = line.strip()
        sentence_ids.append(line)

    n = int(sys.argv[1])
    lines = raw_seq_file.readlines()
    idx = 0
    for i in xrange(n - 1, len(lines), n + 1):
        # Post process
        raw_seq = lines[i].strip().split(' ')
        seq = post_process(raw_seq)
        seq = seq.split(' ')

        # Map phone-based seq to character-based seq
        seq_chr = []
        for item in seq:
            seq_chr.append(map_48_chr[map_48_39[item]])
        output_string = ''
        output_string = "".join(seq_chr) # join list back into string

        # Write out the phone_sequence
        writer.writerow({'id':sentence_ids[idx], 'phone_sequence':output_string})
        idx += 1

if __name__ == '__main__':
    main(sys.argv)
