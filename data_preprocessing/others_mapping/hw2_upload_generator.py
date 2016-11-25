import sys
import re
import csv

def post_process(seq):
    # Remove the lonely char
    smoothed = []
    for i in xrange(1, len(seq) - 1):
        if seq[i] != seq[i - 1] and seq[i] != seq[i + 1]:
            continue
        smoothed.append(seq[i])

    # Trimming
    real_output = []
    real_output.append(smoothed[0])
    current_p = smoothed[0]
    for p in smoothed:
        if p != current_p:
            real_output.append(p)
            current_p = p

    # Remove head and tail 'sil' ('pau' in 60 phones)
    if real_output[0] == 'L':
        real_output.remove(real_output[0])
    if real_output[-1] == 'L':
        real_output.pop()

    real_output = " ".join(real_output) # join list back into string
    return real_output

def main(argv):
    # Process I/O files
    raw_seq_file = open('raw_seq', 'U')
    hw2_upload = open('hw2_upload.csv', 'w')
    fieldnames = ['id', 'phone_sequence']
    writer = csv.DictWriter(hw2_upload, fieldnames=fieldnames)
    writer.writeheader()
    
    # Read in test_sentenceid.txt
    test_sentenceid = open('/tmp3/mlds_hw1/MLDS_HW1_RELEASE_v1/mfcc/test_sentenceid.txt', 'U')
    test_sentenceid_lines = test_sentenceid.readlines()
    sentence_ids = []
    for line in test_sentenceid_lines:
        line = line.strip()
        sentence_ids.append(line)

    lines = raw_seq_file.readlines()
    idx = 0
    for line in lines:
        if line == '\n':
            continue

        # Post process
        raw_seq = line.strip().split(' ')
        seq = post_process(raw_seq)
        seq = seq.split(' ')

        # Map phone-based seq to character-based seq
        seq_chr = []
        for item in seq:
            seq_chr.append(item)
        output_string = ''
        output_string = "".join(seq_chr) # join list back into string

        # Write out the phone_sequence
        writer.writerow({'id':sentence_ids[idx], 'phone_sequence':output_string})
        idx += 1

if __name__ == '__main__':
    main(sys.argv)
