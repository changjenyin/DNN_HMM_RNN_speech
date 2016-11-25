#!/usr/bin/env python
#Usage: python classify.py
import numpy as np
import os
import sys
import argparse
import glob
caffe_root = '/tmp4/eric11220/caffe/'
sys.path.insert(0, caffe_root + 'python')
import caffe
import numpy as np
import csv

def main(argv):
    parser = argparse.ArgumentParser()
    # Optional arguments
    parser.add_argument(
        "--model_def",
        default="/tmp4/eric11220/caffe/models/feat_to_phone_net/7_3000/cascading/deploy_hw1.prototxt",
        #default="/tmp4/eric11220/caffe/models/feat_to_phone_net/5_2000_1943_drop/deploy.prototxt",
        #default="/tmp4/eric11220/caffe/models/feat_to_phone_net/5_2000_fbank/deploy.prototxt",
        help="Model definition file."
    )
    parser.add_argument(
        "--pretrained_model",
        default="/tmp4/eric11220/caffe/models/feat_to_phone_net/7_3000/cascading/_iter_2500000.caffemodel",
        #default="/tmp4/eric11220/caffe/models/feat_to_phone_net/5_2000_fbank/_iter_900000.caffemodel",
        #default="/tmp4/eric11220/caffe/models/feat_to_phone_net/5_2000_1943_drop/drop_3,5_iter_9500000.caffemodel",
        help="Trained model weights file."
    )
    parser.add_argument(
        "--gpu",
        default=False,
        action='store_true',
        help="Switch for gpu computation."
    )
    parser.add_argument(
        "--file",
        #default="/tmp4/eric11220/MLDS_Final/mfcc/test.ark",
        default="/tmp4/eric11220/MLDS_Final/mfcc/7_gram.ark",
        #default="/tmp4/eric11220/caffe/models/feat_to_phone_net/eval.h5",
        help="Path to testing data"
    )
    parser.add_argument(
        "--batch",
        #default=10,
        default=1,
        help="batch size"
    )
    parser.add_argument(
        "--form",
        default='48',
        help='predict form'
    )
    parser.add_argument(
        "--layer",
        help='layer number'
    )
    args = parser.parse_args()

    # Make classifier
    if args.gpu:
        caffe.set_mode_gpu()
        print 'GPU mode'
    
    net = caffe.Net(args.model_def, args.pretrained_model, caffe.TEST)
    print [(k, v.data.shape) for k, v in net.blobs.items()]
    batch_size = args.batch

    # Read in test data
    test_file = open(args.file, 'r')
    test_lines = test_file.readlines()
    testdata_cnt = len(test_lines)
    print testdata_cnt
    feature_dimension = len(test_lines[0].strip().split(' ')[1:])
    
    testdata = np.zeros((testdata_cnt, feature_dimension))
    frame_ids = []
    for i in xrange(0, testdata_cnt):
        frame_id, features_string = test_lines[i].strip().split(' ', 1)
        frame_ids.append(frame_id)
        features = features_string.split(' ')
        for j in xrange(0, feature_dimension):
            testdata[i][j] = float(features[j])

    # Build label-phone dictionary
    label_phone = {}
    if args.form == '48':
        print 'output from of NN: 48'
        labelFile = '/tmp4/eric11220/MLDS_Final/conf/48.idx-39.phone.map'
    elif args.form == '1943':
        print 'output from of NN: 1943'
        labelFile = '/tmp4/eric11220/MLDS_Final/conf/state_39.phone.map'
    raw_input()

    with open(labelFile, 'U') as mapping:
        for line in mapping:
            label, phone = line.strip().split(' ')
            label_phone[int(label)] = phone
    

    frameid_idx = 0
    idx = 0
    which = 'fc' + str(args.layer)
    with open('/tmp4/eric11220/MLDS_Final/dnn_feats/' + which + '_feature.ark', 'w') as outf:
        while idx < testdata_cnt:   
            out = net.forward()


            #print net.blobs[which].data[0].shape
            feats = net.blobs[which].data[0]
            #raw_input()

            outf.write(frame_ids[frameid_idx])
            for feat in feats:
                outf.write(' ' + str(feat))
            outf.write('\n')

            frameid_idx += 1
            idx += batch_size

if __name__ == '__main__':
    main(sys.argv)
