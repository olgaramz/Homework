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
        try:
            with urllib.request.urlopen(i) as page:
                pagehtml = page.read().decode()
            pagetree = lxml.html.fromstring(pagehtml)
            title = pagetree.findtext('.//title')
            try:            
                author = pagetree.xpath('.//a[@rel="author"]/text()')[0]
            except IndexError:
                author = 'no author'
            try:
                date = pagetree.xpath('.//li/text()')[7]
                date = date.replace('\r', '')
                date = date.replace('\n', '')
                date = date.replace('\t', '')
                date = date.replace(':', '')
                if date == '':
                    date = 'unknown date'
            except IndexError:
                date = 'unknown date'
            introtext = pagetree.findtext('.//div[@class="itemIntroText"]/p')
            text = pagetree.xpath('.//div[@class="itemFullText"]/p/text()')
            textstring = '\n'.join(text)
            linksOnPage = pagetree.xpath('.//a/@href')
            for n in linksOnPage:
                M = re.search('/index\.php/[^"]*', n)
                if M != None:
                    queue.append(baseurl + M.group(0))
        except UnicodeEncodeError:
            m = re.match('http://www.gazetayakutia.ru/index.php/component/k2/itemlist/tag/(.*)', i)
            if m != None:
                try:
                    with urllib.request.urlopen('http://www.gazetayakutia.ru/index.php/component/k2/itemlist/tag/' + urllib.request.quote(m.group(1))) as page:
                        pagehtml = page.read().decode()
                except urllib.request.HTTPError:
                    pass
            pagetree = lxml.html.fromstring(html)
            title = tree.findtext('.//title')
            try:            
                author = pagetree.xpath('.//a[@rel="author"]/text()')[0]
            except IndexError:
                author = 'no author'
            try:
                date = pagetree.xpath('.//li/text()')[7]
                date = date.replace('\r', '')
                date = date.replace('\n', '')
                date = date.replace('\t', '')
                date = date.replace(':', '')
                if date == '':
                    date = 'unknown date'
            except IndexError:
                date = 'unknown date'
            introtext = pagetree.findtext('.//div[@class="itemIntroText"]/p')
            text = pagetree.xpath('.//div[@class="itemFullText"]/p/text()')
            textstring = '\n'.join(text)
            linksOnPage = pagetree.xpath('.//a/@href')
            for n in linksOnPage:
                M = re.search('/index\.php/[^"]*', n)
                if M != None:
                    queue.append(baseurl + M.group(0))
        f = open(date + '.html', 'w', encoding = 'utf-8') #filename
        f.write(pagehtml)
        f.close()
        f1 = open(date + '.txt', 'w', encoding = 'utf-8')
        f1.write(str(author) + '\n' + date + '\n' + str(introtext) + '\n' + textstring)
        f1.close()            
        visited.append(i)
        queue.remove(i)
    else:
        queue.remove(i)
