import csv

tablesplittexts = []
balancedcorpus = []

def balanceByDecade(lst, start, end, volume):
    decadecorpus = []
    corpusvolume = 0
    while corpusvolume < volume:
        for i in lst:
            try:
                chron = i[5]
                decade = int(chron[0:4])
                if decade in range(start,end):
                    decadecorpus.append(i)
                    corpusvolume += int(i[22])
                if corpusvolume >= volume:
                    break
            except ValueError:
                pass
            except IndexError:
                pass
    return decadecorpus

with open('source_post1950_wordcount.csv', 'r', encoding = 'utf-8') as csvfile:
    table = csv.reader(csvfile, delimiter=';')
    for row in table:
        try:
            wordcount = int(row[22])
        except ValueError:
            wordcount = 0
        if wordcount > 100000:
            rowtext1 = []
            rowtext2 = []
            rowtext3 = []
            wordcount1 = wordcount//3
            row1 = row[0] + '1'
            row2 = row[0] + '2'
            row3 = row[0] + '3'
            rowtext1.append(row1)
            rowtext1.extend(row[1:21])
            rowtext1.append(wordcount1)
            rowtext2.append(row2)
            rowtext2.extend(row[1:21])
            rowtext2.append(wordcount1)
            rowtext3.append(row3)
            rowtext3.extend(row[1:21])
            rowtext3.append(wordcount1)
            tablesplittexts.append(rowtext1)
            tablesplittexts.append(rowtext2)
            tablesplittexts.append(rowtext3)
        elif 70000 <= wordcount <= 100000:
            rowtext1 = []
            rowtext2 = []
            wordcount1 = wordcount//2
            row1 = row[0] + '1'
            row2 = row[0] + '2'
            rowtext1.append(row1)
            rowtext1.extend(row[1:21])
            rowtext1.append(wordcount1)
            rowtext2.append(row1)
            rowtext2.extend(row[1:21])
            rowtext2.append(wordcount1)
            tablesplittexts.append(rowtext1)
            tablesplittexts.append(rowtext2)
        else:
            tablesplittexts.append(row)

corpus = tablesplittexts[1:]
dec50 = balanceByDecade(corpus, 1950, 1960, 15000000)
dec61 = balanceByDecade(corpus, 1961, 1970, 15000000)
dec71 = balanceByDecade(corpus, 1971, 1980, 15000000)
dec81 = balanceByDecade(corpus, 1981, 1990, 15000000)
dec91 = balanceByDecade(corpus, 1991, 2000, 15000000)
dec01 = balanceByDecade(corpus, 2001, 2010, 15000000)
dec11 = balanceByDecade(corpus, 2011, 2015, 15000000)

balancedcorpus.append(tablesplittexts[0])
balancedcorpus.extend(dec50)
balancedcorpus.extend(dec61)
balancedcorpus.extend(dec71)
balancedcorpus.extend(dec81)
balancedcorpus.extend(dec91)
balancedcorpus.extend(dec01)
balancedcorpus.extend(dec11)

with open('output.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerows(balancedcorpus)
