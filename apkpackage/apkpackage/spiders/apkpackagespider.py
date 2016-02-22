# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Spider
from scrapy.selector import Selector
from apkpackage.items import ApkpackageItem
from twisted.test.test_sip import response1
from scrapy.http import Request
from string import atoi
from __builtin__ import str
from _ast import Str
import time

class ApkpackagespiderSpider(scrapy.Spider):
    name = "apkpackage"
    allowed_domains = ["coolapk.com"]
    #types = ['sns', 'system', 'desktop', 'themes', 'news', 'network', 'media', 'photography', 'life', 'tools', 'business']
    types = ['sns','media', 'news','shopping']
    start_urls = []
    for type in types:
        start_urls.append("http://www.coolapk.com/apk/" + type)
    
    def parse(self, response):    
        response_selector = Selector(response)
        #next_link = response_selector.xpath ('//div[@class="panel-footer ex-card-footer text-center"]/ul/li/a[text()="&gt;"]')
        current_link = response_selector.xpath(u'//div[@class="panel-footer ex-card-footer text-center"]/ul//li[@class="active"]/a/@href').extract()[0]
        all_link = response_selector.xpath(u'//div[@class="panel-footer ex-card-footer text-center"]/ul//li/a/@href').extract()
        last_link = all_link[-1]
        current_page_num = current_link[current_link.find('=') + 1:]
        current_page_num = atoi(current_page_num)
        type = current_link[current_link.find('apk/') +4:current_link.find('?')-1]
        last_page_num = last_link[last_link.find('=') + 1:]
        if cmp(last_page_num, "###") !=0 :
            last_page_num = atoi(last_page_num)
            if current_page_num < last_page_num:                
                current_page_num = current_page_num + 1            
                next_link = "http://www.coolapk.com" + current_link[0:current_link.find('=')+1] + str(current_page_num)
                yield Request(url=next_link, callback=self.parse)
            for detail in self.parsedetail(response, type):
                yield detail                                                    
        
     
    def parsedetail(self, response, type):
        print "type:" +type
        sel = Selector(response)
        sites = sel.xpath('//ul[@class="media-list ex-card-app-list"]/li')
        for site in sites :
            item = ApkpackageItem()
            item['name'] = site.xpath('div/h4/a/text()').extract()
            item['packageName'] = site.xpath('a/@href').extract()[0].split("/")[2]
            item['type'] = type
            item['typeid'] = str(self.types.index(type))
            yield item 
            

                    

        
           
                       