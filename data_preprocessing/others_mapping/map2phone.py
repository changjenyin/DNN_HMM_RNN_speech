import sys

fff = open(sys.argv[3],'r')
letter_array = {}
letter_reverse = {}
def get_letter_array():
    with open('48_idx_chr.map','r') as f:
        i = 0
        for data in f:
            letter_array.setdefault(i,data.split()[2])
            letter_reverse.setdefault(data.split()[0],i)
            i += 1
get_letter_array()
    
fw = open(sys.argv[1],'w')
with open(sys.argv[2],'r') as f:
    fw.write('Id,Prediction\n')
    for data in f:
        fw.write(fff.readline().split(' ')[0]+','+letter_array[int(data.strip().split()[0])]+'\n')
fw.close()
