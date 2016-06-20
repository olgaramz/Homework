import os
import re

text = []

class Disambiguator(object):
    def __init__(self):
        self.frequent = {}
        self.bigrams = []
    def search(self, text): 
        for index, value in enumerate(text):
            m = re.search('{(\w+)=PR=}', value)
            if m != None:
                prep = m.group(1)
                nxt = text[index+1]
                n = re.search('{\w+=(S(PRO)?|A(PRO|NUM)?).+}', nxt)
                if n != None:
                    grammar = nxt.split('|')
                    for i in grammar:
                        n = re.search('=([а-я]{1,3}),', i)
                        if n != None:
                            case = n.group(1)
                            bigram = prep + '\t' + case
                            self.bigrams.append(bigram)
        return self.bigrams
    def frequency(self, bigrams):
        for bigram in bigrams:
            if bigram in self.frequent:                         
                self.frequent[bigram] += 1
            else:
                self.frequent[bigram] = 1
        return self.frequent

class Cleaner(Disambiguator):
    def __init__ (self):
        self.cleanedText = []
    def remover(self, text, frequent):
        for index, value in enumerate(text):
            m = re.search('{(\w+)=PR=}', value)
            self.cleanedText.append(value)
            if m != None:
                prep = m.group(1)
                nxt = text[index+1]
                n = re.search('(.+?{\w+)(=(S(PRO)?|A(PRO|NUM)?).+)}', nxt)
                if n != None:
                    word = n.group(1)
                    gramcat = n.group(2)
                    grammar = gramcat.split('|')
                    for i in grammar:
                        o = re.search('=([а-я]{1,3}),', i)
                        if o != None:
                            case = o.group(1)
                            bigram = prep + '\t' + case
                            if bigram in frequent:
                                if frequent[bigram] < 10:
                                    grammar.remove(i)
                                else:
                                    pass
                    gramstr = ' '.join(grammar)
                    word += gramstr
                    self.cleanedText.append(word)
                    text.remove(text[index+1])
            else:
                continue
        return self.cleanedText
      
      
dis = Disambiguator()

filename = 'C:\\Users\\Asus\\Desktop\\OOP\\testcorpus.txt'
command = 'C:\\mystem.exe -cid ' + filename + ' C:\\Users\\Asus\\Desktop\\OOP\\testout.txt'
os.system(command)
        
with open('C:\\Users\\Asus\\Desktop\\OOP\\testout.txt', 'r', encoding='utf-8') as f:
    for line in f:
        words = line.split(' ')
        for word in words:
            text.append(word)
d = dis.search(text)
bd = dis.frequency(d)

cln = Cleaner()

txt = cln.remover(text, bd)

cleantxt = ' '.join(txt)

with open('cleantext.txt', 'w', encoding='utf-8') as output:
    output.write(cleantxt)
