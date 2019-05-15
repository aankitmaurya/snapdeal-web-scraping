# -*- coding: utf-8 -*-
import scrapy
# from wallet.items import WalletItem
import re
# import pymysql
# class WalletPipeline(object):

#     def __init__(self):
        
#         self.host = 'localhost'
#         self.user = 'root'
#         self.password = 'root'
#         self.db = 'wallet'
#         self.connection = pymysql.connect(host=self.host,user= self.user, password=self.password, db=self.db)
    
#     def connect():
#         connection = pymysql.connect(host='localhost',user= 'root', password='root', db='wallet')
#         if connection:
#             print('--------------------------connected')
#         else:
#             print('+++++++++++++++++++++++++++++++++++++not connected')


class FlipkartSpider(scrapy.Spider):
    name = "flipkart"
    allowed_domains = ["flipkart.com"]
    start_urls = ['https://www.flipkart.com/bags-wallets-belts/wallets-clutches/wallets/pr?count=40&p%5B%5D=facets.discount_range_v1%255B%255D%3D60%2525%2Bor%2BMore&sid=reh%2Fcca%2Fh76&fm=neo%2Fmerchandising&iid=M_acabadb9-4911-4438-8049-0e8dbfc2480c_18.3HCZHOH0UZ&ppt=Homepage&ppn=Homepage&otracker=hp_omu_Mid%2BSeason%2BClearance%2BSale_1_Min.%2B60%2525%2BOff_3HCZHOH0UZ_1&cid=3HCZHOH0UZ&page=1']

    def parse(self, response):
        pages = response.xpath('//a[@class="_2Xp0TH"]/@href').extract()
        result = 'https://www.flipkart.com'
        for urls in pages:
            results = result + urls
            # print '--------',results
            yield scrapy.Request(url = results,callback=self.product_urls)
    def product_urls(self, response):
        # print('+++++',response.url)
        product_urls = response.xpath('//a[@class="Zhf2z-"]/@href').extract() 
        result = 'https://www.flipkart.com'
        for urls in product_urls:
            results = result + urls
            # print('......',results)
            yield scrapy.Request(url = results,callback=self.asdf,meta={'asd':results})
    def asdf(self,response):
        print('++++++',response)    
        title_name =response.xpath('//a[@class="_2cLu-l"]/text()').extract() or response.xpath('//span[@class="_35KyD6"]/text()').extract() 
        # print('........',title_name)

        price = response.xpath('//div[@class="_1uv9Cb"]/div[@class="_1vC4OE _3qQ9m1"]/text()').extract_first() or response.xpath('//div[@class="_1uv9Cb"]/div[@class="_1vC4OE _3qQ9m1"]/text()').extract_first()
        # print('......',price)
	price = str(price)
	price = price.replace("₹","")

        mrp = response.xpath('//div[@class="_3auQ3N"]/text()').extract() or response.xpath('//div[@class="_3auQ3N _1POkHg"]/text()').extract()
        if mrp:
            mrp = mrp[1]
        # print('+++++++++++',mrp)

        offer= response.xpath('//div[@class="VGWI6T _1iCvwn _9Z7kX3"]/span/text()').extract() or response.xpath('//div[@class="VGWI6T _1iCvwn"]/span/text()').extract()
        # print('++++++++',offer)

        rating = response.xpath('//div[@class="hGSR34 _2beYZw bqXGTW"]/text()').extract_first() or response.xpath('//div[@class="hGSR34 _1x2VEC"]/text()').extract_first()
        # print('........',rating)

        #review = response.xpath('//span[@class="_38sUEc"]/span/text()').extract_first() or response.xpath('//span[@class="_38sUEc"]/span/span/text()').extract_first()
        # print('.....',review)

        new_dict = {'title_name':title_name,'price':price,'mrp':mrp,'offer':offer,'rating':rating}
        new_dict['results'] = response.meta['asd']
        
        # print(new_dict)
        yield new_dict
        #asd = WalletItem()
     #   asd['title_name'] = title_name
      #  asd['price'] = price
       # asd['mrp'] = mrp
        #asd['offer'] = offer
        #asd['rating'] = rating
      #  asd['review'] = review
#         # print '----------',asd
#         yield asd
# total_products = response.xpath('//div[@class="pagination"]/p/text()').extract_first()
        # print '--------',total_products
        # total_products = int(total_products) if total_products else None
        # total_pages = total_products/31 if total_products else 0

        # for i in range(1,total_pages+1):
        #   page_url = 'https://www.yellowpages.com/search?search_terms=Bakery&geo_location_terms=Cardiff%2C%20CA&page=' + str(i)
        #   print '-------------',page_url
        #   # print '+++++++++++++++++++++',len(product_urls)
    #   # result = 'https://www.yellowpages.com'
    #   # for url in product_urls:
    #   #   results = result + url
    #   #   print '------',results

    # https://www.flipkart.com/bags-wallets-belts/wallets-clutches/wallets/pr?count=40&p%5B%5D=facets.discount_range_v1%255B%255D%3D60%2525%2Bor%2BMore&sid=reh%2Fcca%2Fh76&fm=neo%2Fmerchandising&iid=M_acabadb9-4911-4438-8049-0e8dbfc2480c_18.3HCZHOH0UZ&ppt=Homepage&ppn=Homepage&otracker=hp_omu_Mid%2BSeason%2BClearance%2BSale_1_Min.%2B60%2525%2BOff_3HCZHOH0UZ_1&cid=3HCZHOH0UZ&page=2
    # https://www.flipkart.com/bags-wallets-belts/wallets-clutches/wallets/pr?count=40&p%5B%5D=facets.discount_range_v1%255B%255D%3D60%2525%2Bor%2BMore&sid=reh%2Fcca%2Fh76&fm=neo%2Fmerchandising&iid=M_acabadb9-4911-4438-8049-0e8dbfc2480c_18.3HCZHOH0UZ&ppt=Homepage&ppn=Homepage&otracker=hp_omu_Mid%2BSeason%2BClearance%2BSale_1_Min.%2B60%2525%2BOff_3HCZHOH0UZ_1&cid=3HCZHOH0UZ&page=1
