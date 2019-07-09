# import scrapy
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from scrapy import Request
# import time
# from ankit.items import AnkitItem
# from scrapy.http import FormRequest, TextResponse
# from datetime import date
# class Super(scrapy.Spider):
# 	name = "ypus"


# 	start_urls =['https://www.yellowpages.com/search?search_terms=hotel&geo_location_terms=new%20york&page=%s'% page for page in range(1,25)]

# 	def __init__(self, keyword=None, **kwargs):
# 		self.keyword = keyword
# 		self.driver = webdriver.Chrome()



# 	def parse(self,response):
# 		self.driver.get(response.url)
# 		time.sleep(2)
# 		# time.sleep(6)
		
# 		selector = TextResponse(url=response.url, body=self.driver.page_source, encoding='utf-8')
	
# 		# close_button = self.driver.find_element_by_xpath('//*[@id="helpIntro"]/div/div/div[1]/button/span').click()


# 		listing_titles = selector.xpath('//div[@class="info"]/h2/a/@href').extract()

# 		# print('-------------------------',listing_titles)

# 		for i in listing_titles:

# 			i = "https://www.yellowpages.com"+i
# 			print('-------------------------',i)


# 			yield Request(url = i, callback = self.parse2)




# 	def parse2(self,response):
# 		self.driver.get(response.url)
# 		time.sleep(1)
	
# 		selector = TextResponse(url=response.url, body=self.driver.page_source, encoding='utf-8')


# 		name = selector.xpath('//div[@class="sales-info"]/h1//text()').extract()

# 		address = selector.xpath('//*[@id="main-header"]/article/section[2]/div[1]/h2//text()').extract()
		

# 		phone = selector.xpath('//*[@id="main-header"]/article/section[2]/div[1]/p[1]//text()').extract()


# 		years_in_buisness = selector.xpath('//*[@id="main-header"]/article/section[2]/div[2]/div/div//text()').extract()


# 		info = selector.xpath('//dd[@class="general-info"]/p[1]//text()').extract()


# 		hours = selector.xpath('//*[@id="business-info"]/dl/dd[2]/div/table/tbody/tr/td/time//text()').extract()

# 		extra_phone = selector.xpath('//dd[@class="extra-phones"]/p/span[2]//text()').extract()

# 		services_product = selector.xpath('//*[@id="business-info"]/dl/dd[4]/p//text()').extract()


# 		brand = selector.xpath('//dd[@class="brands"]//text()').extract()



# 		payment = selector.xpath('//dd[@class="payment"]//text()').extract()


# 		neighbour = selector.xpath('//*[@id="business-info"]/dl/dd[8]/span/a//text()').extract()

# 		categories = selector.xpath('//dd[@class="categories"]/span/a//text()').extract()



# 		print("----------------------name---------------------",name)
# 		print("--------------------info-----------------------",info)
# 		print("--------------------address-----------------------",address)
# 		print("----------------------mob---------------------",phone)
# 		print("-----------------------hours--------------------",hours)
# 		print("-----------------------extra_phone--------------------",extra_phone)
# 		print("----------------------services_product---------------------",services_product)
# 		print("-----------------------brand--------------------",brand)
# 		print("------------------------payment-------------------",payment)
# 		print("------------------------neighbour-------------------",neighbour)
# 		print("------------------------categories-------------------",categories)

# 		new_dict = {}

# 		new_dict["Name"] = name
# 		new_dict["info"] = info
# 		new_dict["address"] = address
# 		new_dict["phone"] = phone
# 		new_dict["hours"] = hours
# 		new_dict["extra_phone"] = extra_phone
# 		new_dict["services_product"] = services_product
# 		new_dict["brand"] = brand
# 		new_dict["payment"] = payment
# 		new_dict["neighbour"] = neighbour
# 		new_dict["categories"] = categories
		
# 		yield new_dict