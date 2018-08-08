from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import csv
import time

csv_file = open('healthgrades_tray_all2.csv', 'w')
writer = csv.writer(csv_file)

#<a href="javascript:document.frmMain.action.value='display_physician_info';document.frmMain.PhysicianID.value=12094889;document.frmMain.submit();" title="For more information, click here.">AHMED, SHAMIM</a>
driver = webdriver.Chrome()
# driver.implicitly_wait(15)
nyc_zips=['10457', '10460','10458', '10467', '10468','11201', '11215', '11217', '11206', '11221', '11237', '10026', '10027', '10030', '10037', '10039', '11412', '11423', '11432', '11433', '11434', '11435', '11436', '10306', '10307', '10308', '10309', '10312']#'11217']#,'11231','10453', 
base_link='https://www.healthgrades.com/usearch?what=OBGYN&entityCode=PS574&searchType=PracticingSpeciality&zip='
for zipcode in nyc_zips:
	link = base_link+zipcode
	driver.get(link)
	#driver.get(r"https://www.healthgrades.com/usearch?what=Obstetrics%20%26%20Gynecology&entityCode=PS574&searchType=PracticingSpecialty&spec=45&category=Provider&where=NYC%2C%20NY&pt=40.6501038%2C%20-73.9495823&distances=50&pageNum=1&source=Osm&city=NYC&state=NY")
	#driver.get(r"https://www.healthgrades.com/usearch?what=Obstetrics%20%26%20Gynecology&entityCode=PS574&searchType=PracticingSpecialty&spec=45&category=Provider&where=NYC%2C%20NY&pt=40.6501038%2C%20-73.9495823&distances=10&pageNum=1&source=Osm&city=NYC&state=NY")
	time.sleep(2)

	index = 1
	while index <=10:#True: #
		try:
			print("Scraping Page number " + str(index))
			index = index + 1
			time.sleep(2)

			doctors = driver.find_elements_by_xpath('//li[@class="uCard"]')
			print(len(doctors))
			for doctor in doctors:
				doctor_name=doctor.find_element_by_xpath('.//a').text
				print(doctor_name)
				try:
					# //*[@id="card-carousel-search"]/div[2]/ul/li[3]/div/div/div[1]/div/div[2]/div[2]/span[2]
					rating = doctor.find_element_by_xpath('.//div[@class="uCard__rating "]/span').get_attribute('aria-label')
					n_reviews = doctor.find_element_by_xpath('.//div[@class="uCard__rating "]/span[2]').get_attribute('aria-label')
					print(n_reviews)
				except Exception as e:
					rating=0
					n_reviews=0
					print(e)
					continue
				item={}
				item['Name']=doctor_name
				item['rating']=rating
				item['n_reviews']=n_reviews

				writer.writerow(item.values())
			doctors=[]
			next_page=driver.find_element_by_xpath('//div[@class="deck-shuffle"]/a')#.get_attribute('href')
			next_page.click()


		except Exception as e:
			print(e)
			#driver.close()
			break




