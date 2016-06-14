from pymysql import connect, cursors

allUsers = []

def insertIntoDB(lst):
    counter = 0
    counter2 = 0
    l = {}
    for i in lst:
        counter += 1
        listoffields = i.split('\t')
        sex = listoffields[1]
        bdate = listoffields[2]
        lang = listoffields[3]
        if lang in l:
            for key in l.keys():
                if l[key] == lang:
                    idlang = key
        else:
            counter2 += 1
            l[counter2] = lang
            idlang = counter2
        KeyID = counter
        sqlcommand1 = 'INSERT INTO metainfo (id, sex, birthdate, languages) VALUES (' + str(KeyID) + ', ' + sex + ', ' + bdate + ', ' + str(idlang) + ');'
        sqlcommand2 = 'INSERT INTO languages (id, lang) VALUES (' + str(idlang) + ', ' + lang + ');'
        cursor.execute(sqlcommand1)
        cursor.execute(sqlcommand2)
        
conn = connect(host = 'localhost', port = 3306, user = 'admin', passwd = '*****', db = 'VK')
cursor = conn.cursor(cursors.DictCursor)
cursor.execute( "CREATE TABLE `metainfo` (id INTEGER, sex VARCHAR(1), birthdate VARCHAR(20), languages INTEGER);")
cursor.execute("CREATE TABLE `languages`(id INTEGER, lang VARCHAR(100));")

with open('C:\\Users\\Asus\\Desktop\\mysql\\meta.csv', 'r', encoding = 'utf-8') as meta:
    for line in meta:
        allUsers.append(line)
users = allUsers[1:]
insertIntoDB(users)
