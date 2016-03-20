f = open('амхарское письмо.txt', 'r', encoding = 'utf-8')

lettersInLine = []
vowels = []
x = 1
d = {}
z = 0

for line in f:
    if z < 1:
        vowels = line.split()
        z += 1
    else:
        lettersInLine = line.split()
        for letter in lettersInLine[1:]:
            if x < 8:
                key = lettersInLine[x]
                d[key] = lettersInLine[0] + vowels[x - 1]
                x += 1
            else:
                x = 1

f.close()


text = open('amharwiki.txt', 'r', encoding = 'utf-8')
newFile = open('wiki.txt', 'w', encoding = 'utf-8')

for line in text:
    for letter in line:
        if letter in d.keys():
            letter = d[letter]
            newFile.write(letter)
        else:
            newFile.write(letter)

newFile.close()
text.close()
