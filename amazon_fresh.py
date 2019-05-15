import scrapy
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from scrapy import Request
import time
from ankit.items import AnkitItem
from scrapy.http import FormRequest, TextResponse
from datetime import date
class Super(scrapy.Spider):
	name = "amazon"
	start_urls = ['https://www.amazon.com/b/?_encoding=UTF8&bbn=10329849011&node=11825099011&ref_=sv_fresh_1']
	def __init__(self, keyword=None, **kwargs):
		self.keyword = keyword
		self.driver = webdriver.Chrome()


	def parse(self,response):
		self.driver.get(response.url)
		new_dict = {}
		selector = TextResponse(url=response.url, body=self.driver.page_source, encoding='utf-8')
		time.sleep(4)
		close_button = self.driver.find_element_by_xpath('//*[@id="nav-main"]/div[1]/div[2]/div/div[3]/span[1]/span/input').click()
		time.sleep(4)
		grocery = self.driver.find_element_by_xpath('//*[@id="nav-subnav"]/a[4]/a').click()
		time.sleep(2)
		selector = TextResponse(url=response.url, body=self.driver.page_source, encoding='utf-8')
		items = selector.xpath('//div[@class="bxc-grid__image   bxc-grid__image--light"]/a/@href').extract()
		time.sleep(4)
		
		for url in items:
			full_url = 'https://www.amazon.com'+url
			print('-------------------------',full_url)
		
			yield Request(url = full_url, callback = self.parse2)


	def parse2(self,response):
		self.driver.get(response.url)
		
		time.sleep(3)
		selector = TextResponse(url=response.url, body=self.driver.page_source, encoding='utf-8')
		product_link = selector.xpath('//a[@class="a-link-normal"]/@href').extract()
		for i in product_link:
			product_href = 'https://www.amazon.com'+i

			yield Request(url = product_href, callback= self.parse3)

	def parse3(self,response):
		self.driver.get(response.url)
		time.sleep(2)
		new_dict = {}
		selector = TextResponse(url=response.url, body=self.driver.page_source, encoding='utf-8')
		product_name = selector.xpath('//span[@id="productTitle"]/text()').extract_first()
		product_name = product_name.strip()
		if not product_name:
			product_name = 'product_name is not mentioned'

		selector = TextResponse(url=response.url, body=self.driver.page_source, encoding='utf-8')
		product_brand = selector.xpath('//span[@id="productTitle"]/text()').extract_first()
		product_brand = product_brand.strip().split(' ')
		product_brand = product_brand[0:2]
		product_brand = ' '.join(product_brand)
		product_brand = product_brand.strip()
		product_brand = "".join(product_brand)
		if not product_brand:
			product_brand = "product_brand is not defined"


		product_quantity = selector.xpath('//span[@id="productTitle"]/text()').extract_first()
		product_quantity = product_quantity.split(',',-1)
		product_quantity = product_quantity[-1]
		product_quantity = product_quantity.strip()
		
		if not product_quantity:
			product_quantity = "product_quantity is not found"

		product_img = selector.xpath('//span[@class="a-button-text"]/img/@src').extract_first()
		product_img = str(product_img)
		if not product_img:
			product_img = "product image url not found"

		product_description = selector.xpath('//div[@id="productDescription"]/p/text()').extract()
		
		Product_Ingradients = selector.xpath('//span[contains(text(),"Ingredients")]//following-sibling::p//text()').extract()

		if not Product_Ingradients:
			Product_Ingradients = selector.xpath('//div[@class="content"]/h5[contains(text(),"Ingredients")]//following-sibling::text()').extract()
			if not Product_Ingradients:
				
				Product_Ingradients = None

		Product_Warning = selector.xpath('//span[contains(text(),"Safety Warning")]//following-sibling::p//text()').extract()
		if not Product_Warning:
			Product_Warning = selector.xpath('//div[@class="content"]/h5[contains(text(),"Safety Warning")]//following-sibling::text()').extract_first()
			if not Product_Warning:
			
				Product_Warning = None
					
		



		new_dict['Product_Name'] = product_name
		new_dict['Product_Price'] = None
		new_dict['Product_Code'] = None
		new_dict['Product_Brand'] = product_brand
		new_dict['Product_Image_Url'] = product_img
		new_dict['Product_Quantity'] = product_quantity
		new_dict['Product_URL'] = response.url
		new_dict['Website'] = 'bjs'
		new_dict['Product_Description'] = product_description
		new_dict['Product_Warning'] = Product_Warning
		new_dict['Product_Ingradients_list'] = Product_Ingradients
		new_dict['Cost_Per_Unit'] = None
		new_dict['Nutrition_dict'] = None
		new_dict['Store_Name'] = None
		new_dict['Product_Price_MSRP'] = None
		new_dict['Product_Price_Special'] = None
		new_dict['Product_Price_Special_Exp'] = None
		new_dict['Product_Price_Special_Information'] = None
		new_dict['Product_Price_Sale'] = None
		new_dict['Product_Price_Sale_Exp'] = None
		new_dict['Product_type'] = None
		new_dict['Product_category'] = None
		new_dict['Time_Stamp'] = date.today().isoformat()
		yield new_dict

		
		print("--------------------------",product_name)
		print('--------------------------',product_brand)
		print('--------------------------',product_quantity)
		print('--------------------------',product_description)
		print('--------------------------',product_img)
		print('===========================',Product_Warning)
		print("===========================",Product_Ingradients)