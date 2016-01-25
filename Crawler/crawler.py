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
            visited.append(i)
            queue.remove(i)
            f = open(title + '.txt', 'w', encoding = 'utf-8') #invalid syntax?
            f.write(html1)
            f.close()
            linksOnPage = tree1.xpath('.//a/@href')
            for n in linksOnPage:
                M = re.search('/index\.php/[^"]*', n)
                if M != None:
                    queue.append(baseurl + M.group(0)
    elif i in visited: #invalid syntax
        queue.remove(i)

#for one page

pageurl = 'http://www.gazetayakutia.ru/index.php/component/k2/item/19844-dmitrij-glushko-ya-obyazatelno-vernus-v-yakutiyu'

with urllib.request.urlopen('http://www.gazetayakutia.ru/index.php/component/k2/item/19844-dmitrij-glushko-ya-obyazatelno-vernus-v-yakutiyu') as page:
   pagehtml = page.read().decode()

pagetree = lxml.html.fromstring(pagehtml)
title = pagetree.findtext('.//title')
author = pagetree.xpath('.//li[@style="padding:0 4px 0 0;"]/text()')#[0] #empty
text = pagetree.findtext('.//!-- Item fulltext --/div[@class="itemFullText"]') #empty
