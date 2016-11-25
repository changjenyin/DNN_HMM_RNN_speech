import os
import sys
import csv
import glob
import numpy as np
from statistics import mode
from collections import Counter

caffe_root = '/tmp4/eric11220/caffe/'
sys.path.insert(0, caffe_root + 'python')
import caffe

if len(sys.argv) != 2:
    print 'Usage: python by_weight path'
    exit()

path = sys.argv[1]
prototxt = path + '/deploy_hw1.prototxt'

if '1943' in path:
    form = '1943'
else:
    form = '48'

nets = []
with open('model.list', 'U') as inf:
    for line in inf:
        model = path + '/' + line.strip()
        net = caffe.Net(prototxt, model, caffe.TEST)
        nets.append(net)

    label_phone = {}
    if form == '1943':
        labelFile = '/tmp4/eric11220/MLDS_Final/conf/state_48_39.map'
    else:
        labelFile = '/tmp4/eric11220/MLDS_Final/conf/48.idx-39.phone.map'

    with open(labelFile, 'U') as mapping:
        for line in mapping:
            if form == '1943':
                #label, tmp, phone = line.strip().split('\t')
                label, phone, tmp = line.strip().split('\t')
            else:
                label, phone = line.strip().split(' ')
            label_phone[int(label)] = phone
    
    # Classify to generate frameid,phone file
    frameid_phone = open('ensemble_frameid_phone.csv', 'w')
    writer = csv.DictWriter(frameid_phone, fieldnames=['Id', 'Prediction'])
    writer.writeheader()

    test_file = open("/tmp4/eric11220/MLDS_Final/mfcc/hw1_test_7gram.ark", 'U')
    test_lines = test_file.readlines()
    testdata_cnt = len(test_lines)
    feature_dimension = len(test_lines[0].strip().split(' ')[1:])
    frame_ids = []
    for i in xrange(0, testdata_cnt):
        frame_id, features_string = test_lines[i].strip().split(' ', 1)
        frame_ids.append(frame_id)

    frameid_idx = 0
    idx = 0
    while idx < testdata_cnt:   
        outs = [net.forward() for net in nets]

        # Add all prob together
        answers = sum([out['prob'] for out in outs])
        answers = answers / np.sum(answers)
        ans = answers.argmax()

        # Voting
        #answers = [out['prob'].argmax() for out in outs]
        #try:
        #    ans = mode(answers)
        #except:
        #    tmp = Counter(answers).most_common()
        #    ans = tmp[0][0]

        writer.writerow({'Id':frame_ids[frameid_idx], 'Prediction':label_phone[ans]})
        frameid_idx += 1

        idx += 1

