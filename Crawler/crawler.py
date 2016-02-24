import lxml.html
import os
import urllib.request
import re

baseurl = 'http://www.gazetayakutia.ru'
queue = []
visited = []
visited.append(baseurl)

with urllib.request.urlopen(baseurl) as response:
   html = response.read().decode()
tree = lxml.html.fromstring(html)
links = tree.xpath('.//a/@href')
for i in links:
    m = re.search('/index\.php/[^"]*', i)
    if m != None:
        queue.append(baseurl + m.group(0))

for i in queue:
    if i not in visited:
        counter += 1
        try:
            with urllib.request.urlopen(i) as page:
                pagehtml = page.read().decode()
                pageurl = i    
        except UnicodeEncodeError:
            m = re.match('http://www.gazetayakutia.ru/index.php/component/k2/itemlist/tag/(.*)', i)
            if m != None:
                try:
                    with urllib.request.urlopen('http://www.gazetayakutia.ru/index.php/component/k2/itemlist/tag/' + urllib.request.quote(m.group(1))) as page:
                        pagehtml = page.read().decode()
                        pageurl = i
                except urllib.error.HTTPError:
                    continue       
        pagetree = lxml.html.fromstring(pagehtml)
        title = pagetree.findtext('.//title')
        try:            
            author = pagetree.xpath('.//a[@rel="author"]/text()')[0]
        except IndexError:
            author = 'Noname'
        date1 = pagetree.xpath('.//li/text()')
        for x in date1:
            p = re.search('\.*([A-z]*, [0-9]{2} [A-z]* [0-9]{4} [0-9]{2}:[0-9]{2})', x)
            if p != None:
                dateCreated = p.group(1)
                dateCreated = dateCreated.replace(':', '_')
        introtext = pagetree.findtext('.//div[@class="itemIntroText"]/p')
        text = pagetree.xpath('.//div[@class="itemFullText"]/p/text()')
        textstring = '\n'.join(text)
        linksOnPage = pagetree.xpath('.//a/@href')
        for n in linksOnPage:
            M = re.search('/index\.php/[^"]*', n)
            if M != None:
                queue.append(baseurl + M.group(0))
        if dateCreated != 'unknown date':
            splitDate = dateCreated.split()
            year = splitDate[3]
            month = splitDate[2]
            day = splitDate[1]
        else:
            year = 'unknown year'
            month = 'unknown month'
            day = 'unknown day'
        path = 'C:\\Users\\User\\Documents\\Corpus\\plaintext\\' + year + '\\' + month
        filename = path + '\\' + dateCreated + str(counter) + '.txt'
        if os.path.exists(path) is False:
            os.makedirs(path)
        f1 = open(filename, 'w', encoding = 'utf-8')
        f1.write('@au ' + author + '\n' + '@ti ' + title + '\n' + '@da ' + dateCreated + '\n' + str(introtext) + '\n' + textstring)
        f1.close()            
        visited.append(i)
        print(counter) #remove later
