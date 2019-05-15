import scrapy
from selenium import webdriver
from scrapy import Request
import time
from scrapy.http import FormRequest ,TextResponse

class Super(scrapy.Spider):
	name = "fabindia"
	start_urls = ['https://www.fabindia.com/store-locator']
	def __init__(self, keyword=None, **kwargs):
		self.keyword = keyword
		self.driver = webdriver.Chrome()
	def parse(self,response):
		self.driver.get(response.url)
		time.sleep(4)
		new_dict = {}
		selector = TextResponse(url=response.url, body=self.driver.page_source, encoding='utf-8')
		city = selector.xpath('//div[@class="StoreLocationsList"]//ul/li//a/text()').extract()
		a = []
		a.append(city)
		for i in city:
			i = "'"+i+"'"
			self.driver.get(response.url)
			time.sleep(3)
			city = self.driver.find_element_by_xpath("//ul/li//a[contains(text(),"+i+")]").click()
			time.sleep(5)
			selector = TextResponse(url=response.url, body=self.driver.page_source, encoding='utf-8')
			address1 = selector.xpath('//div[@class="store-address"]')
			for add in address1:
				address = add.xpath('.//span//text()').extract()
				address = "".join(address).replace('/n','')
				new_dict["City"] = i
				new_dict["address"] = address
				yield new_dict