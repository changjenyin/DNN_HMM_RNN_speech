# Usage: python trim4WFST.py
import sys

def post_process(seq):
    real_output = []
    real_output.append(seq[0])
    current_p = seq[0]

    # Smoothing & Trimming
    cnt = 0
    for p in seq:
        cnt += 1
        if p != current_p:
            current_p = p
            '''
            if cnt < 3:
                cnt = 0
                continue
            '''

            cnt = 0
            real_output.append(p)

    # Remove head and tail 'sil' ('pau' in 60 phones)
    if real_output[0] == 'sil':
        real_output.remove(real_output[0])
    if real_output[-1] == 'sil':
        real_output.pop()

    real_output = " ".join(real_output) # join list back into string
    return real_output

def main(argv):
    # Process I/O files
    #raw_seq_file = open('/home/master/03/eric11220/Deep/final/HMM/raw_seq/raw_seq_1000best_73000.txt', 'U')
    raw_seq_file = open('/home/master/03/eric11220/Deep/final/kaldi-trunk/egs/timit/s5/raw_seq_timit_text.txt', 'U')
    seq_file = open('/home/master/03/eric11220/Deep/final/Lexicon_WFST/seq_timit_text.txt', 'w')
    
    # Build map_48_60
    map_48_60 = {}
    map_60_48_39 = open('/tmp4/eric11220/MLDS_Final/conf/phones.60-48-39.map', 'U')
    for line in map_60_48_39:
        phone_60_48_39 = line.strip().split('\t')
        map_48_60[phone_60_48_39[1]] = phone_60_48_39[0]

    # Trim each seq
    phone_seq_list = []
    lines = raw_seq_file.readlines()
    for line in lines:
        seq_60 = []
        if line == '<s>\n':
            phone_seq_list = []
            seq_file.write('<s>\n')
            continue
        
        seq_48 = line.strip().split(' ')
        for item in seq_48:
            #seq_60.append(map_48_60[item]) # Map 48 to 60
            seq_60.append(item) # Map 48 to 60

        phone_seq = post_process(seq_60)
        if phone_seq in phone_seq_list:
            continue
        phone_seq_list.append(phone_seq)
        seq_file.write(phone_seq + '\n')

if __name__ == '__main__':
    main(sys.argv)
