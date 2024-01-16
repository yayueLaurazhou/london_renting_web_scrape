from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import math

# min_num_bedroom from studio to 6, max_price_per_month from 600 to 4000, search radius miles from 0.25 to 10
# since the those input fields need scrolling to show the rest of the elements
input_data = {
    "location": "EC1V",
    "min_num_bedroom": 3,
    "max_price_per_month": 3000,
    "search_radius_miles": 5
}

search_radius_selector = {
    '0': '0',
    '0.25': '1',
    '0.5': '2',
    '1': '3',
    '3': '4',
    '5': '5',
    '10': '6'
}

num_bedrooms_selector = {
    'studio': "1",
    '1': '2',
    '2': '3',
    '3': '4',
    '4': '5',
    '5': '6',
    '6': '7'
}

base_url = "https://www.zoopla.co.uk/to-rent/property/london/"


class ZooplaSearch:
    """A class that uses selenium to input filter"""

    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option('detach', True)
        self.driver = webdriver.Chrome(options=chrome_options)

    def accept_cookies(self):
        self.driver.get(base_url)
        self.driver.switch_to.frame('gdpr-consent-notice')
        WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(
                (By.ID, "save")
            )
        )
        try:
            accept_button = self.driver.find_element(By.ID, "save")
            accept_button.click()
        except NoSuchElementException:
            raise InvalidTagError("Cannot find such an element")
        finally:
            self.driver.switch_to.default_content()
            self.driver.maximize_window()

    def input_address(self):
        location = self.driver.find_element(By.TAG_NAME, "input")
        location.clear()
        location.send_keys(input_data["location"])

    def input_search_radius(self):
        # Sometimes the website needs verification of human, in that case, can only input the requirements by hand
        search_radius_str = search_radius_selector[str(input_data["search_radius_miles"])]
        print(search_radius_str)
        time.sleep(5)
        search_radius = self.driver.find_element(By.XPATH,
                                                 "/html/body/div[3]/main/div/div/div/div[2]/div[2]/div[1]/div[2]/div/div/button")
        search_radius.click()
        time.sleep(5)
        WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH,
                 f'/html/body/div[3]/main/div/div/div/div[2]/div[2]/div[1]/div[2]/div/div/ul/li[{search_radius_str}]')
            )
        )
        radius_to_click = self.driver.find_element(By.XPATH,
                                                   f'/html/body/div[3]/main/div/div/div/div[2]/div[2]/div[1]/div[2]/div/div/ul/li[{search_radius_str}]')
        try:
            radius_to_click.click()
        except NoSuchElementException:
            raise InvalidTagError("Cannot find such an element")

    def input_num_bedrooms(self):
        num_bedroom_str = num_bedrooms_selector[str(input_data["min_num_bedroom"])]
        num_bedroom = self.driver.find_element(By.CSS_SELECTOR, "button#select-group-bedrooms")
        time.sleep(3)
        num_bedroom.click()
        time.sleep(3)
        min_num_bedroom = self.driver.find_element(By.XPATH,
                                                   "/html/body/div[3]/main/div/div/div/div[2]/div[2]/div[1]/div[3]/div/div/div[1]/div/button")
        min_num_bedroom.click()
        time.sleep(5)
        WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH,
                 f'/html/body/div[3]/main/div/div/div/div[2]/div[2]/div[1]/div[3]/div/div/div[1]/div/ul/li[{num_bedroom_str}]')
            )
        )
        num_bedroom_to_click = self.driver.find_element(By.XPATH,
                                                        f'/html/body/div[3]/main/div/div/div/div[2]/div[2]/div[1]/div[3]/div/div/div[1]/div/ul/li[{num_bedroom_str}]')
        try:
            num_bedroom_to_click.click()
        except NoSuchElementException:
            raise InvalidTagError("Cannot find such an element")

    def input_price(self):
        # choose the <li> in the <ul> in the XPATH according to the input price
        price_selector = math.ceil((int(input_data["max_price_per_month"])) / 100)
        print(price_selector)
        price = self.driver.find_element(By.CSS_SELECTOR, "button#select-group-price")
        price.click()
        max_price = self.driver.find_element(By.XPATH,
                                             "/html/body/div[3]/main/div/div/div/div[2]/div[2]/div[1]/div[4]/div/div/div[2]/div/button")
        max_price.click()
        time.sleep(3)
        max_price_to_scroll = self.driver.find_element(By.XPATH,
                                                       '/html/body/div[3]/main/div/div/div/div[2]/div[2]/div[1]/div[4]/div/div/div[2]/div/ul')
        self.driver.execute_script("arguments[0].scrollTop = (arguments[0].scrollHeight)/2", max_price_to_scroll)

        # js_script = """
        #     element = argument[0]
        #     element.scrollIntoView({block = 'start'})
        # """
        # self.driver.execute_script(js_script, max_price_to_click)
        # try:
        #     max_price_to_click.click()
        # except NoSuchElementException:
        #     raise InvalidTagError("Cannot find such an element")


test = ZooplaSearch()
test.accept_cookies()
test.input_price()


class InvalidTagError(ValueError):
    pass
