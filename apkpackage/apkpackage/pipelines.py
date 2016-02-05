# -*- coding: utf-8 -*-
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from mhlib import PATH
from os import path
import sqlite3
from fileinput import filename

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ApkpackagePipeline(object):
    
    filename="apkPackage.db"
    
    def __init__(self):
        self.conn=None
        dispatcher.connect(self.initialize,signals.engine_started)
        dispatcher.connect(self.finalize,signals.engine_stopped)
        
    def process_item(self, item, spider):
        self.conn.execute('insert into apkpackage values(?,?,?,?)', (item['typeid'],item['type'],item['name'][0],item['packageName']))
        return item
    
    def initialize(self):
        if path.exists(self.filename):
            self.conn = sqlite3.connect(self.filename)
        else:
            self.conn = self.create_table(self.filename)
            
    def finalize(self):
        if self.conn is not None:
            self.conn.commit()
            self.conn.close()
            self.conn=None
            
    def create_table(self, filename):
        conn=sqlite3.connect(filename)
        conn.execute('create table apkpackage(typeid text, type text, name text,packagename text)')
        conn.commit()
        return conn