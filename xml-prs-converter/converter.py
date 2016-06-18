import lxml.html
import sys
import re

def prstoxml(filename):
    xmltext = '<body>\n'
    listOfColumns = []
    with open(filename, 'r', encoding='utf-8') as text:
        for line in text:
            columns = line.split('\t')
            listOfColumns.append(columns)

    del listOfColumns[1:10]
    listOfColumns.remove(listOfColumns[0])
    seen = set()
    for index, i in enumerate(listOfColumns):
        if str(i) not in seen:
            seen.add(str(i))        
            currentstrng = ''
            seNum = i[0]
            wordNum = i[1]
            lang = i[2]
            wordGraph = i[3]
            word = i[4]
            indexword = i[5]
            nvars = i[6] #number of variants
            nlems = i[7] #number of lemmas
            nvar = i[8]
            lem = i[9]
            trans = i[10]
            transRu = i[11]
            lex = i[12]
            gram = i[13]
            flex = i[14]
            punctl = i[15]
            punctr = i[16]
            sentPos = i[17]
            if sentPos == 'bos':
                currentstrng += '<se>\n'
            currentstrng += punctl
            annotStrng = '<w>\n<ana lex="' + lem + '" morph="'  + '" gr="' + gram + flex + '" trans="' + transRu + '" />\n'
            currentstrng += annotStrng            
            if nvars != '':        
                variants = int(nvars)
                if variants > 1:
                    tolookahead = listOfColumns[index:index+variants]
                    for j in tolookahead:
                        transRu1 = j[10]
                        lem1 = j[8]
                        lex1 = j[11]
                        indexword1 = j[5]
                        flex1 = j[13]
                        gram1 = j[12]
                        annotStrng1 = '<ana lex="' + lem1 + '" morph="' + flex1 + '" gr="' + lex1 + gram1 + '" trans="' + transRu1 + '" />\n'
                        currentstrng += annotStrng1
                        seen.add(str(j))
            currentstrng += word
            currentstrng += '</w>\n'
            currentstrng += punctr
            if sentPos == 'eos':
                currentstrng += '</se>\n'
            xmltext += currentstrng
        else:
            pass
    xmltext += '</body>'
    return xmltext
    
filename = 'C:\\Users\\Asus\\Desktop\\Converter\\testprs.prs'
m = prstoxml(filename)
with open('xmlout1.xml', 'w', encoding='utf-8') as f:
    f.write(m)
