from enum import Enum
from typing import List
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import getpass
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select


def login_user() -> None:
    # Open your browser, and point it to the login page
    getpass.getpass("Press Enter after You are done logging in") #< THIS IS THE SECOND PART


def navigate_to_my_profile(driver: webdriver.Chrome) -> None:
    """
    Gets the navigation bar, iterate through it to get "My Profile", click on it
    """
    outer_nav_element: WebElement = driver.find_element(By.CLASS_NAME, "primary-nav")
    nav_unordered_list: WebElement = outer_nav_element.find_element(By.TAG_NAME, "ul")
    nav_selections: List[WebElement] = nav_unordered_list.find_elements(By.TAG_NAME, "li")
    for nav_selection in nav_selections:
        if nav_selection.text == "My Profile":
            clickable_nav = nav_selection.find_element(By.TAG_NAME, "a")
            clickable_nav.click()
            break


def navigate_to_bukit_merah_ridge(driver: webdriver.Chrome) -> None:
    """
    Navigate from "My Profile" -> "Bukit Merah (May 2022)" to "Bukit Merah Ridge (May 2022)"
    """
    bto_projects: WebElement = driver.find_element(By.TAG_NAME,
                                       "app-your-flat-application")  # parent component consists of 2 childrent
    projects = bto_projects.find_elements(By.TAG_NAME, "app-selection-flat-cards")  # children component in list form
    for project in projects:  # loop through the children component
        # check project.text against name of project
        if "Bukit Merah (May 2022)" in project.text:
            clickable_element = project.find_element(By.TAG_NAME, "a")
            clickable_element.click()
    bmr_project = driver.find_element(By.CLASS_NAME, "card-body")
    bmr_project.click()


class SelectionType(str, Enum):
    flat_type: str = "Choose Flat Type"
    ethnic_type: str = "Choose Ethnic Type"
    block_type: str = "Choose Block No."
    unknown: str = "Unknown"

    @classmethod
    def _missing_(cls, value):
        return cls.unknown


def get_selection_type(selection: WebElement) -> SelectionType:
    option_element = selection.find_element(By.TAG_NAME, "option")
    option_element_text: str = option_element.text
    return SelectionType(option_element_text)


def select_drop_downs(driver: webdriver.Chrome) -> None:
    """
    Selects Dropdowns
    - Choose Ethnic Type to "Chinese"
    - Choose Block No. to "Blk 132A"
    """
    time.sleep(3)
    drop_down_parent_container: WebElement = driver.find_element(By.CSS_SELECTOR, "div[class='container my-10']")
    drop_down_form_row: WebElement = drop_down_parent_container.find_element(By.CSS_SELECTOR, "div[class='form-row']")
    select_divs: List[WebElement] = drop_down_form_row.find_elements(By.CSS_SELECTOR, "div[class='col-lg-4 col-md-6 ']")

    for index, selection in enumerate(select_divs):
        print(f"select: {selection.text}")
        selection_type: SelectionType = get_selection_type(selection)
        if selection_type == SelectionType.ethnic_type:
            select_element: WebElement = selection.find_element(By.CSS_SELECTOR, "select[class*='form-control select-secondary']")
            select_object: Select = Select(select_element)
            select_object.select_by_visible_text('Chinese')
        elif selection_type == SelectionType.block_type:
            select_element: WebElement = selection.find_element(By.CSS_SELECTOR, "select[class*='form-control select-secondary']")
            select_object: Select = Select(select_element)
            select_object.select_by_visible_text('Blk 132A')


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.implicitly_wait(5) # seconds
driver.maximize_window()
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

# Go to HDB Landing Page
driver.get('https://homes.hdb.gov.sg/home/landing')

driver.find_element(By.CLASS_NAME, "account-text").click() # click on log in button
login_user()
navigate_to_my_profile(driver=driver)
navigate_to_bukit_merah_ridge(driver=driver)
select_drop_downs(driver=driver)
