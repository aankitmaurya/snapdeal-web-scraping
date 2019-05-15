import scrapy
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from scrapy import Request
import time
from ankit.items import AnkitItem
from scrapy.http import FormRequest, TextResponse
from datetime import date
class Super(scrapy.Spider):
	name = "rochebros"
	start_urls = ['https://shopping.rochebros.com/shop/categories']
	def __init__(self, keyword=None, **kwargs):
		self.keyword = keyword
		self.driver = webdriver.Chrome()


	def parse(self,response):
		self.driver.get(response.url)
		time.sleep(6)
		
		selector = TextResponse(url=response.url, body=self.driver.page_source, encoding='utf-8')
	
		close_button = self.driver.find_element_by_xpath('//*[@id="shopping-selector-parent-process-modal-close-click"]').click()
		time.sleep(5)
		
		selector = TextResponse(url=response.url, body=self.driver.page_source, encoding='utf-8')
		items = selector.xpath('//li[@class="subcategory category ng-scope ng-isolate-scope"]/a/@href').extract()
		time.sleep(6)

		for url in items:
			full_url = 'https://shopping.rochebros.com'+url
			print('-------------------------',full_url)
		
			yield Request(url = full_url, callback = self.parse2)

# https://shopping.rochebros.com/shop/categories
	def parse2(self,response):
		self.driver.get(response.url)
		
		time.sleep(5)
		selector = TextResponse(url=response.url, body=self.driver.page_source, encoding='utf-8')
		category = selector.xpath('//li[@class="subcategory category ng-scope ng-isolate-scope"]/a/@href').extract()
		for full in category:
			full = 'https://shopping.rochebros.com'+full
			print('=======================================',full)
		
			yield Request(url = full, callback = self.parse3)

	def parse3(self,response):
		self.driver.get(response.url)
		time.sleep(8)
		new_dict = {}
		selector = TextResponse(url=response.url, body=self.driver.page_source, encoding='utf-8')
		image_url = selector.xpath('//div[@class="cell-image-wrapper"]/a/@data-src').extract_first()

		product = self.driver.find_element_by_xpath('//div[@class="cell-image-wrapper"]').click()
		time.sleep(5)

		selector = TextResponse(url=response.url, body=self.driver.page_source, encoding='utf-8')
		product_name = selector.xpath('//div[@class="product-info"]/h2[@ng-bind-html="productTitle()"]//text()').extract_first()
		print("=====product_name=======",product_name)
		product_name = "'"+product_name+"'"


		# selector = TextResponse(url=response.url, body=self.driver.page_source, encoding='utf-8')
		# if selector.xpath('//ul[@class="breadcrumbs ng-scope"]/li[6]/a[contains(text(),'+product_name+')]'):
		# 	selector = TextResponse(url=response.url, body=self.driver.page_source, encoding='utf-8')
		# 	product_url = selector.xpath('//ul[@class="breadcrumbs ng-scope"]/li[6]/a/@href').get()
		# 	product_url = "https://shopping.rochebros.com"+product_url


		# selector = TextResponse(url=response.url, body=self.driver.page_source, encoding='utf-8')
		# if selector.xpath('//ul[@class="breadcrumbs ng-scope"]/li[7]/a[contains(text(),'+product_name+')]'):
		# 	selector = TextResponse(url=response.url, body=self.driver.page_source, encoding='utf-8')
		# 	product_url = selector.xpath('//ul[@class="breadcrumbs ng-scope"]/li[7]/a/@href').get()
		# 	product_url = "https://shopping.rochebros.com"+product_url
		# else:
		# 	product_url = "product_url not found "
		



		product_quantity = selector.xpath('//div[@class="product-info"]/h2[@ng-bind-html="productTitle()"]//text()').extract_first()
		product_quantity = product_quantity.split(',',-1)
		product_quantity = product_quantity[-1]
		product_quantity = product_quantity.strip()
		print("=====product_quantity=======",product_quantity)

		if not product_quantity:
			product_quantity = "product_quantity is not found"

		product_category = selector.xpath('//ul[@class="breadcrumbs ng-scope"]/li/a[@class="ng-binding ng-scope"]//text()').extract()
		
		product_category =  product_category[0]
		product_category  = "".join(product_category)
		print("=====product_category=======",product_category)
		if not product_category:
			product_category = 'product category not found'



		product_type = selector.xpath('//ul[@class="breadcrumbs ng-scope"]/li/a[@class="ng-binding ng-scope"]//text()').extract()
		print("+++++++++++++++++++++++++++++++++++++++++++",len(product_type))
		
		product_type =  product_type[-1]
		product_type  = "".join(product_type)
		print("=====product_type=======",product_type)
		if not product_type:
			product_type = 'product category not found'



		product_price = selector.xpath('//span[@class="amount ng-binding"]//text()').extract_first()
		product_price = "".join(product_price)
		print("=====product_price=======",product_price)



		product_brand = selector.xpath('//div[@class="product-info"]/h2/text()').extract_first()
		product_brand = product_brand.strip().split(' ')
		product_brand = product_brand[0:1]
		
		if not product_brand:
			product_brand = "product_brand is not defined"


		try:
			Ingredients_click = self.driver.find_element_by_xpath('//div[@ng-if="product.ingredients"]').click()
			time.sleep(2)
			selector = TextResponse(url=response.url, body=self.driver.page_source, encoding='utf-8')
			Ingredients = selector.xpath('//p[@class="ng-binding"]//text()').extract()
			
			Ingredients = "".join(Ingredients)
			Ingredients = str(Ingredients)
			Ingredients = Ingredients.strip()
			Ingredients = Ingredients.replace('\\n', '')
			Ingredients = Ingredients.replace('u' '', '')
			
		except:
			Ingredients = None

		try:
			tab = self.driver.find_element_by_xpath('//div[@ng-if="product.warnings"]').click()
			time.sleep(2)
			selector = TextResponse(url=response.url, body=self.driver.page_source, encoding='utf-8')
			Warnings = selector.xpath('//p[@class="ng-binding"]//text()').extract()
			
			# warnings = "".join(warnings)
			# warnings = str(warnings)
			# Warnings = Warnings.strip()
			# warnings = warnings.replace('\\n', '')
			# warnings = warnings.replace('u' '', '')


		except:
			Warnings = None

		selector = TextResponse(url=response.url, body=self.driver.page_source, encoding='utf-8')
		product_url = selector.xpath('//ul[@class="breadcrumbs ng-scope"]/li/a/@href')[-1].get()
		product_url = "https://shopping.rochebros.com"+product_url


		Nutrition_dict = {}

		try:
			tab = self.driver.find_element_by_xpath('//div[@ng-if="product.nutrition"]').click()
			time.sleep(5)
			selector = TextResponse(url=response.url, body=self.driver.page_source, encoding='utf-8')

			# Nutrition_dict = {}

			value = ['Energy','Protein','Total Fat','Total Carbohydrate', 'Dietary Fiber', 'Sugars',
				'Sodium', 'Potassium', 'Saturated Fat', 'Monounsaturated Fat', 'Polyunsaturated Fat',
				'Trans Fat', 'Cholesterol']
			# for small in value:
			# 	small = small.lower()


			# selector = TextResponse(url=response.url, body=self.driver.page_source, encoding='utf-8')

				# alltext = selector.xpath('//div[@class="nutrition-info"]//text()').extract()
			alltext = selector.xpath('//div[@class="extras-content"]//div[@class="ng-binding"]')
			print("---------------=======alltext=================================-------------",alltext)

			for one in alltext:
				nut = one.xpath('.//text()').extract_first()

				print("---------------======================nut==================-------------",nut)
					# alltext_lower in nut:
				# nut = nut.strip()
				# nut = nut.lower()

				# for small in value:
				# 	small = small.lower()

				# 	if (small in nut):
				# 		print("+++++++++++++++++++++++++++++++++++++++++++++++",small)

							# for each in small: 
							# 	each = "'"+each+"'"

							# 	selector = TextResponse(url=response.url, body=self.driver.page_source, encoding='utf-8')

							# 	Ingradients_value = selector.xpath('//section[@class="ng-scope"]/div[contains(text(),'+each+')]//following-sibling::text()').extract()













			# for each_item_value in value:
			# 	print("================each_item_value========================",each_item_value)
			# 	each_item_value = "'"+each_item_value+"'"

			# 	selector = TextResponse(url=response.url, body=self.driver.page_source, encoding='utf-8')
				
			# 	try:
			# 		# Ingradients_value = selector.xpath('//section[contains(text(),'+each_item_value+')]//following-sibling::text()').extract()
			# 		Ingradients_value = selector.xpath('//section[@class="ng-scope"]//div[@class="ng-binding"]/b[contains(text(),'+each_item_value+')]//following-sibling::text()').extract()
			# 		# Ingradients_value = Ingradients_value
			# 		print("================Ingradients_value=========================",Ingradients_value)


			# 		# if not Ingradients_value:
			# 			# Ingradients_value = selector.xpath('//section[@class="ng-scope"]//div[@class="ng-binding"]/b[contains(text(),'+each_item_value+')]//following-sibling::text()').extract()

			# 	except:
			# 		Ingradients_value = None


				# Nutrition_dict[each_item_value] = Ingradients_value


				# try:
				# 	if:
				# 		Ingradients_value = selector.xpath('//section[@class="ng-scope"]//div[@class="ng-binding"]/b[contains(text(),'Total Fat')]//following-sibling::text()').extract()
				






			# percentage = ['Calcium', 'Iron', 'Vitamin C', 'Vitamin A', 'Thiamin', 'Riboflavin', 'Niacin',
			# 			'Pantothenic acid', 'Vitamin B-6', 'Vitamin B-12', 'Vitamin D',"Vitamin B-6"]

			# for each_item_percentage in percentage:
			# 	print("======================each_item_percentage=====================",each_item_percentage)
		
			# 	each_item_percentage = "'"+each_item_percentage+"'"

			# 	selector = TextResponse(url=response.url, body=self.driver.page_source, encoding='utf-8')
			# 	try:
			# 		Ingradients_percentage = selector.xpath('//section[@class="ng-scope"]//div[@class="ng-binding"]/b[contains(text(),'+each_item_percentage+')]//preceding-sibling::div[@class="right"]//text()').extract()
			# 		print("=====================Ingradients_percentage======================",Ingradients_percentage)


			# 	except:

			# 		Ingradients_percentage = None


			# 	Nutrition_dict[each_item_percentage] = Ingradients_percentage



		except:
			Nutrition_dict = None


		yield Nutrition_dict

		# print("--------------------------",product_name)
		# print('--------------------------',product_brand)
		# print('--------------------------',product_quantity)
		# print('--------------------------',product_type)
		# print('--------------------------',product_category)
		# print('--------------------------',product_price)
		# print("===========================",Ingredients)
		# print('===========================',Warnings)
		# print('===========================',product_url)
		# print('===========================',Nutrition_dict)




		new_dict['Product_Name'] = product_name
		new_dict['Product_Price'] = product_price
		new_dict['Product_Code'] = None
		new_dict['Product_Brand'] = product_brand
		new_dict['Product_Image_Url'] = image_url
		new_dict['Product_Quantity'] = product_quantity
		new_dict['Product_URL'] = product_url
		new_dict['Website'] = 'bjs'
		new_dict['Product_Description'] = None
		new_dict['Product_Warning'] = Warnings
		new_dict['Product_Ingradients_list'] = Ingredients
		new_dict['Cost_Per_Unit'] = None
		new_dict['Nutrition_dict'] = Nutrition_dict
		new_dict['Store_Name'] = None
		new_dict['Product_Price_MSRP'] = None
		new_dict['Product_Price_Special'] = None
		new_dict['Product_Price_Special_Exp'] = None
		new_dict['Product_Price_Special_Information'] = None
		new_dict['Product_Price_Sale'] = None
		new_dict['Product_Price_Sale_Exp'] = None
		new_dict['Product_type'] = product_type
		new_dict['Product_category'] = product_category
		new_dict['Time_Stamp'] = date.today().isoformat()

		yield new_dict