import requests
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from browsermobproxy import Server
import json

ids = []
totalItems = [0]

pageurl= "https://www.instagram.com/infinityward/"
fname = "infinity_ward"

def writeFile(file, text):
    f = open(file + '.txt', 'a+')
    f.write(text + '\n')

def realFirst():
    tmp = requests.get(pageurl).text
    ##print (type(tmp))
    #print (tmp)
    abs = tmp.split(",")
    for i in abs:
        if "display_src" in i:
            tmps = ((i.split(": \"")[-1]).replace('"',""))
            writeFile(fname, tmps)
            totalItems[0] += 1


def entry(url):
    server = Server('/home/wai/Desktop/WebScrap/source/forInstagram/browsermob-proxy-2.1.4/bin/browsermob-proxy')
    server.start()
    proxy = server.create_proxy()
    proxy.new_har()
    chrome_options = webdriver.ChromeOptions()
    #chrome_options.add_argument("--headless")
    #chrome_options.add_argument("--mute-audio")
    chrome_options.add_argument("--proxy-server={0}".format(proxy.proxy))
    driver = webdriver.Chrome("/home/wai/Applications/chromedriver", chrome_options=chrome_options)
    driver.get(url)
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    driver.find_element_by_link_text("Load more").send_keys(Keys.ENTER)
    tmp = (proxy.har)
    entries = (tmp['log']['entries'])
    finalTmp = []
    for i in entries:
        if (i['request']['queryString']):
            finalTmp.append(i['request']['queryString'])
    qID =  (finalTmp[-1][0]['value'])
    qVariable = (finalTmp[-1][1]['value'])
    ids.append(qID)

    qVariable = json.loads(qVariable)
    vID = str(qVariable['id'])
    ids.append(vID)
    vFirst = str(qVariable['first'])
    ids.append(vFirst)
    vAfter = str(qVariable['after'])
    ids.append(vAfter)

    driver.close()
    proxy.close()
    server.stop()

def getFollowing():
    text = 'https://www.instagram.com/graphql/query/?query_id='+ids[0]+'&variables={"id":"'+ids[1]+',"first":20}'
    resp = requests.get(text).json()
    print (resp)


def genGET(no=12):
    #return 'https://www.instagram.com/graphql/query/?query_id='+ids[0]+'&variables={"id":"'+ids[1]+'","first":'+ids[2]+',"after":"'+ids[-1]+'"}'
    return 'https://www.instagram.com/graphql/query/?query_id=' + ids[0] + '&variables={"id":"' + ids[1] + '","first":20'

def getTotal(resText):
    resp = requests.get(resText).json()
    #print (resp)
    #print (resp['status'])
    trying = 0
    if resp['status'] == 'fail':
        print ("Damn")
    while resp['status'] == 'fail' and trying < 5:
        print ('trying')
    if resp['status'] != 'fail':
        first = (resp['data']['user']['edge_owner_to_timeline_media'])
        #print("total number of post >" + str(first['count']))
        return str(first['count'])
    else:
        return False

def getImg(resText):
    resp = requests.get(resText).json()
    print (resp)
    first =  (resp['data']['user']['edge_owner_to_timeline_media'])
    second = first['edges']
    #print (len(second))
    for i in second:
        third = i['node']
        #print (third)
        #print(third['display_url'])
        writeFile(fname, third['display_url'])
        totalItems[0] = int(totalItems[-1]) + 1

#realFirst()
print (ids)
entry(pageurl)
print (ids)
#getFollowing()

total = getTotal(genGET())
print (total)
subTotal = int(total) - int(totalItems[0])
#print (genGET(no=12))
getImg(genGET(no=subTotal))
#getImg(genGET(no=100))
print (str(totalItems[0]))
if str(total) == str(totalItems[0]):
    print ("Yes")
