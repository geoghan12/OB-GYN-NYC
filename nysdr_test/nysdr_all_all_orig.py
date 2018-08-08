from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import csv
import time

#<a href="javascript:document.frmMain.action.value='display_physician_info';document.frmMain.PhysicianID.value=12094889;document.frmMain.submit();" title="For more information, click here.">AHMED, SHAMIM</a>
driver = webdriver.Chrome()
driver.implicitly_wait(15)
driver.get("https://www.nydoctorprofile.com/dispatch?action=process_welcome")

delay=20

go_to_search = driver.find_element_by_xpath("//*[@id='frmMain']/table/tbody/tr/td/table[2]/tbody/tr/td[2]/table/tbody/tr/td[2]/table[1]/tbody/tr[3]/td/table/tbody/tr[6]/td[3]/input")
go_to_search.click()

csv_file = open('allNYS_obgyn.csv', 'w')
writer = csv.writer(csv_file)

specialty_button= driver.find_element_by_name("SpecialtyGroupParam")
specialty_button.click()
specialty_opts=specialty_button.find_elements_by_tag_name("option")
five_boros=[3,4,5,26,30,34,44,45,55]
#specialty_opts=["Obstetrics and Gynecology"]
for s_ind in [13]:#range(len(specialty_opts)):
	specialty_button= driver.find_element_by_name("SpecialtyGroupParam")
	specialty_button.click()
	specialty_opts=specialty_button.find_elements_by_tag_name("option")
	curr_specialty=specialty_opts[s_ind]

	if curr_specialty.text!="Any":
		print('-'*50)
		print(curr_specialty.text)
		curr_specialty.click()
		#could use PASS here for more efficiency?

		counties= driver.find_element_by_name("CountyFipsCodeParam")
		counties.click()
		county_options=counties.find_elements_by_tag_name("option")

		for c_ind in five_boros:#range(len(county_options)):
			#wait_counties = WebDriverWait(driver, 10)
			# next_counties = wait_counties.until(EC.element_to_be_clickable(counties)) #(By.XPATH,'//img[@name="go11"]')
			# next_counties.click()
			counties= driver.find_element_by_name("CountyFipsCodeParam")
			counties.click()
			county_opt_tmp=counties.find_elements_by_tag_name("option")
			#choose the Next county
			option=county_opt_tmp[c_ind]
			if option.text != "Any":
				print('-'*50)
				print(option.text)
				county=option.text
				option.click()
				search_it_up=driver.find_element_by_xpath('//*[@id="frmMain"]/table/tbody/tr/td/table[2]/tbody/tr/td[2]/table/tbody/tr/td[2]/table[1]/tbody/tr[3]/td/table/tbody/tr[19]/td[1]/input')
				search_it_up.click()

				# csv_file = open('allNYS3.csv', 'w')
				# writer = csv.writer(csv_file)

				# Page index used to keep track of where we are.
				index = 1
				# We want to start the first two pages.
				# If everything works, we will change it to while True
				while True: #index <=1:
					try:
						print("Scraping Page number " + str(index))
						index = index + 1
						table_xpath='//*[@id="frmMain"]/table/tbody/tr/td/table[2]/tbody/tr/td[2]/table/tbody/tr/td[2]/table[1]/tbody/tr[2]/td/table[2]/tbody/tr/td/table[2]/tbody/tr'
						page_table=driver.find_elements_by_xpath(table_xpath)
						print(len(page_table))
						print('-'*50)

						for i in range(len(page_table)): 
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
							print(education)

							#practice info
							field_link=driver.find_element_by_xpath('//img[@width="111"]')
							field_link.click()

							# '//*[@id="frmMain"]/table[4]'
							# '//*[@id="frmMain"]/table[4]/tbody/tr/td/table[2]/tbody/tr/td'
							field_xpath='//*[@id="frmMain"]/table[3]/tbody/tr[4]/td/table/tbody/tr/td/table[2]/tbody/tr[2]/td[1]'
							# field_elem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, field_xpath)))
							# field_med=field_elem.text
							field_med=driver.find_element_by_xpath(field_xpath).text
							print(field_med)

							# malpractice lawsuits
							#wait_button1 = WebDriverWait(driver, 10)
							mal_link=driver.find_element_by_xpath('//img[@width="120"]')
							# print('mal_link=driver.find_element_by_xpath("//img[@width="120"]"")')
							mal_link.click()
							# print('mal_link.click()')
							mal_xpath='//*[@id="frmMain"]/table[4]/tbody/tr/td/table[2]/tbody/tr/td'
							mal_elem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, mal_xpath)))
							# print('mal_elem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, mal_xpath)))')
							
							malpractice=mal_elem.text
							print(malpractice)
							if malpractice!="None reported":
								print('malpractice!!')
								full_mal=driver.find_elements_by_xpath('//*[@id="frmMain"]/table[4]/tbody/tr')
								malpractice=full_mal[0].text

							#save to my dictionary
							phys_dict['name'] = name
							phys_dict['education'] = education
							phys_dict['field_med'] = field_med
							phys_dict['malpractice'] = malpractice
							phys_dict['county']=county
							writer.writerow(phys_dict.values())
							back_button=driver.find_element_by_xpath('//img[@name="prn"]')
							back_button.click()

						#go to next page of results
						next_page=driver.find_element_by_xpath('//img[@name="go31"]')
						next_page.click()

					except Exception as e:
						print(e)
						#driver.close()
						#break
						print('+'*50)
						print("new county- exception")
						wait_button = WebDriverWait(driver, 3)
						next_button = wait_button.until(EC.element_to_be_clickable((By.XPATH,
											'//img[@name="go11"]')))
						next_button.click()
						break
