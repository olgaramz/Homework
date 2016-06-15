import lxml.html
import re
from alphabet_detector import AlphabetDetector

ad = AlphabetDetector()
global dictionary
dictionary = {}
global punct
punct = ['，', '！', '。', '”', '：', '？', '“', '……']
global sent
sent = ''
lines = []
global strToMark
strToMark = ''
global initLength
initLength = 0

def markup(strng):
    if strng in dictionary:
        annotation = dictionary[strng]        
        transcr = annotation[::2]
        transcr = '; '.join(transcr)
        english = annotation[1::2]
        english = '; '.join(english)
        markedstr = '<w><ana lex="' + strng + '" transcr=' + transcr + '" sem="' + english + '"/>' + strng + '</w>\n'
        global sent        
        sent += markedstr
        length = len(strng)
        tail = strToMark[length-1:]
        result = []
        result.append(tail, length)
        return result
    else:
        newstrng = strng[:-1] #recursion error
        return markup(newstrng) 

    
with open('cedict_ts.u8', 'r', encoding='utf-8') as dictText:
    for line in dictText:
        value = []
        t = re.search('^#.*', line)
        if t == None:
            lineSplit = line.split()
            m = re.search('\[.+?\]', line)
            if m != None:
                transcr = m.group(0)
            n = re.search('/(.+)/$', line)
            if n != None:
                english = n.group(1)
            key = lineSplit[1]
            value.append(transcr)
            value.append(english)
            if key not in dictionary:
                dictionary[key] = value
            else:
                dictionary[key].append(value[0])
                dictionary[key].append(value[1])
    

with open('stal.xml', 'r', encoding='utf-8') as text:
    xml = text.read()
    tree = lxml.html.fromstring(xml)
    sentences = tree.xpath('.//body/se/text()')
    
for i in sentences:
    s = ad.is_cjk(i)
    if s == True:
        strToMark = ''
        for j in i:
            if j not in punct:
                strToMark += j
        initLength = len(strToMark)
        sent = '<se>'
        result = markup(strToMark)
        length = result[1]
        tail = result[0]
        while initLength > 0:
               newresult = markup(tail)
               initlength = initLength - newresult[1]
               tail = newresult[0]
        sent += '</se>\n'
        lines.append(sent)
    else:
        st = '<se>' + i + '</se>\n'
        lines.append(st)

fullText = ''.join(lines)

with open('chinese.xml', 'w', encoding = 'utf-8') as f:
    f.write(fullText)
