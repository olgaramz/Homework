import lxml.html
import os
import urllib.request
import re

baseurl = 'http://www.gazetayakutia.ru'

with urllib.request.urlopen(baseurl) as response:
   html = response.read().decode()

tree = lxml.html.fromstring(html)

queue = []

links = tree.xpath('.//a/@href')
for i in links:
    m = re.search('/index\.php/[^"]*', i)
    if m != None:
        queue.append(baseurl + m.group(0))

visited = []

for i in queue:
    if i not in visited:
        with urllib.request.urlopen(i) as page1:
            html1 = page1.read().decode()
            tree1 = lxml.html.fromstring(html1)
            title1 = tree1.findtext('.//title')
            #author1 = tree1.xpath('.//a[@rel="author"]/text()')[0]
            visited.append(i)
            queue.remove(i)
            f = open(title1[1:5] + '.txt', 'w', encoding = 'utf-8') #filename
            f.write(html1)
            f.close()
            linksOnPage = tree1.xpath('.//a/@href')
            for n in linksOnPage:
                M = re.search('/index\.php/[^"]*', n)
                if M != None:
                    queue.append(baseurl + M.group(0))

#for one page


with urllib.request.urlopen('http://www.gazetayakutia.ru/index.php/component/k2/item/19959-chzhoda-poluchila-prava-zastrojshchika') as page:
   pagehtml = page.read().decode()

pagetree = lxml.html.fromstring(pagehtml)
title = pagetree.findtext('.//title')
author = pagetree.xpath('.//a[@rel="author"]/text()')[0]
text = pagetree.xpath('.//div[@class="itemFullText"]/p/text()') 
date = pagetree.xpath('.//li/text()')[7]
introtext = pagetree.findtext('.//div[@class="itemIntroText"]/p')

#saving files to correct directories

#os.makedirs()

#filename = title[1:5] + '.txt'
#os.path.join(date, filename)
