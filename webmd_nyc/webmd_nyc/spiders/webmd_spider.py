# webmd_spider

from scrapy import Spider, Request
from webmd_nyc.items import WebmdNycItem
import re


class WebmdNycSpider(Spider):
	name = 'webmd_spider'
	allowed_urls = ['https://doctor.webmd.com/']
	# Manhattan start_urls = [r"https://doctor.webmd.com/results?sd=29285&tname=Obstetrics%20%26%20Gynecology&city=Manhattan&state=NY&zip=&lat=40.7834&lon=-73.9662&s=none&so="]
	# Queens start_urls=[r"https://doctor.webmd.com/results?sd=29285&tname=Obstetrics%20%26%20Gynecology&city=Queens&state=NY&zip=&lat=40.7498&lon=-73.7976&s=none&so="]
	nyc_zips=['10307']#,'11231','10453', '10457', '10460','10458', '10467', '10468','11201', '11215', '11217', '11206', '11221', '11237', '10026', '10027', '10030', '10037', '10039', '11412', '11423', '11432', '11433', '11434', '11435', '11436', '10306', '10307', '10308', '10309', '10312']
	start_urls=['https://doctor.webmd.com/results?sd=29285&tname=Obstetrics%20%26%20Gynecology&city=&state=&zip='+zipcode+'&lat=40.6936&lon=-73.9649&s=501&so=' for zipcode in nyc_zips]
	#start_urls= [r'https://doctor.webmd.com/results?sd=29285&tname=Obstetrics%20%26%20Gynecology&city=Brooklyn%20Heights&state=NY&zip=&lat=40.6953&lon=-73.9937&s=none&so=']
	# Brooklyn start_urls = [r"https://doctor.webmd.com/results?sd=29285&tname=Obstetrics%20%26%20Gynecology&city=Brooklyn&state=NY&zip=&lat=40.6501&lon=-73.9495&s=501&so="]
	def parse(self, response):
		# Find the total number of pages in the result so that we can decide how many urls to scrape next
		text=response.xpath('//*[@id="ContentPane33"]/section/div[3]/div[3]/ul/li[6]/a').extract()
		number_pages=20#int(re.search('pagenumber=[0-9]+',text[0]).group()[11:])
		# boro_urls = r"https://doctor.webmd.com/results?sd=29285&tname=Obstetrics%20%26%20Gynecology&city=Brooklyn%20Heights&state=NY&zip=&lat=40.6953&lon=-73.9937&s=none&so="
		nyc_zips=['10307']#,'11231','10453', '10457', '10460','10458', '10467', '10468','11201', '11215', '11217', '11206', '11221', '11237', '10026', '10027', '10030', '10037', '10039', '11412', '11423', '11432', '11433', '11434', '11435', '11436', '10306', '10307', '10308', '10309', '10312']
		start_urls=['https://doctor.webmd.com/results?sd=29285&tname=Obstetrics%20%26%20Gynecology&city=&state=&zip='+zipcode+'&lat=40.6936&lon=-73.9649&s=501&so=' for zipcode in nyc_zips]
		ind=0
		for zip_url in start_urls:
			# List comprehension to construct all the urls
			result_urls = [zip_url+'&pagenumber={}'.format(x) for x in range(1,number_pages)]
			filename='webmd_'+zip_url[ind]+'.csv'
			# next_page = response.xpath('//*[@id="next-onRight"]/a').extract()
			# if next_page:
			# 	next_href = next_page[0]
			# 	next_page_url = 
			# 	request = scrapy.Request(url=next_page_url)
			# 	yield request
			for url in result_urls[:10]:## SET TO TWO FOR DEBUGGING[:4]
				yield Request(url=url, callback=self.parse_result_page)

	def parse_result_page(self, response):
		# This fucntion parses the search result page.
		# We are looking for url of the detail page.
		detail_urls = response.xpath('//a[@class="doctorName"]').extract()
		rank_list=response.xpath('//*[@class="rating overall"]')
		# Yield the requests to the details pages, 
		# using parse_detail_page function to parse the response.
		for doc_ind in range(len(detail_urls)):
			doctor_name=response.xpath('//a[@class="doctorName"]/text()').extract()[doc_ind]
			doc_rank_long=rank_list[doc_ind].extract()
			try:
				doc_rank_str=re.search('data-rating="[0-5]"',doc_rank_long).group()
				doc_rank=int(doc_rank_str[13:14])
			except:
				#if re.search('data-rating=""',doc_rank_long).group()!=None:
				doc_rank=0

			item = WebmdNycItem()
			item['name'] = doctor_name
			item['rating'] = doc_rank

			yield item




