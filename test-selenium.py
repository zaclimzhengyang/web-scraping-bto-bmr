from typing import List

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
import time
import getpass

def loginUser():
    # Open your browser, and point it to the login page
    someVariable = getpass.getpass("Press Enter after You are done logging in") #< THIS IS THE SECOND PART
    #Here is where you put the rest of the code you want to execute


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
# driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get('https://homes.hdb.gov.sg/home/landing')
driver.maximize_window()

# log in from landing page
# driver.maximize_window()
# time.sleep(2)
driver.find_element(By.CLASS_NAME, "account-text").click() # click on log in button
loginUser()
# element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "primary-nav-link")))

# time.sleep(1)
# driver.find_element(By.CLASS_NAME, "ndi-redirect-link-text").click() # use password instead
# time.sleep(1)
# driver.find_element(By.ID, "SpQrToggle-1FATab").click() # password log in

# manually log in
# time.sleep(20)

# after logging in
# component_list = driver.find_element(By.CLASS_NAME, "primary-nav")
# for element in component_list:
#     print(element.text)
driver.implicitly_wait(5)
# find_element > return 1 element
# find_elements > return list of elements
nav_list: WebElement = driver.find_element(By.CLASS_NAME, "primary-nav") # parent component
print(f"nav_list: {nav_list.text}, {nav_list.tag_name}")
unordered_list: WebElement = nav_list.find_element(By.TAG_NAME, "ul") # children component
li_items: List[WebElement] = unordered_list.find_elements(By.TAG_NAME, "li") # returns a list of children component
print(f"unordered_list: {unordered_list.text}, {unordered_list.tag_name}")
for element in li_items:
    if element.text == "My Profile":
        driver.implicitly_wait(5)
        clickable_element = element.find_element(By.TAG_NAME, "a")
        clickable_element.click()
        break
driver.implicitly_wait(5)
bto_projects = driver.find_element(By.TAG_NAME, "app-your-flat-application") # parent component consists of 2 childrent
driver.implicitly_wait(5)
projects = bto_projects.find_elements(By.TAG_NAME, "app-selection-flat-cards") # children component in list form
driver.implicitly_wait(5)
for project in projects: # loop through the children component
    # check project.text against name of project
    if project.text == """BTO
Bukit Merah (May 2022)
Applied flat type:
4-Room""":
        clickable_element = project.find_element(By.TAG_NAME, "a")
        clickable_element.click()

bmr_project = driver.find_element(By.CLASS_NAME, "card-body")
# print(f"bmr_project: {bmr_project.text}, {bmr_project.tag_name}")
bmr_project.click()

form_rows = driver.find_elements(By.TAG_NAME, "select")

for index, form_row in enumerate(form_rows):
    # if "Choose Ethnic Type" in form_row.text:
    print(f"index: {index}, form_row.text: {form_row.text}")
# print(row_mb_5.text)
# ethnic_type = row_mb_5.find_element(By.CLASS_NAME, "col-lg-4 col-md-6")
# print(ethnic_type.text)
# selects = row_mb_5.find_elements(By.TAG_NAME, "select")
#
# for index, select in enumerate(selects):
#     print(f"index: {index}, select.text: {select.text}")

# driver.find_element(By.TAG_NAME, "app-selection-flat-cards").click()
# driver.find_element(By.CLASS_NAME, "primary-nav-item js-primary-nav").click()
# driver.find_element(By.CLASS_NAME, "primary-nav-link").click()
# driver.find_element(By.NAME, "My Profile").click()

while True:
    pass