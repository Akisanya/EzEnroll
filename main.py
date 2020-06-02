from selenium import webdriver
from selenium.webdriver.support.ui import Select
import chromedriver_binary
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from collections import defaultdict

# get course from user
# TODO: validate inpuut
course = input(
    "Enter the course in format <course name> <course number>. Course number must be four digits (pad with 0s if necessary)\nFor Example, ECON 0100: ")

# seperate course name
courseName = course.split()[0].upper()
courseNumber = course.split()[1]

# initialize headless chrome driver
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)
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

# TODO: Handle case when there are no search results


# course info is stored in a nested dictionary.
# instructor -> course attrbute -> list of course attribute values
# course attribute includes status, meeting time, meeting dates, etc
# https://stackoverflow.com/questions/16333296/how-do-you-create-nested-dict-in-python/16333441
# https://stackoverflow.com/questions/5900578/how-does-collections-defaultdict-work#:~:text=A%20defaultdict%20works%20exactly%20like,returned%20by%20the%20default%20factory.
profDict = defaultdict(dict)

# extract course info from each div
# only lectures, no labs
# use list of strings for the value of the innermost map. Have a 'hasMultiple' key that returns true if
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

    # fill profDict

    # append to list if duplicate professor
    if(profName in profDict.keys()):
        profDict[profName]['days/times'].append(rest[0].text[12:])
        profDict[profName]['room'].append(rest[1].text[6:])
        profDict[profName]['meeting dates'].append(rest[3].text[15:])
        profDict[profName]['status'].append(rest[4].text[8:])
        profDict[profName]['class number'].append(title[title.find(
            "(")+1:title.find(")")])

    # initialize
    else:
        profDict[profName]['days/times'] = [rest[0].text[12:]]
        profDict[profName]['room'] = [rest[1].text[6:]]
        profDict[profName]['meeting dates'] = [rest[3].text[15:]]
        profDict[profName]['status'] = [rest[4].text[8:]]
        profDict[profName]['class number'] = [title[title.find(
            "(")+1:title.find(")")]]

driver.quit()
