# Usage: python phone_to_seq.py
# frameid_phone.csv -> raw_seq.txt
import sys

def post_process(seq):
    # Smoothing
    #seq = seq.strip().split(' ') # since string is immutable, do it in list
    #for i in xrange(1, len(seq) - 2):
    #    if seq[i - 1] == seq[i + 1] and seq[i] != seq[i - 1]:
    #        seq[i] = seq[i - 1]

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
    frameid_phone_file = open('frameid_phone.csv', 'U')
    seq_file = open('/home/master/03/eric11220/Deep/final/HMM/raw_seq.txt', 'w')

    # Get first sentence for current_s
    lines = frameid_phone_file.readlines()
    frameid, phone = lines[1].strip().split(',', 1)
    speaker, sentence, tmp = frameid.split('_')
    current_s = speaker + '_' + sentence

    # Combine frames for each sentence
    seq = ''
    for line in lines[1:]: # remove header
        frameid, phone = line.strip().split(',', 1)
        speaker, sentence, tmp = frameid.split('_')
        sentence = speaker + '_' + sentence

        # When meet other sentence, trim and write seq to output file
        if sentence != current_s:
            seq_file.write(seq + '\n')
            current_s = sentence
            seq = '' 
            continue

        seq += phone + ' '

    # Last sentence
    seq_file.write(seq + '\n')

if __name__ == '__main__':
    main(sys.argv)
