from selenium import webdriver
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
for option in counties.find_elements_by_tag_name("option"):
	if option.text == "Brooklyn (Borough)":
		option.click()
		break

search_it_up=driver.find_element_by_xpath('//*[@id="frmMain"]/table/tbody/tr/td/table[2]/tbody/tr/td[2]/table/tbody/tr/td[2]/table[1]/tbody/tr[3]/td/table/tbody/tr[19]/td[1]/input')
search_it_up.click()

table_xpath='//*[@id="frmMain"]/table/tbody/tr/td/table[2]/tbody/tr/td[2]/table/tbody/tr/td[2]/table[1]/tbody/tr[2]/td/table[2]/tbody/tr/td/table[2]/tbody/tr'
page_table=driver.find_elements_by_xpath(table_xpath)
print(len(page_table))
print('-'*50)

print(page_table[0].text)



physician_link=driver.find_element_by_xpath('//*[@id="frmMain"]/table/tbody/tr/td/table[2]/tbody/tr/td[2]/table/tbody/tr/td[2]/table[1]/tbody/tr[2]/td/table[2]/tbody/tr/td/table[2]/tbody/tr[1]/td[1]/a')
print(physician_link.text)
#physician_link.click()

# ed_link=driver.find_element_by_xpath('//img[@name="ed"]')
# ed_link.click()

# # Iterate through the table of physicians
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
# 	#print(review_body)
# # Locate the next button element on the page and then call `button.click()` to click it.
# button = driver.find_element_by_xpath('//li[@class="nextClick displayInlineBlock padLeft5 "]')
# button.click()
# time.sleep(2) # to wait for loading the internet

#physicia2_link=driver.find_element_by_xpath('//*[@id="frmMain"]/table/tbody/tr/td/table[2]/tbody/tr/td[2]/table/tbody/tr/td[2]/table[1]/tbody/tr[2]/td/table[2]/tbody/tr/td/table[2]/tbody/tr[2]/td[1]/a')


# Search Results: COME BACK LATER
#test=driver.find_element_by_xpath('//*[@id="frmMain"]/table/tbody/tr/td/table[2]/tbody/tr/td[2]/table/tbody/tr/td[2]/table[1]/tbody/tr[2]/td/table[1]/tbody/tr[1]/td/p/') #text()[1]
#test=driver.find_element_by_xpath('//*[@id="frmMain"]/table/tbody/tr/td/table[2]/tbody/tr/td[2]/table/tbody/tr/td[2]/table[1]/tbody/tr[2]/td/table[1]/tbody/tr[1]/td/p/br[1]')
#test=driver.find_element_by_xpath('//p[@class="data"').text
