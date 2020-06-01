from selenium import webdriver
from selenium.webdriver.support.ui import Select
import chromedriver_binary
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import collections

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

# wait until page is loaded, waits maximum of 10 seconds
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, ".primary-head")))


# contains divs containing each of the availabe courses
courseDivs = driver.find_elements_by_css_selector(
    '#search-results .section-content')


# course info is stored in a nested dictionary.
# instructor -> course attrbute -> course attribute value
# course attribute includes status, meeting time, meeting dates, etc
profDict = collections.defaultdict(dict)
temp = {}

# extract course info from each div
# only lectures, no labs
# TODO: Handle duplicate professors for the same course
# use list of strings for the value of the innermost map. Have a 'hasMultiple' key that returns true if
# a professor has multiple sections
for x in courseDivs:
    # extracts class number if it is a lecture
    title = x.find_element_by_css_selector('.strong.section-body').text

    # skip lab sections and recitations
    if(title.find('LAB') != -1 or title.find('REC') != -1):
        continue

    rest = x.find_elements_by_css_selector('.section-body')

    # first element is class number which has already been added to temp
    rest.pop(0)
    rest.pop(0)  # first element is unimportant

    # extract prof name, unless it is staff
    if(rest[2].text.find("Staff") == -1):
        profNames = rest[2].text.split()
        profName = profNames[1] + " " + profNames[2]
        if(profName[len(profName)-1] == ','):
            profName = profName[:-1]

    # add staff
    else:
        profName = "Staff"

    # skip labels in HTML and assign values in profDict
    profDict[profName]['days/times'] = rest[0].text[12:]
    profDict[profName]['room'] = rest[1].text[6:]
    profDict[profName]['meeting dates'] = rest[3].text[15:]
    profDict[profName]['status'] = rest[4].text[8:]
    profDict[profName]['class number'] = title[title.find(
        "(")+1:title.find(")")]


driver.quit()
