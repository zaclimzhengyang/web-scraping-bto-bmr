from datetime import datetime
from typing import List, Dict, Any
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import getpass
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select

from models.bto_enums import SelectionType, EthnicType, BlockType
from models.data_models import UnitInformation, convert_unit_size_sqm_to_unit_size, convert_price_string_to_price
import pandas as pd

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


def get_selection_type(selection: WebElement) -> SelectionType:
    option_element = selection.find_element(By.TAG_NAME, "option")
    option_element_text: str = option_element.text
    return SelectionType(option_element_text)


def select_drop_downs(driver: webdriver.Chrome, ethnic_type: EthnicType, block_type: BlockType) -> None:
    """
    Selects Dropdowns
    - Choose Ethnic Type to "Chinese"
    - Choose Block No. to "Blk 132A"
    """
    time.sleep(5)
    drop_down_parent_container: WebElement = driver.find_element(By.CSS_SELECTOR, "div[class='container my-10']")
    drop_down_form_row: WebElement = drop_down_parent_container.find_element(By.CSS_SELECTOR, "div[class='form-row']")
    select_divs: List[WebElement] = drop_down_form_row.find_elements(By.CSS_SELECTOR, "div[class='col-lg-4 col-md-6 ']")

    for index, selection in enumerate(select_divs):
        selection_type: SelectionType = get_selection_type(selection)
        if selection_type == SelectionType.ethnic_type:
            select_element: WebElement = selection.find_element(By.CSS_SELECTOR, "select[class*='form-control select-secondary']")
            select_object: Select = Select(select_element)
            select_object.select_by_visible_text(ethnic_type.value)
        elif selection_type == SelectionType.block_type:
            select_element: WebElement = selection.find_element(By.CSS_SELECTOR, "select[class*='form-control select-secondary']")
            select_object: Select = Select(select_element)
            select_object.select_by_visible_text(block_type.value)

def scrape_block_information(driver: webdriver.Chrome, ethnic_type: EthnicType, block_type: BlockType) -> List[UnitInformation]:
    time.sleep(5)
    drop_down_parent_container: WebElement = driver.find_element(By.CSS_SELECTOR, "div[class='container my-10']")
    grid_container: WebElement = drop_down_parent_container.find_element(By.ID, "available-grid")
    grid_rows: List[WebElement] = grid_container.find_elements(By.CSS_SELECTOR, "div[class='row level']")

    final_list: List[UnitInformation] = []

    for grid_row in grid_rows:
        floor_number_div: WebElement = grid_row.find_element(By.CSS_SELECTOR, "div[class='col-md-1 col-sm-12 flat-grid floor']")
        floor_number_tag: WebElement = floor_number_div.find_element(By.TAG_NAME, "label")
        floor_number: str = floor_number_tag.text
        units_row: WebElement = grid_row.find_element(By.CSS_SELECTOR, "div[class='col-md-11 col-sm-12']")
        unit_divs: List[WebElement] = units_row.find_elements(By.CSS_SELECTOR, "div[class='flat-grid unit']")
        for unit_div in unit_divs:
            # available = True
            # available: btn btn-text-dark select-short-listing selected
            # not available: btn btn-text-dark select-short-listing grayUnitCard
            disabled_button: List[WebElement] = unit_div.find_elements(By.CSS_SELECTOR, "button[class='btn btn-text-dark select-short-listing grayUnitCard']")
            if len(disabled_button) > 0:
                available: bool = False
                print(f"available False: {available}")
            else:
                available: bool = True
                print(f"available True: {available}")

            unit_label: WebElement = unit_div.find_element(By.TAG_NAME, "label")
            unit_size: str
            unit_price: str
            unit_label_text, unit_size, unit_price = unit_label.text.strip().split("\n")
            # unit_number = '47-516'
            unit_number: str = f"{floor_number}-{unit_label_text}"
            print(f"unit_number: {unit_number}, unit_size: {unit_size}, unit_price: {unit_price}")
            unit_information: UnitInformation = UnitInformation(unit_number=unit_number, unit_size_sqm=convert_unit_size_sqm_to_unit_size(unit_size_string=unit_size), unit_price_sgd=convert_price_string_to_price(unit_price), ethnic_type=ethnic_type, block_type=block_type, created_at=datetime.utcnow(), available=available)
            final_list.append(unit_information)
    return final_list

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.implicitly_wait(0.1) # seconds
driver.maximize_window()
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

# Go to HDB Landing Page
driver.get('https://homes.hdb.gov.sg/home/landing')

driver.find_element(By.CLASS_NAME, "account-text").click() # click on log in button
login_user()
navigate_to_my_profile(driver=driver)
navigate_to_bukit_merah_ridge(driver=driver)

all_unit_information: List[UnitInformation] = []

for ethnic_type in EthnicType:
    for block_type in BlockType:
        print(f"ethnic_type: {ethnic_type}, type(ethnic_type): {ethnic_type}")
        print(f"block_type: {block_type}, type(block_type): {block_type}")
        select_drop_downs(driver=driver, ethnic_type=ethnic_type, block_type=block_type)
        block_and_ethnicity_unit_informations: List[UnitInformation] = scrape_block_information(driver=driver, ethnic_type=ethnic_type, block_type=block_type)
        all_unit_information.extend(block_and_ethnicity_unit_informations)

all_unit_information_records: List[Dict[str, Any]] = [unit_information.dict() for unit_information in all_unit_information]

df: pd.DataFrame = pd.DataFrame(all_unit_information_records)
df.to_csv("all_unit_information.csv", index=False)