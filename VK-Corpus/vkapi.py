import vk
import time

csvheader = 'id\tsex\tbdate\tlanguages\n'

def getIDs(lst):
    allIDs = []
    for i in lst:
        try:
            userID = i['uid']
            allIDs.append(userID)
        except TypeError:
            pass
    return allIDs

def getFields(lst):
    infostring = ''
    for i in lst:
        ID = i['uid']
        sex = i['sex']
        try:
            bdate = i['bdate']
        except KeyError:
            bdate = '-'
        try:
            pers = i['personal']
            langs = pers['langs']
            lang = ';'.join(langs)
        except KeyError:
            lang = '-'
        except TypeError:
            lang = '-'
        t = str(ID) + '\t' + str(sex) + '\t' + bdate + '\t' + lang + '\n'
        infostring += t
    return infostring

def getTexts(lst):
    posts = []
    for i in lst:
        try:
            text = i['text']
            if text != '':
                posts.append(text)
        except TypeError:
            pass
    return posts

session = vk.Session()
session = vk.AuthSession(app_id='******', user_login='mymail@example.com', user_password='*******')
api = vk.API(session)
users = api.users.search(city=59, count = 1000)

fullIDList = getIDs(users)
info = api.users.get(user_ids=fullIDList, fields='sex,bdate,personal')
s = getFields(info)
fullcsv = csvheader + s
with open('corpus\\meta.csv', 'w', encoding = 'utf-8') as f:
    f.write(fullcsv)

for i in fullIDList:
    texts = api.wall.get(owner_id = i, filter = 'owner')
    userposts = getTexts(texts)
    z = '\n\n\n'.join(userposts)
    user = 'corpus\\' + str(i) + '.txt'
    with open(user, 'w', encoding='utf-8') as f:
        f.write(z)
    time.sleep(1)
