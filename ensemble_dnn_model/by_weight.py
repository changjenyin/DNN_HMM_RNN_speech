import os
import sys
import csv
import glob
import numpy as np

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


modelCnt = 0
weight = None
with open('model.list', 'U') as inf:
    for line in inf:
        modelCnt += 1 
        model = path + '/' + line.strip()
        net = caffe.Net(prototxt, model, caffe.TEST)
        if weight == None:
            weight = [np.zeros((v[0].data.shape)) for k, v in net.params.items()]

        for w, info in zip(weight, net.params.items()):
            w += info[1][0].data


    net = caffe.Net(prototxt, model, caffe.TEST)
    for w in weight:
        w = w / modelCnt

    for w, info in zip(weight, net.params.items()):
        name = info[0]
        net.params[name][0].data[...] = w

    label_phone = {}
    labelFile = '/tmp4/eric11220/MLDS_Final/conf/48.idx-39.phone.map'
    with open(labelFile, 'U') as mapping:
        for line in mapping:
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
        out = net.forward()

        ans = out['prob'].argmax()
        writer.writerow({'Id':frame_ids[frameid_idx], 'Prediction':label_phone[ans]})
        frameid_idx += 1

        idx += 1

