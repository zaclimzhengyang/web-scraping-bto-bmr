from selenium import webdriver
from selenium.webdriver.common.by import By
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
driver.find_element(By.CLASS_NAME, "primary-nav-link").click()
# driver.find_element(By.CLASS_NAME, "primary-nav-link").click()
# driver.find_element(By.NAME, "My Profile").click()

while True:
    pass