from bs4 import BeautifulSoup

# from lxml import html
# import requests

input_data = {
    "location": "EC1Y1BE",
    "min_num_bedroom": 3,
    "max_price_per_month": 3000,
    "search_radius_miles": 5
}
base_url = "https://www.zoopla.co.uk/to-rent/property/london/"


def validate_address():
    """Location must be a valid UK postcode address"""
    pass


def create_url():
    location_str = '-'.join([input_data["location"][:3].lower(), input_data['location'][4:].lower()])
    return base_url + location_str + f"/?beds_min={input_data['min_num_bedroom']}&price_frequency=per_month&price_max={input_data['max_price_per_month']}&radius={input_data['search_radius_miles']}&results_sort=newest_listings&search_source=to-rent"


class ListingsData:
    def __init__(self):
        self.page = requests.get(create_url()).content
        self.tree = html.fromstring(self.page)
        # chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_experimental_option('detach', True)
        # self.driver = webdriver.Chrome(options=chrome_options)
        # self.url = create_url()

    @property
    def price(self):
        """Zoopla doesn't allow return the text of a tag, returns a <property object>
        In robots.txt it states that it blocks general scraping from /property and its subdirectories"""
        # self.driver.get(self.url)
        # price_xpath = "/html/body/div[3]/main/div/div/div/div[2]/div[3]/div/section/div[2]/div[3]/div[1]/div[1]/div/div/div/div[2]/div/a/div/div[1]/div/p[1]"
        # return self.tree.xpath(price_xpath)
        # price = self.driver.find_element(By.XPATH, price_xpath).text
        # return price




    @property
    def address(self):
        pass

    @property
    def agent_contact(self):
        pass

    @property
    def location(self):
        pass

    @property
    def description(self):
        pass

    @property
    def avaliable_date(self):
        pass

    @property
    def floorplan(self):
        pass


test = ListingsData()
print(ListingsData.price)
