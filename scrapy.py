#coding:utf-8
from Queue import Queue
import threading
import urllib2
import urllib
import time
import json
import codecs
import re
import time
from bs4 import BeautifulSoup
'''
download example
print "downloading with urllib" 
url = 'http://www.pythontab.com/test/demo.zip'  
print "downloading with urllib"
urllib.urlretrieve(url, "demo.zip")
'''
def rename():
    pattern = re.compile(r'\w+_\w+.png$')
    filenames = []
    toberename = []
    allnames = os.listdir(".")
    for onename in allnames:
        if pattern.match(onename):
            toberename.append(onename)
    for tobeone in toberename:
        print tobeone
        renamed = tobeone.replace("_", ".")
        print "rename from ->" + tobeone + " to ->" + renamed + "\n"
        os.rename(tobeone, renamed)

urls_queue = Queue()
download_queue = Queue()
lock = threading.Lock()
f = codecs.open('out.txt', 'w', 'utf8')
class ThreadUrl(threading.Thread):

    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        pass

class ThreadDownLoad(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        
    def run(self):
        while True:
            time.sleep(5)
            downitem = self.queue.get()
            print "begin down -->" + downitem['name'] + "\t" + downitem['img']
            filename = downitem['name'] + ".png"
            urllib.urlretrieve(downitem['img'], filename)
            self.queue.task_done()           
        

class ThreadCrawl(threading.Thread):

    def __init__(self, queue, out_queue):
        threading.Thread.__init__(self)       
        self.queue = queue
        self.out_queue = out_queue

    def run(self):
        while True:
            time.sleep(5)
            oneurl = self.queue.get()
            try:
                req = urllib2.Request(oneurl)                
                res = urllib2.urlopen(req)                
            except urllib2.HTTPError, e:
                raise e.reason
            li=[]
            soup = BeautifulSoup(res.read(), 'html.parser')
            ss = soup.select("a[data-app-pname]")
            for str in soup.select("a[data-app-pname]"):
                dic={}
                dic['name'] = str['data-app-pname']
                dic['img'] = str['data-app-icon']
                li.append(dic)

            urlstr = soup.find_all("a", class_="page-item next-page ")
            nextlink = urlstr[0]['href']
            '''  
            for dic in li:
                print dic['name'] + "\t" + dic['img']
            '''
            res.close()
            if nextlink != "":
                self.queue.put(nextlink)
            for item in li:
                self.out_queue.put(item)            
            self.queue.task_done()
            

    def _data_post(self, item):
        if item == '':
            return ""        
        return self.url + "/" + item

    def _item_queue(self):
        pass


'''
no useed
'''
class ThreadWrite(threading.Thread):

    def __init__(self, queue, lock, f):
        threading.Thread.__init__(self)
        self.queue = queue
        self.lock = lock
        self.f = f

    def run(self):
        while True:
            item = self.queue.get()
            self._parse_data(item)
            self.queue.task_done()

    def _parse_data(self, item):
        for i in item:
            l = self._item_to_str(i)
            with self.lock:
                print 'write %s' % l
                self.f.write(l)

    def _item_to_str(self, item):
        positionName = item['positionName']
        positionType = item['positionType']
        workYear = item['workYear']
        education = item['education']
        jobNature = item['jobNature']
        companyName = item['companyName']
        companyLogo = item['companyLogo']
        industryField = item['industryField']
        financeStage = item['financeStage']
        companyShortName = item['companyShortName']
        city = item['city']
        salary = item['salary']
        positionFirstType = item['positionFirstType']
        createTime = item['createTime']
        positionId = item['positionId']
        return positionName + ' ' + positionType + ' ' + workYear + ' ' + education + ' ' + \
            jobNature + ' ' + companyLogo + ' ' + industryField + ' ' + financeStage + ' ' + \
            companyShortName + ' ' + city + ' ' + salary + ' ' + positionFirstType + ' ' + \
            createTime + ' ' + str(positionId) + '\n'


def main():
    for i in range(4):
        t = ThreadCrawl(urls_queue, download_queue)
        t.setDaemon(True)
        t.start()
    urls = ['http://www.wandoujia.com/category/5029']
    for oneurl in urls:
        urls_queue.put(oneurl)
    for i in range(4):
        t = ThreadDownLoad(download_queue)
        t.setDaemon(True)
        t.start()

    urls_queue.join()
    data_queue.join()
    print 'data_queue siez: %d' % data_queue.qsize()
main()
