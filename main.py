from selenium import webdriver
from selenium.webdriver.support.ui import Select
import chromedriver_binary
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# get course from user
course = input(
    "Enter the course in format <course name> <course number>. Course number must be four digits (pad with 0s if necessary)\nFor Example, ECON 0100: ")

# seperate course name
courseName = course.split()[0].upper()
courseNumber = course.split()[1]

driver = webdriver.Chrome()
driver.get("https://psmobile.pitt.edu/app/catalog/classSearch")

# fill in course number
driver.find_element_by_id('catalog-nbr').send_keys(courseNumber)
# fill in subject
select = Select(driver.find_element_by_name('subject'))
select.select_by_value(courseName)
# Pick Pittsburgh Campus
select = Select(driver.find_element_by_name('campus'))
select.select_by_value("PIT")
# Pick fall term
select = Select(driver.find_element_by_name('term'))
select.select_by_value("2211")
# click search button
driver.find_element_by_id('buttonSearch').click()

# wait until page is loaded
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, ".primary-head")))


driver.quit()
