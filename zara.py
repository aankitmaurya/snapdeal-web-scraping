import scrapy
from selenium import webdriver
from scrapy import Request
import time
from scrapy.http import FormRequest ,TextResponse
class Super(scrapy.Spider):
	name = "sprdry"
	start_urls = ['https://www.zara.com/in/en/z-stores-l1404.html?v1=11108']
	def __init__(self, keyword=None, **kwargs):
		self.keyword = keyword
		self.driver = webdriver.Chrome()
	def parse(self,response):
		self.driver.get(response.url)
		new_dict = {}
		selector = TextResponse(url=response.url, body=self.driver.page_source, encoding='utf-8')
		text_area = self.driver.find_element_by_xpath('//div/label[@for="store-locator-location"]').click()
		data = ['delhi','banglore','gurgoan','noida','ahamdabad','surat','jaipur','kolkata','chennai','hydrabad','pune','thane','chandigarh','mohali']
		for i in data:
			text_area = self.driver.find_element_by_xpath('//div/input[@id="store-locator-location"]').clear()
			text_area = self.driver.find_element_by_xpath('//div/input[@id="store-locator-location"]').send_keys(i)
			time.sleep(4)
			search_button = self.driver.find_element_by_xpath('//button[@class="button-primary button-big _searchStores"]')
			search_button.click()
			selector = TextResponse(url=response.url, body=self.driver.page_source, encoding='utf-8')
			city = selector.xpath('//a/span/span[@class="shop-info _shopInfo"]//text()').extract()
			# shop = selector.xpath('//a/span/strong[@class="shop"]//text()').extract()
			shop_address = selector.xpath('//div[@class="address"]//text()').extract()
			# for j in shop_address:
			new_dict["City"] = i,
			new_dict["address"] = shop_address
			yield new_dict