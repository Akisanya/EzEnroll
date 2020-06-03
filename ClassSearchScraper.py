from selenium import webdriver
from selenium.webdriver.support.ui import Select
import chromedriver_binary
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from collections import defaultdict


# initialize headless chrome driver
# adds adblock: driver.add_extension('Adblock-Plus_v.crx')
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)


class PittClassSearch:
    def __init__(self, course):
        # seperate course name and number
        self.courseName = course.split()[0].upper()
        self.courseNumber = course.split()[1]
        # use selenium to search for the course and return divs containg the search results
        divs = self.searchClass()
        # parse the divs and fill dictionary
        self.profDict = self.parseDivs(divs)
        driver.quit()

    def searchClass(self):
        driver.get("https://psmobile.pitt.edu/app/catalog/classSearch")
        # fill in course number
        driver.find_element_by_id('catalog-nbr').send_keys(self.courseNumber)
        # fill in subject
        select = Select(driver.find_element_by_name('subject'))
        select.select_by_value(self.courseName)
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
        return courseDivs

    def parseDivs(self, courseDivs):
        # {instructor<str> -> {course attrbute<str> -> [course attribute values]<str>}}
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

        return profDict

    def getProfDict(self):
        return self.profDict
