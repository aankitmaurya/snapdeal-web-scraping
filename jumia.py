import scrapy
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from scrapy import Request
import time
from ankit.items import AnkitItem
from scrapy.http import FormRequest, TextResponse
from datetime import date
class Super(scrapy.Spider):
	name = "jumia"
	start_urls = ['https://www.jumia.co.ke/']
	# def __init__(self, keyword=None, **kwargs):
	# 	self.keyword = keyword
	# 	self.driver = webdriver.Chrome()


	def parse(self,response):
		# self.driver.get(response.url)
		# time.sleep(2)

	
		# selector = TextResponse(url=response.url, body=self.driver.page_source, encoding='utf-8')
		items = response.xpath('//a[@class="subcategory"]/@href').extract()

		print("=====================================lenth========================================================",len(items))

		for i in items:
			print(i)

			yield Request(url = i, callback = self.parse2)

	def parse2(self,response):
		# self.driver.get(response.url)
		
		# time.sleep(1)
		# selector = TextResponse(url=response.url, body=self.driver.page_source, encoding='utf-8')
		a = []
		product = response.xpath('//section[@class="products -mabaya"]/div[1]/a[@class="link"]/@href').extract()
		for j in product:
			try:
				a.append(j)
			except:
				None

		product = response.xpath('//section[@class="products -mabaya"]/div[2]/a[@class="link"]/@href').extract()
		for j in product:
			try:
				a.append(j)
			except:
				None

		product = response.xpath('//section[@class="products -mabaya"]/div[3]/a[@class="link"]/@href').extract()
		for j in product:
			try:
				a.append(j)
			except:
				None

		product = response.xpath('//section[@class="products -mabaya"]/div[4]/a[@class="link"]/@href').extract()
		for j in product:
			try:
				a.append(j)
			except:
				None

		product = response.xpath('//section[@class="products -mabaya"]/div[5]/a[@class="link"]/@href').extract()
		for j in product:
			try:
				a.append(j)
			except:
				None

		product = response.xpath('//section[@class="products -mabaya"]/div[6]/a[@class="link"]/@href').extract()
		for j in product:
			try:
				a.append(j)
			except:
				None

		product = response.xpath('//section[@class="products -mabaya"]/div[7]/a[@class="link"]/@href').extract()
		for j in product:
			try:
				a.append(j)
			except:
				None

		product = response.xpath('//section[@class="products -mabaya"]/div[8]/a[@class="link"]/@href').extract()
		for j in product:
			try:
				a.append(j)
			except:
				None

		product = response.xpath('//section[@class="products -mabaya"]/div[9]/a[@class="link"]/@href').extract()
		for j in product:
			try:
				a.append(j)
			except:
				None

		product = response.xpath('//section[@class="products -mabaya"]/div[10]/a[@class="link"]/@href').extract()
		for j in product:
			try:
				a.append(j)
			except:
				None

		product = response.xpath('//section[@class="products -mabaya"]/div[11]/a[@class="link"]/@href').extract()
		for j in product:
			try:
				a.append(j)
			except:
				None

		for each in a:
			# print("------------each----------------",each)

			yield Request(url = each, callback = self.parse3)

	def parse3(self,response):
		# self.driver.get(response.url)
		# time.sleep(1)
		new_dict = {}
		# selector = TextResponse(url=response.url, body=self.driver.page_source, encoding='utf-8')
		price = response.xpath('//div[@class="price-box"]/div/span//text()').extract()

		title = response.xpath('//span/h1[@class="title"]//text()').extract()

		category = response.xpath('//nav[@class="osh-breadcrumb"]/ul/li[2]/a/text()').extract()

		subcategory = response.xpath('//nav[@class="osh-breadcrumb"]/ul/li/a/text()')[-2].extract()

		print('=================',price)
		print('=================',title)
		print('========subcategory=========',subcategory)
		print('=======category==========',category)
		print('=================',response.url)

		new_dict = {}

		new_dict["Title"] = title
		new_dict["price"] = price
		new_dict["subcategory"] = subcategory
		new_dict["category"] = category
		new_dict["page_source"] = response.url

		yield new_dict