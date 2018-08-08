from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import csv
import time

#<a href="javascript:document.frmMain.action.value='display_physician_info';document.frmMain.PhysicianID.value=12094889;document.frmMain.submit();" title="For more information, click here.">AHMED, SHAMIM</a>
driver = webdriver.Chrome()
driver.get("https://www.nydoctorprofile.com/dispatch?action=process_welcome")

go_to_search = driver.find_element_by_xpath("//*[@id='frmMain']/table/tbody/tr/td/table[2]/tbody/tr/td[2]/table/tbody/tr/td[2]/table[1]/tbody/tr[3]/td/table/tbody/tr[6]/td[3]/input")
go_to_search.click()

specialty_opts= driver.find_element_by_name("SpecialtyGroupParam")
specialty_opts.click()
for option in specialty_opts.find_elements_by_tag_name("option"):
	if option.text == "Obstetrics and Gynecology":
		option.click()
		break

counties= driver.find_element_by_name("CountyFipsCodeParam")
counties.click()
county_options=counties.find_elements_by_tag_name("option")
# for test in county_options:
# 	print(test.text)
for option in county_options:
	#wait_counties = WebDriverWait(driver, 10)
	# next_counties = wait_counties.until(EC.element_to_be_clickable(counties)) #(By.XPATH,'//img[@name="go11"]')
	# next_counties.click()
	counties= driver.find_element_by_name("CountyFipsCodeParam")
	counties.click()
	if option.text != "Any":
		print('-'*50)
		print(option.text)
		# if option.text == "Brooklyn (Borough)":
		option.click()
			# break
		search_it_up=driver.find_element_by_xpath('//*[@id="frmMain"]/table/tbody/tr/td/table[2]/tbody/tr/td[2]/table/tbody/tr/td[2]/table[1]/tbody/tr[3]/td/table/tbody/tr[19]/td[1]/input')
		search_it_up.click()

		csv_file = open('GynoNYS.csv', 'w')
		writer = csv.writer(csv_file)

		# Page index used to keep track of where we are.
		index = 1
		# We want to start the first two pages.
		# If everything works, we will change it to while True
		while index <=1:
			try:
				print("Scraping Page number " + str(index))
				index = index + 1
				table_xpath='//*[@id="frmMain"]/table/tbody/tr/td/table[2]/tbody/tr/td[2]/table/tbody/tr/td[2]/table[1]/tbody/tr[2]/td/table[2]/tbody/tr/td/table[2]/tbody/tr'
				page_table=driver.find_elements_by_xpath(table_xpath)
				print(len(page_table))
				print('-'*50)

				for i in [0]:#range(len(page_table)): 
					phys_dict = {}
					phys_xpath=table_xpath+'['+str(i+1)+']/td[1]/a'
					physician_link=driver.find_element_by_xpath(phys_xpath)
								
					name=physician_link.text
					print(name)
					physician_link.click()

					#med school education
					ed_link=driver.find_element_by_xpath('//img[@name="ed"]')
					ed_link.click()
					education=driver.find_element_by_xpath('//*[@id="frmMain"]/table[4]/tbody/tr/td/table[1]/tbody/tr[2]/td').text

					#practice info
					field_link=driver.find_element_by_xpath('//img[@width="111"]')
					field_link.click()
					field_med=driver.find_element_by_xpath('//*[@id="frmMain"]/table[3]/tbody/tr[4]/td/table/tbody/tr/td/table[2]/tbody/tr[2]/td[1]').text
					print(field_med)

					# malpractice lawsuits
					mal_link=driver.find_element_by_xpath('//img[@width="120"]')
					mal_link.click()
					malpractice=driver.find_element_by_xpath('//*[@id="frmMain"]/table[4]/tbody/tr/td/table[2]/tbody/tr/td').text
					if malpractice!="None reported":
						print('malpractice!!')
						full_mal=driver.find_elements_by_xpath('//*[@id="frmMain"]/table[4]/tbody/tr')
						malpractice=full_mal[0].text
						# test=driver.find_elements_by_xpath("//*[contains(text(), 'Number of payments: ')]")
						# print(test.text)
						# t=1
						# for item in full_mal:
						# 	print(t)
						# 	print('-'*50)
						# 	print(item.text)
						# 	t+=1

					#save to my dictionary
					phys_dict['name'] = name
					phys_dict['education'] = education
					phys_dict['field_med'] = field_med
					phys_dict['malpractice'] = malpractice
					writer.writerow(phys_dict.values())

					#go back to results page:
					back_button=driver.find_element_by_xpath('//img[@name="prn"]')
					back_button.click()

				#go to next page of results
				next_page=driver.find_element_by_xpath('//img[@name="go31"]')
				next_page.click()

			# Iterate through the table of physicians
			# for physician in page_table:
			# 	# Initialize an empty dictionary for each review
			# 	review_dict = {}
			# 	# Use relative xpath to locate the title, content, username, date, rating.
			# 	# Once you locate the element, you can use 'element.text' to return its string.
			# 	# To get the attribute instead of the text of each element, use `element.get_attribute()`
			# 	title = review.find_element_by_xpath('.//div[@itemprop="headline"]').text
			# 	rating = review.find_element_by_xpath('.//span[@itemprop="ratingValue"]').text
			# 	print(rating)
			# 	#print(title)
			# 	# Your code here
			# 	review_body = review.find_element_by_xpath('.//span[@itemprop="reviewBody"]').text
				#print(review_body)
			# Locate the next button element on the page and then call `button.click()` to click it.
			# button = driver.find_element_by_xpath('//li[@class="nextClick displayInlineBlock padLeft5 "]')
			# button.click()
			# time.sleep(2) # to wait for loading the internet

				print('+'*50)
				print("new county")
				wait_button = WebDriverWait(driver, 20)
				next_button = wait_button.until(EC.element_to_be_clickable((By.XPATH,
									'//img[@name="go11"]')))
				next_button.click()
				time.sleep(4)

				# search_again=driver.find_element_by_xpath('//img[@name="go11"]')
				# search_again.click()
			except Exception as e:
				print(e)
				#driver.close()
				#break
				print('+'*50)
				print("new county- exception")
				wait_button = WebDriverWait(driver, 20)
				next_button = wait_button.until(EC.element_to_be_clickable((By.XPATH,
									'//img[@name="go11"]')))
				next_button.click()
				continue

# Search Results: COME BACK LATER
#test=driver.find_element_by_xpath('//*[@id="frmMain"]/table/tbody/tr/td/table[2]/tbody/tr/td[2]/table/tbody/tr/td[2]/table[1]/tbody/tr[2]/td/table[1]/tbody/tr[1]/td/p/') #text()[1]
#test=driver.find_element_by_xpath('//*[@id="frmMain"]/table/tbody/tr/td/table[2]/tbody/tr/td[2]/table/tbody/tr/td[2]/table[1]/tbody/tr[2]/td/table[1]/tbody/tr[1]/td/p/br[1]')
#test=driver.find_element_by_xpath('//p[@class="data"').text
