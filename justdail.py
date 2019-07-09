import scrapy
from scrapy.http import Request
import csv
import re,json
from datetime import datetime
from slugify import slugify
from scrapy.selector import Selector

class justdialSpider(scrapy.Spider):

	name = "just"

	def start_requests(self):
		url = ["https://www.justdial.com/Jaipur/Cafe"]
		for i in url:
			yield scrapy.Request(url=i, callback=self.parse)

	def parse (self,response):
		for i in range(1,50+1):
			url = response.url+"/page-"+str(i)
			yield Request(url=url, callback=self.parseListing ,priority=(100-i)*100)
		yield Request(url=response.url, callback=self.parse )

		

	def parseListing (self,response):
		# 1 - yz
		# 2 - wx
		# 3 - vu
		# 4 - ts
		# 5 - rq
		# 6 - po
		# 7 - nm
		# 8 - lk
		# 9 - ji
		# 0 - acb
		listing_product= response.xpath('//li[@class="cntanr"]')
		category = response.xpath('//h1[@class="sel lng_commn"]/text()').extract_first()

		for i in listing_product:
			url=i.xpath('.//@data-href').extract_first()
			title = i.xpath('.//span[@class="lng_cont_name"]/text()').extract_first()
			contact_number = i.xpath('.//p[@class="contact-info "]/span/a//span/@class').re(r'mobilesv icon-(.*)')
			contact_number = [w.replace('dc', '+').replace('fe', '(').replace('hg', ')').replace('ba', '-').replace('yz', '1').replace('wx', '2').replace('vu', '3').replace('ts', '4').replace('rq', '5').replace('po', '6').replace('nm', '7').replace('lk', '8').replace('ji','9').replace('acb','0') for w in contact_number]
			contact_number = "".join(contact_number)

			address = i.xpath('.//span[@class="cont_fl_addr"]/text()').extract_first()
			rating = i.xpath('.//span[@class="exrt_count"]/text()').extract_first()
			product_id = i.xpath('.//section[@class="jcar"]/@onclick').re_first(r'setsescookie(.*),')
			product_id = product_id.replace('(','').replace("'","")
			output = {}




			output['node_name_category'] = category
			output['node_name_title'] = title
			output['node_name_phones'] = contact_number
			output['node_name_address'] = address
			output['node_name_rating'] = rating
			output['node_name_url'] = url
			output['product_id'] = product_id
			yield output