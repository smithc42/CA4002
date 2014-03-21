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
	"http://www.flightstats.com/go/FlightStatus/flightStatusByAirport.do?airportCode=DUB&airportQueryTime=7",
	"http://www.flightstats.com/go/FlightStatus/flightStatusByAirport.do?airportCode=DUB&airportQueryTime=8",
	"http://www.flightstats.com/go/FlightStatus/flightStatusByAirport.do?airportCode=DUB&airportQueryTime=9",
	"http://www.flightstats.com/go/FlightStatus/flightStatusByAirport.do?airportCode=DUB&airportQueryTime=10",
	"http://www.flightstats.com/go/FlightStatus/flightStatusByAirport.do?airportCode=DUB&airportQueryTime=11",
	"http://www.flightstats.com/go/FlightStatus/flightStatusByAirport.do?airportCode=DUB&airportQueryTime=12",
	"http://www.flightstats.com/go/FlightStatus/flightStatusByAirport.do?airportCode=DUB&airportQueryTime=13",
	"http://www.flightstats.com/go/FlightStatus/flightStatusByAirport.do?airportCode=DUB&airportQueryTime=14",
	"http://www.flightstats.com/go/FlightStatus/flightStatusByAirport.do?airportCode=DUB&airportQueryTime=15",
	"http://www.flightstats.com/go/FlightStatus/flightStatusByAirport.do?airportCode=DUB&airportQueryTime=16",
	"http://www.flightstats.com/go/FlightStatus/flightStatusByAirport.do?airportCode=DUB&airportQueryTime=17",
	"http://www.flightstats.com/go/FlightStatus/flightStatusByAirport.do?airportCode=DUB&airportQueryTime=18",
	"http://www.flightstats.com/go/FlightStatus/flightStatusByAirport.do?airportCode=DUB&airportQueryTime=19",
	"http://www.flightstats.com/go/FlightStatus/flightStatusByAirport.do?airportCode=DUB&airportQueryTime=20",
	"http://www.flightstats.com/go/FlightStatus/flightStatusByAirport.do?airportCode=DUB&airportQueryTime=21",
	"http://www.flightstats.com/go/FlightStatus/flightStatusByAirport.do?airportCode=DUB&airportQueryTime=22",
	"http://www.flightstats.com/go/FlightStatus/flightStatusByAirport.do?airportCode=DUB&airportQueryTime=23"]
	
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