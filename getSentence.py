import sys

if len(sys.argv) != 3:
    print 'Usage: python getSentence.py inFile idx'
    exit()

name = sys.argv[1]
idx  = int(sys.argv[2])

cnt = 0
out  = name + '_' + str(idx)
with open(name, 'U') as inf:
    with open(out, 'w') as outf:
        for line in inf:
            if line == '\n':
                cnt += 1
                if cnt <= idx:
                    continue

            if cnt >= idx:
                outf.write(line)
