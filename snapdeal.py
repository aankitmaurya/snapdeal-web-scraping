#web scraping article by Ankit Kumar

import scrapy
from scrapy import Request

class quotespider(scrapy.Spider):
	name = 'phones'
	# name of spider is phones
	start_urls = [
'https://www.snapdeal.com/products/mobiles-mobile-phones/filters/Form_s~Smartphones?sort=plrty&q=Form_s%3ASmartphones%7C'	
		]

	def parse(self,response):
		href = response.xpath('//div[@class="product-tuple-image "]/a/@href').extract()
		
		for i in href:
			yield Request(url= i,callback= self.parse2) 

	def parse2(self,response):
		price = response.xpath('//span[@class="pdp-final-price"]/span/text()').get()
		title = response.xpath('//h1/text()').get()
		image_url = response.xpath('//ul[@id="bx-slider-left-image-panel"]/li/img/@src').get()
		Ram_size = response.xpath('//li[@class="col-xs-8 reset-padding"]/span/text()')[0].get()
		Screen_size = response.xpath('//li[@class="col-xs-8 reset-padding"]/span/text()')[1].get()
		Rear_camera = response.xpath('//li[@class="col-xs-8 reset-padding"]/span/text()')[2].get()
		Front_camera = response.xpath('//li[@class="col-xs-8 reset-padding"]/span/text()')[3].get()
		Internal_memory = response.xpath('//li[@class="col-xs-8 reset-padding"]/span/text()')[4].get()

		print("=====================NEXT PHONE======================")

		print("PRODUCT_TITLE",title.strip())
		print("PRICE",price)
		print("URL",image_url)
		print("RAM",Ram_size)
		print("SCREEN-SIZE",Screen_size)
		print("REAR-CAMERA",Rear_camera)
		print("FRONT-CAMERA",Front_camera)
		print("INTERNAL MEMORY",Internal_memory)		