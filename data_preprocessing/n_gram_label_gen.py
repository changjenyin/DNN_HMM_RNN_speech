import sys

def main (argv):
    if len(argv) != 3:
        print 'Usage: python n_gram_generator path n_gram'
        return
    
    path = argv[1]
    n_gram = int(argv[2])

    out_name = str(n_gram) + '_gram_label.lab'

    with open(path, 'U') as inf:
        with open(out_name, 'w') as outf:
            num_phone = 0
            sentence_now = ''
            speaker_now = ''
            idx_list = {}

            for line in inf:
                frame, idx = line.strip().split(',')
                speaker, sentence, phone = frame.split('_')
                phone = int(phone)

                if sentence_now == '':
                    sentence_now = sentence
                    speaker_now = speaker

                if sentence != sentence_now:
                    for i in range(1, len(idx_list)+1):
                        write_line = speaker_now + '_' + sentence_now + '_' + str(i) + ',' + idx_list[i]
                        outf.write(write_line + '\n')

                    idx_list = {}
                    sentence_now = sentence

                idx_list[phone] = idx

            for i in range(1, len(idx_list)+1):
                write_line = speaker_now + '_' + sentence_now + '_' + str(i) + ',' + idx_list[i]
                outf.write(write_line + '\n')


if __name__ == '__main__':
    main(sys.argv)
