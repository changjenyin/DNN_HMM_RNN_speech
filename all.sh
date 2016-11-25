n = $1

#echo -e '\n15-frame mfcc -> frameid_phone.csv...'
#python classify.py
#echo -e '\nframeid_phone.csv -> n_seq.txt'
#python phone_to_seq.py

echo -e '\n15-frame mfcc -> raw_seq.txt'
python ../HMM/viterbi.py

echo -e '\nraw_seq.txt -> n_seq.txt'
python trim4WFST.py

echo -e '\nn_seq.txt -> sentences.txt(n1 n2 n3...)'
python WFST_exe.py $n

echo -e '\nsentences.txt -> output_without_id.txt'
python rescore.py

echo -e '\noutput_without_id.txt + /tmp4/eric11220/MLDS_Final/mfcc/test_sentenceid.txt -> upload.csv'
python combine_id_sentence.py
