#!/usr/bin/env python
# coding=utf-8

import sys
import csv

def trans2seq(openfile,writefile):
    try:
        of = open(openfile,'r')
    except IOError as err:
        print 'file open error: ',err
    wf = open(writefile,'w')
    wf.write('id,phone_sequence\n')
    ofcsv = csv.reader(of)
    ofcsv.next()
    seq = []
    speaker = []
    head = 1
    for i in xrange(180406):
        pointer = ofcsv.next()
        nextspeaker = pointer[0].split('_')[0:2]
        if speaker == []:
            speaker = nextspeaker

        if speaker == nextspeaker:
            if pointer[1]=='L' and head ==1:
                continue
            else:
                if len(seq) == 0:
                    seq.append(pointer[1])
                else:
                    if pointer[1] != seq[-1]:
                        seq.append(pointer[1])
                head = 0
        else:
            if seq[-1] == 'L':
                seq.pop(-1)
            wf.write('_'.join(speaker)+','+''.join(seq))
            wf.write('\n')
            speaker = nextspeaker
            seq = []
            head = 1
            if pointer[1]=='L':
                continue
            else:
                seq.append(pointer[1])
                head = 0

    if seq[-1] == 'L':
        seq.pop(-1)
    wf.write('_'.join(speaker)+','+''.join(seq))
    wf.write('\n')

    of.close()
    wf.close()
    return 1

if __name__ == '__main__':
    openfile = sys.argv[1]
    writefile = sys.argv[2]
    a = trans2seq(openfile,writefile)
    if a:
        print 'Successfully Done!'
    else:
        print 'Something Wrong!'

