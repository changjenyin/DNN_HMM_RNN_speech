inf = open('sentences_bad.txt', 'U')
outf = open('sentences.txt', 'w')

for line in inf:
    line = line.strip().split(' ')
    sen = []
    for word in line:
        if word == 'use~':
            word = 'use'
        elif word == 'i\'':
            word = 'i'
        elif word == 'he\'':
            word = 'he'
        elif word == '\'all':
            word = 'all'
        elif word == 'boat\'':
            word = 'boat'
        elif word == 'live~':
            word = 'live'
        elif word == 'earth\'':
            word = 'earth'
        elif word == 'she\'':
            word = 'she'
        elif word == 'we\'':
            word = 'we'
        elif word == 'read~v_pres':
            continue
        sen.append(word)

    sen = ' '.join(sen)
    outf.write(sen + '\n')
