import re
inf =open('ngram.scores.txt', 'U')

content = inf.read()
matches = re.finditer(r'logprob= (.*?) ', content)

result = [match.group(1) for match in matches]

with open('parsed.txt', 'w') as outf:
    for prob in result:
        outf.write(prob + '\n')
