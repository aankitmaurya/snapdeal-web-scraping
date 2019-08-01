import scrapy
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from scrapy import Request
import time
from scrapy.http import FormRequest, TextResponse
from datetime import date
class Super(scrapy.Spider):
	name = "lybrate"
	# start_urls = ['https://www.lybrate.com/search?cityName=%s' % page for page in ['Gangtok']]
	start_urls = ['https://www.lybrate.com/search?cityName=%s' % page for page in ['Cuttack','Rourkela','Puri','Balasore']]
	def __init__(self, keyword=None, **kwargs):
		self.keyword = keyword
		self.driver = webdriver.Chrome()


	def parse(self,response):
		self.driver.get(response.url)
		time.sleep(2)
		
		selector = TextResponse(url=response.url, body=self.driver.page_source, encoding='utf-8')

		for page in range(1,2):
			full_url = response.url+'&page='+str(page)
		
			yield Request(url = full_url, callback = self.parse2)


	def parse2(self,response):
		self.driver.get(response.url)
		
		time.sleep(2)
		selector = TextResponse(url=response.url, body=self.driver.page_source, encoding='utf-8')
		category = selector.xpath('//div[@profile="profile"]/div[1]')
		for i in category:

			
			page_source = i.xpath('.//h2/a/@href').extract()
			k = []

			title = i.xpath('.//h2/a//text()').extract()
			if title:
				title = title[1:]
				for t in title:
					t = t.replace('\n','').replace('\t','')
					k.append(t)

			degree = i.xpath('.//div[@class="lybEllipsis ly-doctor__degree grid__col-20 ng-binding ng-scope"]//text()').extract_first()
			if (degree is None) :
				pass
			else:

				degree = degree.strip().replace('\n','').replace('\t','')

			speciality = i.xpath('.//div[@ng-if="ctrl.profile.specialityName"]//text()').extract_first()
			if speciality:
				speciality = speciality.strip()
			else:
				speciality = "speciality not found"

			clinic = i.xpath('.//div[@ng-if="ctrl.profile.clinicLocation.name"]//text()').extract()

			clinic = clinic[2:5:2]
			if not clinic:
				clinic = 'clinic name not found'

			clinic_location = i.xpath('.//span[@data-ng-if="ctrl.profile.clinicLocation.cityName && !ctrl.showFullAddress"]//text()').extract()
			clinic_location = clinic_location[2:6]
			a = []
			for j in clinic_location:

				j = j.strip().replace('\n\t\t\t\t\t','').replace('\t','')
				a.append(j)

			experience = i.xpath('.//div[@ng-if="ctrl.profile.experience && ctrl.profile.experience > 0"]//span//text()').extract()
			if not experience:
				experience = 'experience not found'
			rating = i.xpath('.//span[@ng-if="ctrl.profile.userRatings && ctrl.profile.userRatings > 0"]//text()').extract()
			if not rating:
				rating = 'rating not found'
			feedback = i.xpath('.//span[@ng-if="ctrl.profile.feedbackCount && ctrl.profile.feedbackCount > 0"]//text()').extract()
			if not feedback:
				feedback = None


			print('---------Doctor name--------',k)
			print('---------Education--------',degree)
			print('---------speciality--------',speciality)
			print('---------clinic--------',clinic)
			print('---------clinic_location--------',a)
			print('--------experience--------',experience)
			print('---------rating--------',rating)
			print('--------------feedback------------',feedback)
			print('----------------page_source----------------',page_source)
			print('====================================================== next doctor ================================================================')

			new_dict = {}

			new_dict['Doctor name'] = k
			new_dict['Education'] = degree
			new_dict['Specialty'] = speciality

			new_dict['Hospital/Clinic name'] = clinic
			new_dict['Address'] = a
			new_dict['Experience'] = experience
			new_dict['Rating'] = rating

			new_dict['# of patient feedback'] = feedback
			new_dict['page_source'] = page_source
			new_dict['State'] = 'Orissa'
			new_dict['Pincode'] = None
			new_dict['City'] = a

			yield new_dict






















