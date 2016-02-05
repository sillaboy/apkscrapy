# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Spider
from scrapy.selector import Selector
from apkpackage.items import ApkpackageItem
from twisted.test.test_sip import response1
from scrapy.http import Request
from string import atoi
from __builtin__ import str

class ApkpackagespiderSpider(scrapy.Spider):
    name = "apkpackage"
    allowed_domains = ["coolapk.com"]
    start_urls = ["http://www.coolapk.com/apk/sns"]  
    
    def parse(self, response):    
        response_selector = Selector(response)
        #next_link = response_selector.xpath ('//div[@class="panel-footer ex-card-footer text-center"]/ul/li/a[text()="&gt;"]')
        current_link = response_selector.xpath(u'//div[@class="panel-footer ex-card-footer text-center"]/ul//li[@class="active"]/a/@href').extract()[0]       
        all_link = response_selector.xpath(u'//div[@class="panel-footer ex-card-footer text-center"]/ul//li/a/@href').extract()
        disables = all_link[-2]
        next_page_num = current_link[current_link.find('=') +1:]
        next_page_num = atoi(next_page_num) + 1
        next_page_prefix = current_link[0:current_link.find('=')+1] + str(next_page_num)
        next_link = "http://www.coolapk.com" + next_page_prefix
        detail_link = "http://www.coolapk.com"  + current_link      
                
        if (cmp(disables, "###") != 0):                
            yield Request(url=next_link, callback=self.parse)
        yield self.parsedetail(response)                                              
        
     
    def parsedetail(self, response):
        sel = Selector(response)
        sites = sel.xpath('//ul[@class="media-list ex-card-app-list"]/li')
        for site in sites :
            item = ApkpackageItem()
            item['name'] = site.xpath('div/h4/a/text()').extract()
            item['packageName'] = site.xpath('a/@href').extract()

                    

        
           
                       