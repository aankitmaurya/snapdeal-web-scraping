import scrapy
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from scrapy import Request
import time
from ankit.items import AnkitItem
from scrapy.http import FormRequest, TextResponse
from datetime import date
class Super(scrapy.Spider):
	name = "bjs"
	start_urls = ['https://www.bjs.com/category/grocery-household-and-pet/3000000000000117223']
	def __init__(self, keyword=None, **kwargs):
		self.keyword = keyword
		self.driver = webdriver.Chrome()


	def parse(self,response):
		self.driver.get(response.url)
		new_dict = {}
		selector = TextResponse(url=response.url, body=self.driver.page_source, encoding='utf-8')
		time.sleep(3)
		
		shop_department = self.driver.find_element_by_xpath('//*[@id="page"]/div[1]/header/app-header-template/div/div/div[3]/div[2]/div/div[1]/div[2]/div/div/ul/li/button/div/span[1]').click()
		time.sleep(3)
		grocery = self.driver.find_element_by_xpath('//*[@id="page"]/div[1]/header/app-header-template/div/div/div[3]/div[2]/app-mega-menu-molecule/div/div/ul/li[1]/a').click()
		time.sleep(3)
		selector = TextResponse(url=response.url, body=self.driver.page_source, encoding='utf-8')
		url = selector.xpath('//a[@class="gb-refinement"]/@href').extract()
		time.sleep(4)
		for i in url:
			print(i)
			yield Request(url = i, callback = self.parse2)


	def parse2(self,response):
		self.driver.get(response.url)
		time.sleep(5)
		selector = TextResponse(url=response.url, body=self.driver.page_source, encoding='utf-8')
		sub_category_url = selector.xpath('//a[@class="gb-refinement"]/@href').extract()
		print("-----------------------",sub_category_url)
	
		for product_details in sub_category_url:
			
			yield Request(url = product_details, callback = self.parse3)
		if not sub_category_url:
			product_details = response.url
			
			print("=================parse2========================", product_details)

			yield Request(url = product_details, callback = self.parse3)



	def parse3(self,response):
		self.driver.get(response.url)
		time.sleep(4)
		selector = TextResponse(url=response.url, body=self.driver.page_source, encoding='utf-8')
		sub_category_url2 = selector.xpath('//a[@class="gb-refinement"]/@href').extract()
		print("-----------==============================------------",sub_category_url2)
	
		for product_details in sub_category_url2:
			
			yield Request(url = product_details, callback = self.parse4)
		if not sub_category_url2:
			product_details = response.url
			
			print("====================   parse3  =====================", product_details)

			yield Request(url = product_details, callback = self.parse4)


	def parse4(self,response):
		self.driver.get(response.url)
		time.sleep(5)
		selector = TextResponse(url=response.url, body=self.driver.page_source, encoding='utf-8')
		product = selector.xpath('//a[@id="gb-bjs--tile__image"]/@href').extract()
		for details in product:
			href = "https://www.bjs.com/"+details
			yield Request(url = href, callback = self.parse5)


	def parse5(self,response):
		self.driver.get(response.url)
		# print(response.url)
		new_dict = {}
		time.sleep(3)
		selector = TextResponse(url=response.url, body=self.driver.page_source, encoding='utf-8')

		product_name = selector.xpath('//div[@class="product-title-name"]//text()').extract_first()
		# product_name = "".join(product_name)
		if not product_name:
			product_name = "product_name not mentioned"

		product_brand = selector.xpath('//div[@class="product-title-name"]/text()').extract_first()
		product_brand = product_brand.strip().split(' ')
		product_brand = product_brand[0:2]
		product_brand = ' '.join(product_brand)
		product_brand = product_brand.strip()
		product_brand = "".join(product_brand)
		if not product_brand:
			product_brand = "product_brand is not defined"

		product_price = selector.xpath('//span[@class="price-display"]//text()').extract_first()
		product_price = "".join(product_price)
		if not product_price:
			product_price = selector.xpath('//span[@class="price-display green-Price"]//text()').extract_first()
			product_price = "".join(product_price)
			if not product_price:
				product_price = selector.xpath('//span[@class="price-display green-Price"]//text()').extract()
				if not product_price:
					product_price = 'product price not found'


		product_code = selector.xpath('//div[@class="prod-item-model-number"]/span//text()').extract_first()
		product_code = "".join(product_code)
		if not product_code:
			product_code = "product_code is not mentioned"

		product_description = selector.xpath('//div[@class="desc-table"]//text()').extract_first()
		product_description = "".join(product_description)
		if not product_description:
			product_description = "product_description not mentioned"

		specifications = self.driver.find_element_by_xpath('//p[@class="desktopAccordianHeading"]/span[@class="accordion-icon minus-icon bg-Carat_down active"]').click()
		time.sleep(2)
		selector = TextResponse(url=response.url, body=self.driver.page_source, encoding='utf-8')

		Ingredients = selector.xpath('//tr[@class="specs-table-row"]/th[contains(text(),"Ingredients")]//following-sibling::td//text()').extract()
		Ingredients = "".join(Ingredients)
		if not Ingredients:
			Ingredients = "Ingredients not mentioned"

		Warnings = selector.xpath('//tr[@class="specs-table-row"]/th[contains(text(),"Product Warnings")]//following-sibling::td//text()').extract()
		Warnings = "".join(Warnings)
		if not Warnings:
			Warnings = "Warnings not mentioned"

		product_type = selector.xpath('//ul/li[@class="breadcrumb-item "]/a[@_ngcontent-c25]//text()').extract()
		
		if len(product_type) > 1:
			product_type =  product_type[-1]
			product_type = "".join(product_type)
		
		else:
			product_type =  'product type not found'


		product_category = selector.xpath('//ul/li[@class="breadcrumb-item "]/a[@_ngcontent-c25]//text()').extract()
		if len(product_category) > 2:
			product_category =  product_category[-2]
			product_category  = "".join(product_category)
		else:
			product_category = 'product category not found'


		product_img = selector.xpath('//a[@class="RICHFXColorChangeLink"]/img/@src').extract()
		product_img = str(product_img)
		if not product_img:
			product_img = "img url not found"

		product_quantity = selector.xpath('//div[@class="product-title-name"]/text()').extract_first()
		product_quantity = product_quantity.split(',',-1)
		product_quantity = product_quantity[-1]
		product_quantity = product_quantity.split('/')
		product_quantity = product_quantity[-1]
		product_quantity = "".join(product_quantity)
		if not product_quantity:
			product_quantity = "product_quantity is not found"


		response.url = response.url
		response.url = "".join(response.url)
		if not response.url:
			response.url = "response url not found"

		new_dict['Product_Name'] = product_name
		new_dict['Product_Price'] = product_price
		new_dict['Product_Code'] = product_code
		new_dict['Product_Brand'] = product_brand
		new_dict['Product_Image_Url'] = product_img
		new_dict['Product_Quantity'] = product_quantity
		new_dict['Product_URL'] = response.url
		new_dict['Website'] = 'bjs'
		new_dict['Product_Description'] = product_description
		new_dict['Product_Warning'] = Warnings
		new_dict['Product_Ingradients_list'] = Ingredients
		# new_dict['Cost_Per_Unit'] = None
		# new_dict['Nutrition_dict'] = None
		# new_dict['Store_Name'] = None
		# new_dict['Product_Price_MSRP'] = None
		# new_dict['Product_Price_Special'] = None
		# new_dict['Product_Price_Special_Exp'] = None
		# new_dict['Product_Price_Special_Information'] = None
		# new_dict['Product_Price_Sale'] = None
		# new_dict['Product_Price_Sale_Exp'] = None
		new_dict['Product_type'] = product_type
		new_dict['Product_category'] = product_category
		new_dict['Time_Stamp'] = date.today().isoformat()
		# item['new_dict'] = new_dict
		item = AnkitItem()
		item['new_dict'] = new_dict
		yield item


