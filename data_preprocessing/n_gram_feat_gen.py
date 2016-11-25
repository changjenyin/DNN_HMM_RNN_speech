import sys

def main (argv):
    if len(argv) != 3:
        print 'Usage: python n_gram_generator path n_gram'
        return
    
    path = argv[1]
    n_gram = int(argv[2])

    out_name = str(n_gram) + '_gram.ark'

    feat_dim = 0
    with open(path, 'U') as inf:
        with open(out_name, 'w') as outf:
            num_phone = 0
            sentence_now = ''
            speaker_now = ''
            feature_list = {}

            for line in inf:
                frame, tmp = line.strip().split(' ', 1)
                features = tmp.split(' ')

                speaker, sentence, phone = frame.split('_')
                phone = int(phone)

                if sentence_now == '':
                    sentence_now = sentence
                    speaker_now = speaker

                if sentence != sentence_now:
                    for i in range(1, len(feature_list)+1):
                        lowbound    = i - n_gram
                        downPadding = 0
                        if lowbound < 1:
                            downPadding = 1 - lowbound
                            lowbound    = 1

                        highbound = i + n_gram + 1 # Due to range 
                        upPadding = 0
                        if highbound > len(feature_list) + 1:
                            upPadding = highbound - (len(feature_list) + 1)
                            highbound = len(feature_list) + 1

                        # Down-padding zero
                        n_gram_feature = []
                        for j in range(0, downPadding):
                            n_gram_feature = n_gram_feature + zeros
                        for j in range(lowbound, highbound):
                            n_gram_feature = n_gram_feature + feature_list[j]    
                        for j in range(0, upPadding):
                            n_gram_feature = n_gram_feature + zeros

                        write_line = speaker_now + '_' + sentence_now + '_' + str(i)
                        for feature in n_gram_feature:
                            write_line = write_line + ' ' + str(feature)

                        outf.write(write_line + '\n')

                    feature_list = {}
                    sentence_now = sentence
                    speaker_now  = speaker

                if feat_dim == 0:
                    feat_dim = len(features)
                    zeros    = [0.0] * feat_dim
                feature_list[phone] = features

            # Taking care of the last sentence
            for i in range(1, len(feature_list)+1):
                lowbound    = i - n_gram
                downPadding = 0
                if lowbound < 1:
                    downPadding = 1 - lowbound
                    lowbound    = 1

                highbound = i + n_gram + 1 # Due to range 
                upPadding = 0
                if highbound > len(feature_list) + 1:
                    upPadding = highbound - (len(feature_list) + 1)
                    highbound = len(feature_list) + 1

                # Down-padding zero
                n_gram_feature = []
                for j in range(0, downPadding):
                    n_gram_feature = n_gram_feature + zeros
                for j in range(lowbound, highbound):
                    n_gram_feature = n_gram_feature + feature_list[j]    
                for j in range(0, upPadding):
                    n_gram_feature = n_gram_feature + zeros

                write_line = speaker_now + '_' + sentence_now + '_' + str(i)
                for feature in n_gram_feature:
                    write_line = write_line + ' ' + str(feature)

                outf.write(write_line + '\n')

if __name__ == '__main__':
    main(sys.argv)
