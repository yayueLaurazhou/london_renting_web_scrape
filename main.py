# using beautiful soup to scrape rightmove if not possible, use selenium
# using api calls to get data from zoopla
# prompts user input, scrape data(price, type, address, agent contact, total square meter, number of bedrooms) and summarize(average price)
# write them into a google form, or turn them into a pandas dataframe into pdf and send email to the user
import time

# class PromptUserInput:
#     """An abstract class that obtains input from user, and store them in a global variable"""
#     def validate(self):
#         pass
#
# class Search:
#     """An abstract class that performs the search on the website"""
#
# platform = input("Which platform do you want to get data from?")


from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

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
    'studio': "item-1",
    '1': 'item-2',
    '2': 'item-3',
    '3': 'item-4',
    '4': 'item-5',
    '5': 'item-6',
    '6': 'item-7'
}


base_url = "https://www.zoopla.co.uk/to-rent/property/london/"


class ZooplaSearch:
    """A class that gets an url for scraping"""

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

    def input_address(self):
        location = self.driver.find_element(By.TAG_NAME, "input")
        location.clear()
        location.send_keys(input_data["location"])

    def input_search_radius(self):
        self.driver.maximize_window()
        search_radius_str = search_radius_selector[str(input_data["search_radius_miles"])]
        print(search_radius_str)
        search_radius = self.driver.find_element(By.XPATH,
                                                 "/html/body/div[3]/main/div/div/div/div[2]/div[2]/div[1]/div[2]/div/div/button")
        search_radius.click()
        radius_to_click = self.driver.find_element(By.XPATH, f'/html/body/div[3]/main/div/div/div/div[2]/div[2]/div[1]/div[2]/div/div/ul/li[{search_radius_str}]')
        if radius_to_click:
            radius_to_click.click()
        else:
            print("Search radius not found")

    def input_num_bedrooms(self):
        num_bedroom_str = str(input_data["min_num_bedroom"])
        num_bedroom = self.driver.find_element(By.CSS_SELECTOR, "button#select-group-bedrooms")
        num_bedroom.click()
        min_num_bedroom = self.driver.find_element(By.XPATH,
                                                   "/html/body/div[3]/main/div/div/div/div[2]/div[2]/div[1]/div[3]/div/div/div[1]/div/button")


        if num_bedroom_to_click:
            num_bedroom_to_click.click()
        else:
            print("Min Number of bedrooms not found")


    def input_price(self):
        price = self.driver.find_element(By.CSS_SELECTOR, "button#select-group-price")
        price.click()
        max_price = self.driver.find_element(By.XPATH,
                                             "/html/body/div[3]/main/div/div/div/div[2]/div[2]/div[1]/div[4]/div/div/div[2]/div/button")
        max_price_dropdown = Select(max_price)
        max_price_dropdown.select_by_visible_text(input_data["max_price_per_month"])

    @property
    def address(self):
        pass

    @property
    def agent_info(self):
        pass

    @property
    def location(self):
        pass

    @property
    def description(self):
        pass

    @property
    def floorplan(self):
        pass


test = ZooplaSearch()
test.accept_cookies()
test.input_address()
test.input_search_radius()


class CreateGoogleForm:
    pass


class CreatePdf:
    pass


class InvalidTagError(ValueError):
    pass


class EmailSender:
    pass
    # with smtplib.SMTP(YOUR_SMTP_ADDRESS, port=587) as connection:
    #     connection.starttls()
    #     result = connection.login(YOUR_EMAIL, YOUR_PASSWORD)
    #     connection.sendmail(
    #         from_addr=YOUR_EMAIL,
    #         to_addrs=YOUR_EMAIL,
    #         msg=f"Subject:Amazon Price Alert!\n\n{message}\n{url}".encode("utf-8")
    #     )