# import scrapy
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from scrapy import Request
# import time
# from scrapy.http import FormRequest, TextResponse
# from datetime import date
# class Super(scrapy.Spider):
# 	name = "lybrate"
# 	# list1 = ['Bhubaneswar','Delhi']
# 	start_urls = ['https://www.lybrate.com/search?find=General%20Physician&near=&cityName=Bhubaneswar']
# 	def __init__(self, keyword=None, **kwargs):
# 		self.keyword = keyword
# 		self.driver = webdriver.Chrome()


# 	def parse(self,response):
# 		self.driver.get(response.url)
# 		time.sleep(3)
		
# 		selector = TextResponse(url=response.url, body=self.driver.page_source, encoding='utf-8')
	
# 		for page in range(1,5):
# 			full_url = 'https://www.lybrate.com/search?find=General%20Physician&near=&cityName=Bhubaneswar&page='+str(page)
# 			# print('---========================---',full_url)
		
# 			yield Request(url = full_url, callback = self.parse2)

# 	def parse2(self,response):
# 		self.driver.get(response.url)
		
# 		time.sleep(3)
# 		# print('================',response.url)
# 		selector = TextResponse(url=response.url, body=self.driver.page_source, encoding='utf-8')
# 		# name = selector.xpath('//h2/a//text()').extract()
# 		category = selector.xpath('//div[@profile="profile"]/div[1]')
# 		for i in category:

			
# 			page_source = i.xpath('.//h2/a/@href').extract()
# 			k = []

# 			title = i.xpath('.//h2/a//text()').extract()
# 			if title:
# 				title = title[1:]
# 				for t in title:
# 					t = t.replace('\n','').replace('\t','')
# 					k.append(t)

# 			degree = i.xpath('.//div[@class="lybEllipsis ly-doctor__degree grid__col-20 ng-binding ng-scope"]//text()').extract_first()
# 			if (degree is None) :
# 				pass
# 			else:

# 				degree = degree.strip().replace('\n','').replace('\t','')

# 			speciality = i.xpath('.//div[@ng-if="ctrl.profile.specialityName"]//text()').extract_first()
# 			if speciality:
# 				speciality = speciality.strip()
# 			else:
# 				speciality = "speciality not found"

# 			clinic = i.xpath('.//div[@ng-if="ctrl.profile.clinicLocation.name"]//text()').extract()

# 			clinic = clinic[2:5:2]
# 			if not clinic:
# 				clinic = 'clinic name not found'

# 			clinic_location = i.xpath('.//span[@data-ng-if="ctrl.profile.clinicLocation.cityName && !ctrl.showFullAddress"]//text()').extract()
# 			clinic_location = clinic_location[2:6]
# 			a = []
# 			for j in clinic_location:

# 				j = j.strip().replace('\n\t\t\t\t\t','').replace('\t','')
# 				a.append(j)

# 			# 	clinic_location = "".join(i)
# 			experience = i.xpath('.//div[@ng-if="ctrl.profile.experience && ctrl.profile.experience > 0"]//span//text()').extract()
# 			if not experience:
# 				experience = 'experience not found'
# 			rating = i.xpath('.//span[@ng-if="ctrl.profile.userRatings && ctrl.profile.userRatings > 0"]//text()').extract()
# 			if not rating:
# 				rating = 'rating not found'
# 			feedback = i.xpath('.//span[@ng-if="ctrl.profile.feedbackCount && ctrl.profile.feedbackCount > 0"]//text()').extract()
# 			if not feedback:
# 				feedback = None


# 			print('---------title--------',k)
# 			print('---------degree--------',degree)
# 			print('---------speciality--------',speciality)
# 			print('---------clinic--------',clinic)
# 			print('---------clinic_location--------',a)
# 			print('--------experience--------',experience)
# 			print('---------rating--------',rating)
# 			print('--------------feedback------------',feedback)
# 			print('----------------page_source----------------',page_source)
# 			print('====================================================== next doctor ================================================================')

# 			new_dict = {}

# 			new_dict['Name'] = k
# 			new_dict['Education'] = degree
# 			new_dict['speciality'] = speciality

# 			new_dict['clinic'] = clinic
# 			new_dict['clinic_location'] = a
# 			new_dict['experience'] = experience
# 			new_dict['rating'] = rating

# 			new_dict['feedback'] = feedback
# 			new_dict['page_source'] = page_source
# 			new_dict['state'] = 'Orisa'
# 			new_dict['city'] = 'Bhubaneswar'

# 			yield new_dict