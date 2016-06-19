import re
import argparse

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
            word = i[4]
            nvars = i[6] #number of variants
            lem = i[9]
            trans = i[10]
            lex = i[12]
            gram = i[13]
            flex = i[14]
            punctl = i[15]
            punctr = i[16]
            sentPos = i[17]
            print(sentPos)
            if sentPos == 'bos':
                currentstrng += '<se>\n'
            currentstrng += punctl
            annotStrng = '<w>\n<ana lex="' + lem + '" morph="' + flex + '" gr="' + lex + gram + '" trans="' + trans + '" />\n'
            currentstrng += annotStrng            
            if nvars != '':        
                variants = int(nvars)
                if variants > 1:
                    tolookahead = listOfColumns[index:index+variants]
                    for j in tolookahead:
                        trans1 = j[10]
                        lem1 = j[9]
                        lex1 = j[12]
                        flex1 = j[14]
                        gram1 = j[13]
                        annotStrng1 = '<ana lex="' + lem1 + '" morph="' + flex1 + '" gr="' + lex1 + gram1 + '" trans="' + trans1 + '" />\n'
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

def xmltoprs(filename):
    fulltext = []
    lines = ''
    prstxt = '#sentnum\t#wordnum\t#graphword\t#numvar\t#lex\t#morph\t#gram\t#trans\n'
    with open(filename, 'r', encoding='utf-8') as text:
        for line in text:
            newline = line.replace('\n', '')
            lines += newline
    fulltext = re.split('(?<=</se>)\s+(?=<se>)', lines)
    for index, value in enumerate(fulltext):
        sentnum = str(index + 1) #1
        words = re.split('(?<=</w>)\s+(?=<w>)', value)
        for index, value in enumerate(words):
            wordnum = str(index + 1) #2
            g = re.search('(?<=/>)\s+\w+\s+(?=</w>)', value)
            if g != None:
                graphword = g.group(0)
            graphword = graphword.replace(' ', '') #3
            annotations = re.findall('<ana.+?/>', value)
            for index, value in enumerate(annotations):
                numvar = index + 1
                numberVar = str(numvar)
                a = re.search('lex="(\w+)"', value)
                lex = a.group(1) #4
                m = re.search('morph="(.*?)"', value)
                if m == None:
                    morph = ''
                else:
                    morph = m.group(1) #5
                gr = re.search('gr="(.*?)"', value)
                gram = gr.group(1) #6
                t = re.search('trans="(.*?)"',value)
                trans = t.group(1) #7
                finalstrng = sentnum + '\t' + wordnum + '\t' + graphword + '\t' + numberVar + '\t' + lex + '\t' + morph + '\t' + gram + '\t' + trans + '\n'
                prstxt += finalstrng
    return prstxt
                
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', required=True)
parser.add_argument('-o', '--output', required=True)
parser.add_argument('-f', '--format', required=True)
args = parser.parse_args()

inputfile = args.i
outputfile = args.o

if args.format == 'prs':
    m = prstoxml(inputfile)
    with open(outputfile, 'w', encoding='utf-8') as f:
        f.write(m)
        
if args.format == 'xml':
    m = xmltoprs(inputfile)
    with open(outputfile, 'w', encoding='utf-8') as f:
        f.write(m)
