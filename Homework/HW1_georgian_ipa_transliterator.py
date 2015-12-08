F = open('georgian alphabet table.csv','r', encoding = 'utf-8')   

columns = []
d = {}

for line in F:
    columns = line.split(',')
    d.setdefault(columns[0], []).append(columns[2])

F.close()

f = open('georgian text M&M.txt', 'r', encoding = 'utf=8')

newFile = open('ipa.txt', 'w', encoding = 'utf-8')

for line in f:
    line = line.replace('\ufeff', '')
    for letter in line:
        if letter in d.keys():
            letter = ''.join(d[letter])
        newFile.write(letter)


f.close()
newFile.close()

