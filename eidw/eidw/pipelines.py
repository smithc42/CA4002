# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sys
import MySQLdb
import hashlib
from scrapy.http import Request
from scrapy.exceptions import DropItem
import time    

class EidwPipeline(object):
    def process_item(self, item, spider):
        return item

class DuplicatesPipeline(object):

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item['flight'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['flight'])
            return item
			
class DatabasePipeline(object):
	def __init__(self):
		self.db = MySQLdb.connect("localhost","user","pass","test" )
		self.cursor = self.db.cursor()
		
	def process_item(self, item, spider):    
		try:
			self.cursor.execute("""INSERT INTO FLIGHTS (scrape_time, ORIGIN, FLIGHT_NUMBER, AIRLINE, ARRIVAL_SCHEDULED, ARRIVAL_ACTUAL, GATE, STATUS, EQUIPMENT)  
							VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s)""", 
							(time.strftime('%Y-%m-%d %H:%M:%S'),
							item ['origin'][1].encode('utf-8'), 
							item ['flight'][1].encode('utf-8'),
							item ['airline'][0].encode('utf-8'), 
							item ['arrivalScheduled'][0].encode('utf-8'), 
							item ['arrivalActual'][0].encode('utf-8'), 
							item ['gate'][0].encode('utf-8'), 
							item ['status'][0].encode('utf-8'), 
							item ['equipment'][0].encode('utf-8')))
			self.db.commit()				
		except self.db.Error, e:
			print "Error %d: %s" % (e.args[0], e.args[1])
		return item