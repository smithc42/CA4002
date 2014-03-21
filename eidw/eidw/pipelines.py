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
import datetime

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
		self.duplicatesCursor = self.db.cursor()
		self.insertCursor = self.db.cursor()
		self.scrapedDate = datetime.datetime.today()
		
	def process_item(self, item, spider):    
		try:
			# Select any flights in the database that have the same flight number as the item
			if item ['flight']:
				self.duplicatesCursor.execute ("""SELECT * FROM FLIGHTS WHERE FLIGHT_NUMBER= '%s' ORDER BY id LIMIT 1""" % (item ['flight'][1].encode('utf-8')))
				duplicatesResult = self.duplicatesCursor.fetchall()
				
				if duplicatesResult:
					for row in duplicatesResult:
						self.scrapedDate = row[1]
					if self.scrapedDate:
						days =(datetime.datetime.today() - self.scrapedDate).days
						if days >= 1:
							self.insertCursor.execute("""INSERT INTO FLIGHTS (scrape_time, ORIGIN, FLIGHT_NUMBER, AIRLINE, ARRIVAL_SCHEDULED, ARRIVAL_ACTUAL, GATE, STATUS, EQUIPMENT)  
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
				else:
					self.insertCursor.execute("""INSERT INTO FLIGHTS (scrape_time, ORIGIN, FLIGHT_NUMBER, AIRLINE, ARRIVAL_SCHEDULED, ARRIVAL_ACTUAL, GATE, STATUS, EQUIPMENT)  
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
			else:
				print "Flight number is null"
		except self.db.Error, e:
			print "Error %d: %s" % (e.args[0], e.args[1])
		return item
		