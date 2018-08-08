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

driver.get("https://de.hideproxy.me/go.php?u=2d9G0AR1L93K8x5jsuQF7%2F6CeFFfm7Vzr9cKJnoafnecu6VVD6kRyqtzDvTAx5nlGA%3D%3D&b=5&f=norefer")

# Click job button to go to the job section
# Windows users need to open the file using 'wb'
# csv_file = open('jobs.csv', 'wb')


csv_file = io.open('Data_Analyst_AnalystUS.csv', 'w', encoding="utf-8", newline='')
writer = csv.writer(csv_file)
writer.writerow(['title', 'Avg_salary'])
# Page index used to keep track of where we are.
index = 1
#while index <10: # this is to check if the coding works wiht few pages 
while True:
	try:
		print("Scraping Page number " + str(index))
		index = index + 1
		# Find all the jobs on the page
		wait_job = WebDriverWait(driver, 10)
		joblist = wait_job.until(EC.presence_of_all_elements_located((By.XPATH,
									'//tr[@data-tn-component="salary-entry[]"]')))
		print("joblist length = " + str(len(joblist)))
		for job in joblist:

			# Initialize an empty dictionary for each job
			job_dict = {}
			# Use relative xpath to locate the title, text, username, date.
			# Once you locate the element, you can use 'element.text' to return its string.
			# To get the attribute instead of the text of each element, use 'element.get_attribute()'
			title = job.find_element_by_xpath('.//div[@class="cmp-sal-title"]').text 
			print("title = " + title)
			
			Avg_salary = job.find_element_by_xpath('.//div[@class="cmp-sal-summary"]').text
			print("Avg_salary = " + Avg_salary)

			
			job_dict['title'] = title
			job_dict['Avg_salary'] = Avg_salary
									
			writer.writerow(job_dict.values())


		wait_button = WebDriverWait(driver, 10)
		next_button = wait_button.until(EC.element_to_be_clickable((By.XPATH,
									'//a[@data-tn-element="next-page"]')))
		print("next_button_found")
		next_button.click()
	except Exception as e:
		print(e)
		csv_file.close()
		driver.close()
		break
