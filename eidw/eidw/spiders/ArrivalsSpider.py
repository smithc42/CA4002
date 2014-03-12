from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from eidw.items import EidwItem
import MySQLdb
import time

class ArrivalsSpider(BaseSpider):
	name = "eidw"
	allowed_domains = ["http://www.flightstats.com"]
	start_urls = ["http://www.flightstats.com/go/FlightStatus/flightStatusByAirport.do?airportCode=DUB&airportQueryTime=0", 
	"http://www.flightstats.com/go/FlightStatus/flightStatusByAirport.do?airportCode=DUB&airportQueryTime=6",
	"http://www.flightstats.com/go/FlightStatus/flightStatusByAirport.do?airportCode=DUB&airportQueryTime=7"]
	
	db = MySQLdb.connect("localhost","user","pass","test", charset="utf8", use_unicode=True )
	cursor = db.cursor()

	cursor.execute("DROP TABLE IF EXISTS FLIGHTS")

	sql = """CREATE TABLE FLIGHTS (
			id INT NOT NULL AUTO_INCREMENT,
			scrape_time TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
			PRIMARY KEY(id),
			 ORIGIN  VARCHAR(50) ,
			 FLIGHT_NUMBER  VARCHAR(50) ,
			 AIRLINE VARCHAR(50) ,  
			 ARRIVAL_SCHEDULED VARCHAR(50) ,
			 ARRIVAL_ACTUAL VARCHAR(50) ,
			 GATE VARCHAR(50) ,
			 STATUS VARCHAR(50) ,
			 EQUIPMENT VARCHAR(50) )"""

	cursor.execute(sql)
	db.close()
	
	def parse(self, response):
		unicode(response.body.decode(response.encoding)).encode('utf-8')
		hxs = HtmlXPathSelector(response)
		flights = hxs.xpath("//table[@class='tableListingTable']//tr")
		items = []
		for flights in flights:
			item = EidwItem()
			item ["origin"] = flights.xpath("td[1]/a/text()|td[1]/text()").extract()
			item ["flight"] = flights.xpath("td[2]/a/text()|td[2]/text()").extract()
			item ["airline"] = flights.xpath("td[4]/a/text()|td[4]/text()").extract()
			item ["arrivalScheduled"] = flights.xpath("normalize-space(td[5]/a/text()|td[5]/text())").extract()
			item ["arrivalActual"] = flights.xpath("normalize-space(td[6]/a/text()|td[6]/text())").extract()
			item ["gate"] = flights.xpath("normalize-space(td[7]/a/text()|td[7]/text())").extract()
			item ["status"] = flights.xpath("normalize-space(td[8]/a/text()|td[8]/text())").extract()
			item ["equipment"] = flights.xpath("normalize-space(td[9]/a/text()|td[9]/text())").extract()
			items.append(item)
		return items
		#print items