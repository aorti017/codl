import urllib2
import re
import sys
import HTMLParser
import zipfile
from shutil import rmtree
from os.path import exists
from os import makedirs, getcwd, listdir
from json import loads
from urllib import urlretrieve

id = -1
flags = []


if(len(sys.argv) <= 1):
    print "No URLs passed"
    sys.exit()
else:
    place = 0
    for i in sys.argv:
        if(i.startswith("http://")):
            break
        place += 1
    url = re.sub("http://boards.4chan.org/co/thread/",
    "", sys.argv[place])
    id = re.sub("/.*", "", url)

flg_a = 0
flg_n = 0
flg_z = 0
subject = ""
n_pos = 0
for i in sys.argv:
    if(i == "-a"):
        flg_a = 1
    if(i == "-z"):
        flg_z = 1
    if(i == "-n"):
        flg_n = 1
        n_pos += 1
    elif(not flg_n):
        n_pos += 1

flags.append(flg_a)
flags.append(flg_n)
flags.append(flg_z)

if(n_pos >= len(sys.argv) and flags[1]):
    print "No directory name specified"
    sys.exit()
else:
    if(n_pos >= 0 and n_pos < len(sys.argv)):
        subject = sys.argv[n_pos]

dPath = getcwd()

try:
    json_data = urllib2.urlopen("https://a.4cdn.org/co/thread/"
    + str(id) + ".json").read()
except urllib2.HTTPError as e:
    print e
    sys.exit()

data = loads(json_data)

if(not flags[1]):
    try:
        subject = data["posts"][0]["sub"]
        subject = re.sub("[A-Za-z]torytime", "", subject)[:-1]
    except KeyError:
        subject = (data["posts"][0]["com"])[:25]
        print "No subject found, temporary directory name assigned:"
        print subject

savePath = dPath+"/"+subject+"/"

if(not exists(savePath)):
    makedirs(savePath)

template = data["posts"][0]["filename"]
template = template[:len(template)/3]
template = re.escape(template)

he = HTMLParser.HTMLParser()

dlNum = 1

for i in data["posts"]:
    try:
        if(re.match(r'^%s.*'%template, i["filename"]) or flags[0]):
            urlretrieve("https://i.4cdn.org/co/" + str(i["tim"])
            + i["ext"], savePath +
             "(" + str(dlNum) + ")" + he.unescape(i["filename"]) + i["ext"])
            dlNum += 1
    except KeyError:
        continue

if(flags[2]):
    myZip = zipfile.ZipFile(subject + ".zip", 'w')
    for i in listdir(savePath + "/"):
        myZip.write(savePath +"/" + i,
        i,  zipfile.ZIP_DEFLATED)
    rmtree(savePath)

#ALLOW FOR MULTIPLE URLS
