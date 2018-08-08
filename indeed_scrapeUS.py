from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import re
import io

# Windows users need to specify the path to chrome driver you just downloaded.
# You need to unzip the zipfile first and move the .exe file to any folder you want.
driver = webdriver.Chrome(r'C:\Users\Murugesan\Desktop\DataScience Projects\Webscrap\Indeed_selenium\chromedriver.exe')
# driver = webdriver.Chrome()

driver.get("https://de.hideproxy.me/go.php?u=AJTG6ddZhw25ADTRL5GwT9DKVBIzDFI%3D&b=5")

# Click job button to go to the job section
# Windows users need to open the file using 'wb'
# csv_file = open('jobs.csv', 'wb')
csv_file = io.open('Data_Scientist_US_deletethis.csv', 'w', encoding="utf-8", newline='')
writer = csv.writer(csv_file)
writer.writerow(['title', 'company', 'summary', 'location', 'experience', 'date'])
# Page index used to keep track of where we are.
index = 1
#while index <10:
while True:
	try:
		print("Scraping Page number " + str(index))
		index = index + 1
		# Find all the jobs on the page
		wait_job = WebDriverWait(driver, 10)
		joblist = wait_job.until(EC.presence_of_all_elements_located((By.XPATH,
									'//div[@data-tn-component="organicJob"]')))
		print("joblist length = " + str(len(joblist)))
		for job in joblist:

			# Initialize an empty dictionary for each job
			job_dict = {}
			# Use relative xpath to locate the title, text, username, date.
			# Once you locate the element, you can use 'element.text' to return its string.
			# To get the attribute instead of the text of each element, use 'element.get_attribute()'
			title = job.find_element_by_xpath('.//h2/a').get_attribute('title') 
			
			print("title = " + title)
			companyspantag = job.find_element_by_xpath('.//span[@class ="company"]')
			try: 
				company = companyspantag.find_element_by_xpath('./a').text
			except:
				company = companyspantag.text

			print("company = " + company)
			summary = job.find_element_by_xpath('.//span[@class ="summary"]').text
			print("summary = " + summary)
			location = job.find_element_by_xpath('.//span[@class ="location"]').text
			print("location = " + location)
			try:
				experience = job.find_element_by_xpath('.//span[@class ="experienceList"]').text
			except:
				experience = ""

			print("experience = " + experience)
			date = job.find_element_by_xpath('.//span[@class="date"]').text
			print("date = " + date)

			#salary = job.find_element_by_xpath('.//span[@class="no-wrap"]').get_attribute('no-wrap')

			job_dict['title'] = title
			job_dict['company'] = company
			job_dict['summary'] = summary
			job_dict['location'] = location
			job_dict['experience'] = experience
			job_dict['date'] = date
						
			writer.writerow(job_dict.values())

		# Locate the next button on the page.
		try:
			popup = driver.find_element_by_xpath('//div[@id="prime-popover-x"]')
			popup.click()
			print("closed popup")
		except:
			print("no popup")
			pass
		try:
			popup = driver.find_element_by_xpath('//a[@id="popover-close-link"]')
			popup.click()
			print("closed popup")
		except:
			print("no popup")
			pass	
		wait_button = WebDriverWait(driver, 10)
		if index == 2:
			next_button = wait_button.until(EC.element_to_be_clickable((By.XPATH,
									'//span[@class= "np"]')))
		else:
			next_button = wait_button.until(EC.element_to_be_clickable((By.XPATH,
									'(//span[@class= "np"])[2]')))

		print("next_button_found")
		next_button.click()
	except Exception as e:
		print(e)
		csv_file.close()
		driver.close()
		break
