import lxml.html
import re
from alphabet_detector import AlphabetDetector

ad = AlphabetDetector()
global dictionary
dictionary = {}
global text
text = ''
punct = ['，', '！', '。', '”', '：', '？', '“', '……']
global sent
sent = ''

def markdown(i):
    state = 'exists'
    ind = 1
    while state == 'exists':
        workstrng = i[:ind]
        if workstrng in dictionary:
            state = 'exists'
            ind += 1
        else:
            state = 'none'
    mark = workstrng[:-1]
    markup = dictionary[mark]
    transcr = markup[::2]
    transcr = '; '.join(transcr)
    english = markup[1::2]
    english = '; '.join(english)
    markedstr = '<w><ana lex="' + mark + '" transcr=' + transcr + '" sem="' + english + '"/>' + mark + '</w>\n'                  
    global sent 
    sent += markedstr
    tail = i[len(workstrng):]
    if tail == '':
        return
    elif len(tail) == 1:
        markup = dictionary[tail]
        transcr = markup[::2]
        transcr = '; '.join(transcr)
        english = markup[1::2]
        english = '; '.join(english)
        markedstr = '<w><ana lex="' + tail + '" transcr=' + transcr + '" sem="' + english + '"/>' + tail + '</w>\n'
        sent += markedstr
        return
    else:
        markdown(tail)
        return

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
    
with open('stal.xml', 'r', encoding='utf-8') as t:
    xml = t.read()
    tree = lxml.html.fromstring(xml)
    sentences = tree.xpath('.//body/se/text()')

for i in sentences:
    s = ad.is_cjk(i)
    sent = '<se>'
    if s == True:
        cleanstr = ''
        for letter in i:
            if letter not in punct:
                cleanstr += letter
            else:
                pass
        markdown(cleanstr)
        sent += '</se>\n'
        text += sent
    else:
        tagged = '<se lang="ru">' + i + '</se>\n'
        text += tagged
        
with open('chineseprocessed.xml', 'w', encoding='utf-8') as f:
    f.write(text)
