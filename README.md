# DNN_HMM_RNN_speech
"Automated Speech Recognition System" in Machine Learning and Having it Deep and Structured, Spring 2015

# How to train caffe
./build/tools/caffe.bin train -solver models/finetune_bloody_style/solver.prototxt -weights models/bvlc_reference_caffenet/bvlc_reference_caffenet.caffemodel -gpu 0     

# Use rnnlm to score which sentence has the highest prob
./rnnlm -rnnlm ../models/ptb.model-1.hidden100.class100.txt -test my_nbest.txt -nbest -debug 0 > my_scores.txt     
