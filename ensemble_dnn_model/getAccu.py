import os 

os.system('rm -rf test_accu/result.txt')
for result in os.listdir('test_accu'):
    corCnt = 0
    with open('/tmp4/eric11220/MLDS_Final/label/small.lab') as ans:
        inFile = 'test_accu/' + result
        inf = open(inFile, 'U') 
        inf.readline()

        for line in ans:
            idxCor, phoneCor = line.strip().split(',')
            try:
                idx,    phone    = inf.readline().strip().split(',')
            except:
                print result

            if phoneCor == phone:
                corCnt += 1

        inf.close()
        accu = float(corCnt) / 50000

        with open('test_accu/result.txt', 'a') as outf:
            outf.write(result + ': ' + str(accu) + '\n')

