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
        # 48 phone -> 48 idx
        phone_id_48 = {}
        id_phone_48 = {}
        with open('/tmp4/eric11220/MLDS_Final/conf/48-idx.map', 'U') as inf:
            for line in inf:
                first, sec = line.strip().split(' ')
                phone_id_48[first] = int(sec)
                id_phone_48[int(sec)] = first
    else:
        labelFile = '/tmp4/eric11220/MLDS_Final/conf/48.idx-39.phone.map'

    # ori -> 48.idx
    with open(labelFile, 'U') as mapping:
        for line in mapping:
            if form == '1943':
                #label, tmp, phone = line.strip().split('\t')
                label, phone, tmp = line.strip().split('\t')
            else:
                label, phone = line.strip().split(' ')
            label_phone[int(label)] = phone
    
    # Classify to generate frameid,phone file
    frameid_phone = open('ensemble_frameid_phone_prob.csv', 'w')
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
    #while idx < 1000:   
        outs = [net.forward() for net in nets]

        # Add all prob together
        probs = sum([out['prob'] for out in outs])
        #probs = probs / np.sum(probs)

        geoProb = np.ones(1943)
        answers = np.zeros(48) 
        for prob in probs:
            geoProb *= prob

        # Transform to 48 idx and add prob
        if form == '1943':
            for i in range(1943):
                answers[phone_id_48[label_phone[i]]] += geoProb[i]

        answers = answers / np.sum(answers)
        ans = answers.argmax()

        writer.writerow({'Id':frame_ids[frameid_idx], 'Prediction':id_phone_48[ans]})
        frameid_idx += 1

        idx += 1

